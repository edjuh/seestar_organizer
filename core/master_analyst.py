"""
Filename: core/master_analyst.py
Version: 0.8.3 (Hardened)
Role: The WCS-to-Pixel Bridge
Objective: Orchestrates the plate-solver and pixel mapper. Features automatic
           fallback to Blind Solving if coordinate hints are missing.
"""
from pathlib import Path
from core.logger import log_event
from core.analyst import analyst
from core.pixel_mapper import get_pixel_coords
from utils.astro import ra_to_decimal, dec_to_decimal

class MasterAnalyst:
    def __init__(self):
        pass

    def get_target_pixel(self, fits_path, ra_input=None, dec_input=None):
        log_event(f"MasterAnalyst: Processing target at RA:{ra_input} DEC:{dec_input}")
        
        # 1. Coordinate Conversion (with Blind Solve Fallback)
        ra_deg, dec_deg = None, None
        if ra_input is not None and dec_input is not None:
            try:
                ra_deg = ra_to_decimal(ra_input)
                dec_deg = dec_to_decimal(dec_input)
            except Exception as e:
                log_event(f"MasterAnalyst: Hint conversion failed ({e}). Falling back to Blind Solve.", level="error")
        else:
            log_event("MasterAnalyst: Missing coordinates. Forcing Blind Solve.")

        # 2. Solve the image (creates the .wcs file)
        wcs_file = analyst.solve_image(fits_path, hint_ra=ra_deg, hint_dec=dec_deg)
        
        if not wcs_file:
            log_event("MasterAnalyst: Failed to acquire WCS map. Solving aborted.", level="error")
            return None, None

        # 3. Map the WCS coordinates to Pixels
        # If we did a blind solve, we don't have a specific target RA/Dec to map yet,
        # so we just return the center of the solved image as a proof of life.
        if ra_deg is None or dec_deg is None:
            # Astrometry.net always solves if a .wcs is made. We can extract the center.
            from astropy.wcs import WCS
            try:
                w = WCS(str(wcs_file))
                # Get the pixel coordinates for the reference pixel (usually image center)
                x, y = w.wcs.crpix
                log_event(f"MasterAnalyst: Blind Solve mapped reference pixel to X:{x:.2f}, Y:{y:.2f}")
                return float(x), float(y)
            except Exception as e:
                log_event(f"MasterAnalyst: WCS read error after blind solve -> {e}", level="error")
                return None, None

        # Normal hinted mapping
        x, y = get_pixel_coords(str(wcs_file), ra_deg, dec_deg)
        
        if x is not None and y is not None:
            log_event(f"MasterAnalyst: Target successfully mapped to X:{x:.2f}, Y:{y:.2f}")
            return x, y
        else:
            log_event("MasterAnalyst: Pixel mapping returned None.", level="error")
            return None, None

# Instantiate for easy importing
master_analyst = MasterAnalyst()
