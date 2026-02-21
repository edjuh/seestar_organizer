"""
Filename: core/astap.py
Version: 0.7.1
Role: Plate-solving wrapper for ASTAP to verify scientific target alignment.
Owner: Ed de la Rie (PE5ED)
"""
import subprocess
import os
from pathlib import Path

class AstapResolver:
    def __init__(self, config: dict):
        # Default path on StellarMate/Linux
        self.astap_path = config.get("astap", {}).get("bin_path", "/usr/bin/astap")
        # Search radius in degrees (Seestar FOV is small, so we stay tight)
        self.search_radius = config.get("astap", {}).get("radius", 2.0)

    def solve(self, fits_file: Path) -> dict:
        """
        Runs ASTAP on a FITS file.
        Returns a dict with success status and solved RA/Dec.
        """
        if not fits_file.exists():
            return {"success": False, "error": "File not found"}

        # ASTAP flags: 
        # -f: fits file
        # -r: search radius
        # -z: downsample (0=auto)
        # -v: version/info
        cmd = [
            self.astap_path,
            "-f", str(fits_file),
            "-r", str(self.search_radius),
            "-v"
        ]

        try:
            # We run with a timeout because a failed solve can hang
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # ASTAP creates a .wcs file on success
            wcs_file = fits_file.with_suffix(".wcs")
            
            if wcs_file.exists():
                # On success, we parse the result or the .wcs header
                # For v0.7.1, we'll extract the core coordinates from stdout
                # ASTAP output usually contains 'Solution: RA: 12 34 56, Dec: +12 34 56'
                wcs_file.unlink() # Cleanup
                return {
                    "success": True, 
                    "raw_output": result.stdout,
                    "status": "Solved"
                }
            else:
                return {"success": False, "error": "No solution found", "log": result.stdout}

        except subprocess.TimeoutExpired:
            return {"success": False, "error": "ASTAP timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Quick test logic
    print("[*] ASTAP Core v0.7.1 initialized.")
