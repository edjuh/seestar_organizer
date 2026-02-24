import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from core.calibration_engine import calibration_engine

targets = [
    {"name": "MU Cam", "file": "mu_cam.fits", "ra": "03:53:18", "dec": "+62:11:48"},
    {"name": "SS Cyg", "file": "ss_cyg.fits", "ra": "21:42:45", "dec": "+43:35:08"},
    {"name": "Algol",  "file": "algol.fits",  "ra": "03:08:10", "dec": "+40:57:20"},
    {"name": "RR Lyr", "file": "rr_lyrae.fits", "ra": "19:22:33", "dec": "+42:47:03"}
]

def run_photometry_sweep():
    print(f"{'TARGET':<10} | {'RA/DEC':<20} | {'CALC V-MAG':<12} | {'STATUS'}")
    print("-" * 65)
    
    for t in targets:
        f_path = PROJECT_ROOT / "tests" / "samples" / t['file']
        if not f_path.exists():
            print(f"{t['name']:<10} | {'MISSING FILE':<20} | {'N/A':<12} | ❌")
            continue
            
        mag = calibration_engine.calculate_magnitude(
            str(f_path), 
            t['ra'], 
            t['dec'], 
            t['name']
        )
        
        if mag:
            print(f"{t['name']:<10} | {t['ra']}/{t['dec']:<11} | {mag:>10.3f}   | ✅ LOCKED")
        else:
            # This will happen for MU Cam because the comp stars are out of bounds
            print(f"{t['name']:<10} | {t['ra']}/{t['dec']:<11} | {'FAILED':>10}   | ⚠️ NO COMPS/FLUX")

if __name__ == "__main__":
    run_photometry_sweep()
