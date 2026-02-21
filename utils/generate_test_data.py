#!/usr/bin/env python3
"""
Filename: utils/generate_test_data.py
Description: Generates dummy FITS files with AAVSO headers for testing.
"""
import os
import time
from pathlib import Path
from astropy.io import fits
import numpy as np

def create_dummy_fits(dest_folder, target_name, filter_name):
    path = Path(dest_folder)
    path.mkdir(parents=True, exist_ok=True)
    
    filename = f"Seestar_{target_name}_{filter_name}_{int(time.time())}.fits"
    file_path = path / filename
    
    # Create a small dummy image (100x100)
    data = np.random.random((100, 100)).astype(np.float32)
    hdu = fits.PrimaryHDU(data)
    
    # Add AAVSO-style headers
    header = hdu.header
    header['OBJECT'] = target_name
    header['FILTER'] = filter_name
    header['EXPTIME'] = 10.0
    header['INSTRUME'] = 'Seestar S30'
    header['OBSERVER'] = 'Ed de la Rie'
    
    hdu.writeto(file_path, overwrite=True)
    print(f"Generated: {file_path}")

if __name__ == "__main__":
    # Test targets
    targets = [("V_Sge", "V"), ("SS_Cyg", "B"), ("Z_Cam", "V")]
    # Assuming source_dir from config is /home/stellarmate/seestar_downloads
    test_source = Path("/home/stellarmate/seestar_downloads")
    
    print(f"Creating test data in {test_source}...")
    for obj, filt in targets:
        create_dummy_fits(test_source, obj, filt)
