import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from core.calibration_engine import calibration_engine

def test_full_pipeline():
    fits_file = PROJECT_ROOT / "tests" / "samples" / "ss_cyg.fits"
    target_name = "SS Cyg"
    target_ra = "21:42:45"
    target_dec = "+43:35:08"
    
    print(f"🚀 Initiating End-to-End Photometry for {target_name}...")
    
    final_mag = calibration_engine.calculate_magnitude(
        str(fits_file), 
        target_ra, 
        target_dec, 
        target_name
    )
    
    if final_mag:
        print("\n" + "="*50)
        print(f"⭐ FINAL RESULT: {target_name} Apparent V-Magnitude: {final_mag:.3f}")
        print("="*50)
    else:
        print("\n❌ Pipeline failed. Check logs.")

if __name__ == "__main__":
    test_full_pipeline()
