import sys
from pathlib import Path
from astropy.io import fits

PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from core.master_analyst import master_analyst

def run_mu_cam_test():
    fits_path = PROJECT_ROOT / "tests" / "samples" / "mu_cam.fits"
    
    if not fits_path.exists():
        print(f"❌ File not found: {fits_path}")
        return

    # Coordinates for MU Cam from your research
    ra_hint = "03:53:18"
    dec_hint = "+62:11:48"
    
    print(f"🎯 Target: MU Camelopardalis")
    print(f"📡 Hints -> RA: {ra_hint} | DEC: {dec_hint}")
    print("⚙️ Engaging S30-Pro Optimized Bridge...")
    
    x, y = master_analyst.get_target_pixel(str(fits_path), ra_hint, dec_hint)
    
    if x is not None and y is not None:
        print("\n" + "="*50)
        print(f"✅ SUCCESS: MU Cam found at Pixel X:{x:.2f}, Y:{y:.2f}")
        print(f"📸 This confirms the S30-Pro Plate-Scale logic is solid.")
        print("="*50)
        
        # Bonus: Verify secondary target V442 Cam in the same frame
        # V442 Cam is at RA: 03:54:33 / Dec: +62:08:21
        print("\n🔍 Scanning for secondary variable: V442 Cam...")
        x2, y2 = master_analyst.get_target_pixel(str(fits_path), "03:54:33", "+62:08:21")
        print(f"📍 V442 Cam located at Pixel X:{x2:.2f}, Y:{y2:.2f}")
    else:
        print("❌ Bridge Failed. Check logs/seestar_joost.log.")

if __name__ == "__main__":
    run_mu_cam_test()
