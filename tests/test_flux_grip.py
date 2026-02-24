import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from core.master_analyst import master_analyst
from core.photometry_engine import phot_engine

def test_aperture_grip():
    fits_file = PROJECT_ROOT / "tests" / "samples" / "mu_cam.fits"
    ra, dec = "03:53:18", "+62:11:48"
    
    print(f"1. Asking MasterAnalyst for Coordinates of MU Cam...")
    x, y = master_analyst.get_target_pixel(str(fits_file), ra, dec)
    
    if x and y:
        print(f"✅ MasterAnalyst mapped to X:{x:.2f}, Y:{y:.2f}")
        print(f"2. Engaging PhotometryEngine to extract Instrumental Flux...")
        
        result = phot_engine.extract_flux(str(fits_file), x, y)
        
        if result:
            print("-" * 50)
            print(f"🎯 Refined Centroid : X:{result['x_ref']:.2f}, Y:{result['y_ref']:.2f}")
            print(f"🌌 Sky Background   : {result['sky_bkg']:.2f} ADU/pixel")
            print(f"📦 Raw Aperture Sum : {result['raw_flux']:.2f} ADU")
            print(f"✨ Instrumental Flux: {result['inst_flux']:.2f} ADU")
            print("-" * 50)
        else:
            print("❌ PhotometryEngine failed to extract flux.")
    else:
        print("❌ MasterAnalyst failed to solve.")

if __name__ == "__main__":
    test_aperture_grip()
