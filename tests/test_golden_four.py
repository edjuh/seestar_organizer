import sys
from pathlib import Path
from core.master_analyst import master_analyst

PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

targets = [
    {"name": "MU Cam", "file": "mu_cam.fits", "ra": "03:53:18", "dec": "+62:11:48"},
    {"name": "SS Cyg", "file": "ss_cyg.fits", "ra": "21:42:45", "dec": "+43:35:08"},
    {"name": "Algol",  "file": "algol.fits",  "ra": "03:08:10", "dec": "+40:57:20"},
    {"name": "RR Lyr",  "file": "rr_lyrae.fits", "ra": "19:22:33", "dec": "+42:47:03"}
]

def run_sweep():
    print(f"{'TARGET':<12} | {'RA/DEC HINT':<25} | {'PIXEL X':<8} | {'PIXEL Y':<8} | {'STATUS'}")
    print("-" * 75)
    
    for t in targets:
        f_path = PROJECT_ROOT / "tests" / "samples" / t['file']
        if not f_path.exists():
            print(f"{t['name']:<12} | File Missing")
            continue
            
        x, y = master_analyst.get_target_pixel(str(f_path), t['ra'], t['dec'])
        
        if x is not None:
            status = "🎯 CENTERED" if (950 < x < 970) else "✅ MAPPED"
            print(f"{t['name']:<12} | {t['ra']}/{t['dec']:<20} | {x:>8.2f} | {y:>8.2f} | {status}")
        else:
            print(f"{t['name']:<12} | SOLVE FAILED")

if __name__ == "__main__":
    run_sweep()
