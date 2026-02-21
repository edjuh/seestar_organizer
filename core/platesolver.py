"""
Filename: core/platesolver.py
Version: 1.2.3 (Reniced)
Purpose: Wrapper for ASTAP. 
         - Determines pointing coordinates.
         - Runs at LOW PRIORITY (nice -n 15) to protect guiding.
"""
import subprocess
import shutil
import re
from pathlib import Path

class PlateSolver:
    def __init__(self, config: dict):
        self.simulate = config.get("alpaca", {}).get("simulate", False)
        # Try to find ASTAP executable
        self.bin_path = shutil.which("astap") or "/usr/bin/astap"
        # Try to find 'nice' for priority management
        self.nice_path = shutil.which("nice") or "/usr/bin/nice"
        
    def solve(self, image_path: Path, hint_ra=0.0, hint_dec=0.0, search_radius=30.0):
        """
        Solves the image using ASTAP with Low CPU Priority.
        """
        # 1. Simulation Bypass
        if self.simulate:
            return {
                "success": True, 
                "ra": hint_ra, 
                "dec": hint_dec, 
                "error_deg": 0.000,
                "msg": "Simulated Solve"
            }

        # 2. Binary Check
        if not Path(self.bin_path).exists():
            return {"success": False, "msg": "ASTAP binary not found"}
            
        if not image_path.exists():
             return {"success": False, "msg": "Image file not found"}

        # 3. Build Command with Renice
        # nice -n 15 astap -f file.fits ...
        # -n 15 means "Very polite". (0 is normal, 19 is lowest priority)
        cmd = [
            self.nice_path, "-n", "15",
            self.bin_path,
            "-f", str(image_path),
            "-ra", str(hint_ra),
            "-dec", str(hint_dec),
            "-r", str(search_radius), 
            "-z", "0"
        ]

        try:
            # 4. Execute (Timeout 45s for Pi)
            subprocess.run(cmd, capture_output=True, timeout=45)
            
            # 5. Check for Result
            wcs_file = image_path.with_suffix(".wcs")
            if wcs_file.exists():
                return self._parse_wcs(wcs_file, hint_ra, hint_dec)
            
            return {"success": False, "msg": "No solution found (Timeout or Star count)"}

        except Exception as e:
            return {"success": False, "msg": str(e)}

    def _parse_wcs(self, wcs_path, hint_ra, hint_dec):
        """Extracts RA/DEC from the WCS header file."""
        try:
            content = wcs_path.read_text()
            
            ra_match = re.search(r"CRVAL1\s*=\s*([0-9\.\-]+)", content)
            dec_match = re.search(r"CRVAL2\s*=\s*([0-9\.\-]+)", content)
            
            if ra_match and dec_match:
                ra_deg = float(ra_match.group(1))
                dec_deg = float(dec_match.group(1))
                
                solved_ra = ra_deg / 15.0
                solved_dec = dec_deg
                
                # Euclidean Error Distance
                ra_diff = (solved_ra - hint_ra) * 15.0
                dec_diff = solved_dec - hint_dec
                error = (ra_diff**2 + dec_diff**2)**0.5
                
                return {
                    "success": True,
                    "ra": round(solved_ra, 5),
                    "dec": round(solved_dec, 5),
                    "error_deg": round(error, 5),
                    "msg": "Solved"
                }
        except Exception:
            pass
            
        return {"success": False, "msg": "WCS Parse Failed"}
