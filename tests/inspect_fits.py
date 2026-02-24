import sys
from astropy.io import fits
from pathlib import Path

fits_file = Path(__file__).parent / "samples" / "ss_cyg.fits"

try:
    with fits.open(fits_file) as hdul:
        header = hdul[0].header
        print("=== FITS HEADER DNA ===")
        print(f"INSTRUMENT : {header.get('INSTRUME', 'Unknown')}")
        print(f"CAMERA     : {header.get('CAMERA', 'Unknown')}")
        print(f"BAYER PAT  : {header.get('BAYERPAT', 'Unknown')}")
        print(f"EXPOSURE   : {header.get('EXPTIME', 'Unknown')}s")
        print(f"FOCAL LEN  : {header.get('FOCALLEN', 'Unknown')}mm")
        print(f"PIXEL SIZE : {header.get('XPIXSZ', 'Unknown')}um")
        print(f"IMAGE SIZE : {header.get('NAXIS1')} x {header.get('NAXIS2')}")
except Exception as e:
    print(f"Failed to read header: {e}")
