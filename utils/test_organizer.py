#!/usr/bin/env python3
"""
Filename: utils/test_organizer.py
Description: Generates fake FITS files to test the organizer logic.
"""
import numpy as np
from astropy.io import fits
from pathlib import Path
import time
import os

def create_fake_fits(target, filt):
    source_dir = Path("/home/stellarmate/seestar_downloads")
    source_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = int(time.time())
    fname = f"Seestar_{target}_{filt}_{timestamp}.fits"
    path = source_dir / fname
    
    data = np.random.random((100, 100)).astype(np.float32)
    hdu = fits.PrimaryHDU(data)
    
    hdu.header['OBJECT'] = target
    hdu.header['FILTER'] = filt
    hdu.header['DATE-OBS'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    hdu.header['EXPTIME'] = 30.0
    
    hdu.writeto(path, overwrite=True)
    print(f"Generated: {path}")

if __name__ == "__main__":
    targets = [("SS_Cyg", "V"), ("V_Sge", "B"), ("Z_Cam", "V")]
    for t, f in targets:
        create_fake_fits(t, f)
