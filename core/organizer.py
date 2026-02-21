"""
Filename: core/organizer.py
Purpose: The main processing engine. Watches for new FITS files, 
         injects scientific metadata, and archives them.
"""
import os
import time
import shutil
from astropy.io import fits
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
import astropy.units as u

class Organizer:
    def __init__(self, config):
        self.config = config
        self.source = config['storage']['source_dir']
        self.archive = config['storage']['primary_dir']
        self.obs_code = config['aavso']['observer_code']
        
        # Geolocation for Airmass calculations
        self.location = EarthLocation(
            lat=config['location']['lat'] * u.deg,
            lon=config['location']['lon'] * u.deg,
            height=config['location']['elevation'] * u.m
        )

    def process_new_files(self):
        """Scans the download folder for completed FITS files."""
        if not os.path.exists(self.source):
            return

        for filename in os.listdir(self.source):
            if filename.lower().endswith('.fits'):
                file_path = os.path.join(self.source, filename)
                
                # Atomic check: Ensure the file size is stable (fully written)
                initial_size = os.path.getsize(file_path)
                time.sleep(1.2) # A brief pause to verify
                if initial_size != os.path.getsize(file_path):
                    continue 
                
                self.organize_file(file_path, filename)

    def organize_file(self, file_path, filename):
        """Processes a single FITS file with scientific headers."""
        try:
            with fits.open(file_path, mode='update') as hdul:
                header = hdul[0].header
                
                # Scientific Metadata Injection
                header['OBSERVER'] = self.obs_code
                header['SOFTWARE'] = 'S30-PRO Autonomy v0.9'
                
                # Airmass Calculation (X)
                if 'DATE-OBS' in header and 'OBJCTRA' in header:
                    t = Time(header['DATE-OBS'])
                    coord = SkyCoord(header['OBJCTRA'], header['OBJCTDEC'], unit=(u.hourangle, u.deg))
                    altaz = coord.transform_to(AltAz(obstime=t, location=self.location))
                    # Secant of the zenith angle
                    header['AIRMASS'] = round(altaz.secz.value, 3) if altaz.alt > 0 else 999
                
                header['HISTORY'] = f"Organized and stamped by S30-PRO on {time.ctime()}"
                hdul.flush()

            # Create date-based subdirectory in archive
            date_str = time.strftime("%Y-%m-%d")
            dest_dir = os.path.join(self.archive, date_str)
            os.makedirs(dest_dir, exist_ok=True)
            
            # Final move
            shutil.move(file_path, os.path.join(dest_dir, filename))
            print(f"✅ Stamped and Archived: {filename}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

if __name__ == "__main__":
    print("Organizer engine initialized. Awaiting photons.")
