"""
Filename: core/calibration_engine.py
Objective: Manages Zero-Point (ZP) offsets and flat-field corrections for the IMX585.
"""
import json
import math
from pathlib import Path
from core.logger import log_event
from core.master_analyst import master_analyst
from core.photometry_engine import phot_engine

class CalibrationEngine:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.resolve()

    def load_sequence(self, target_name):
        # We assume sequences are named like mu_cam.json
        safe_name = target_name.lower().replace(" ", "_")
        json_path = self.project_root / "data" / "sequences" / f"{safe_name}.json"
        
        if not json_path.exists():
            log_event(f"CalibrationEngine: Sequence file missing -> {json_path}", level="error")
            return None
            
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            log_event(f"CalibrationEngine: Failed to parse JSON -> {e}", level="error")
            return None

    def calculate_magnitude(self, fits_path, target_ra, target_dec, target_name):
        log_event(f"CalibrationEngine: Initiating photometry for {target_name}")
        
        # 1. Get Target Flux
        tx, ty = master_analyst.get_target_pixel(fits_path, target_ra, target_dec)
        if not tx or not ty:
            return None
            
        target_data = phot_engine.extract_flux(fits_path, tx, ty)
        if not target_data or target_data['inst_flux'] <= 0:
            log_event("CalibrationEngine: Invalid target flux. Aborting.", level="error")
            return None
            
        target_inst_flux = target_data['inst_flux']
        
        # 2. Load Comp Stars
        comp_stars = self.load_sequence(target_name)
        if not comp_stars:
            return None
            
        # 3. Calculate Zero Point from valid Comp Stars
        zero_points = []
        for comp in comp_stars:
            # Extract V mag from the bands array
            v_mag = None
            for band in comp.get('bands', []):
                if band.get('band') == 'V':
                    v_mag = band.get('mag')
                    break
                    
            if v_mag is None:
                continue
                
            cx, cy = master_analyst.get_target_pixel(fits_path, comp['ra'], comp['dec'])
            if not cx or not cy:
                continue
                
            comp_data = phot_engine.extract_flux(fits_path, cx, cy)
            if comp_data and comp_data['inst_flux'] > 0:
                # ZP = True Mag + 2.5 * log10(Instrumental Flux)
                zp = v_mag + 2.5 * math.log10(comp_data['inst_flux'])
                zero_points.append(zp)
                log_event(f"CalibrationEngine: Comp {comp['label']} -> ZP: {zp:.3f}")
                
        if not zero_points:
            log_event("CalibrationEngine: Failed to extract flux for any comparison stars.", level="error")
            return None
            
        # Average the Zero Points for stability
        avg_zp = sum(zero_points) / len(zero_points)
        
        # 4. Calculate Final Target Magnitude
        # Target Mag = ZP - 2.5 * log10(Target Instrumental Flux)
        target_mag = avg_zp - 2.5 * math.log10(target_inst_flux)
        
        log_event(f"CalibrationEngine: {target_name} calculated V-Mag: {target_mag:.3f} (Avg ZP: {avg_zp:.3f} from {len(zero_points)} comps)")
        return target_mag

# Instantiate
calibration_engine = CalibrationEngine()
