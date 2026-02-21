"""
Filename: test_rejection.py
Purpose: Create a fake FITS file with a satellite trail to test the Guard Dog.
"""
import numpy as np
from astropy.io import fits
from pathlib import Path

# Path to your downloads folder
target_path = Path("/home/stellarmate/seestar_downloads/SATELLITE_TEST.fits")

# 1. Create a dark star field (simulated)
data = np.random.normal(loc=100, scale=10, size=(1024, 1024)).astype(np.uint16)

# 2. Draw a bright "Satellite Trail" (a diagonal line)
for i in range(200, 800):
    data[i, i] = 50000  # Very bright pixel line
    data[i, i+1] = 45000
    data[i, i-1] = 45000

# 3. Save it
hdu = fits.PrimaryHDU(data)
hdu.writeto(target_path, overwrite=True)
print(f"Generated {target_path}. Watch the dashboard to see it get REJECTED!")
