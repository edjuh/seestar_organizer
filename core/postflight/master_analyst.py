"""
Filename: core/master_analyst.py
Objective: High-level plate-solving coordinator for narrow-field Seestar frames.
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
        fits_file = Path(fits_path)
        wcs_file = fits_file.with_suffix('.wcs')
        
        ra_deg, dec_deg = None, None
        if ra_input is not None and dec_input is not None:
            try:
                ra_deg = ra_to_decimal(ra_input)
                dec_deg = dec_to_decimal(dec_input)
            except Exception as e:
                log_event(f"MasterAnalyst: Hint conversion failed ({e}).", level="error")

        # Check if we already solved this image to save CPU
        if not wcs_file.exists():
            wcs_file_solved = analyst.solve_image(str(fits_file), hint_ra=ra_deg, hint_dec=dec_deg)
            if not wcs_file_solved:
                log_event("MasterAnalyst: Failed to acquire WCS map.", level="error")
                return None, None
        else:
            log_event(f"MasterAnalyst: Reusing existing WCS map -> {wcs_file.name}")

        if ra_deg is None or dec_deg is None:
            from astropy.wcs import WCS
            try:
                w = WCS(str(wcs_file))
                x, y = w.wcs.crpix
                return float(x), float(y)
            except Exception as e:
                return None, None

        x, y = get_pixel_coords(str(wcs_file), ra_deg, dec_deg)
        
        if x is not None and y is not None:
            return x, y
        else:
            return None, None

master_analyst = MasterAnalyst()
