"""
Objective: Instrumental flux extraction and science-grade lightcurve generation.
"""
"""
Filename: core/photometry_engine.py
"""
import numpy as np
from scipy.ndimage import convolve
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
from photutils.centroids import centroid_com
from photutils.aperture import CircularAperture, CircularAnnulus, aperture_photometry
from core.logger import log_event

class PhotometryEngine:
    # TUNED FOR IMX585 / S30-PRO Geometry
    def __init__(self, aperture_radius=4.0, sky_in=15.0, sky_out=22.0):
        self.r_ap = aperture_radius
        self.r_in = sky_in
        self.r_out = sky_out

    def extract_flux(self, fits_path, x_init, y_init):
        try:
            with fits.open(fits_path) as hdul:
                data = None
                for hdu in hdul:
                    if hdu.data is not None and hdu.data.ndim >= 2:
                        if hdu.data.ndim == 3:
                            data = np.mean(hdu.data, axis=0)
                            log_event("PhotometryEngine: 3D Array detected. Averaging to 2D Mono.")
                        else:
                            raw_data = hdu.data.astype(np.float32)
                            bayer_pat = hdu.header.get('BAYERPAT', '').strip().upper()
                            
                            if bayer_pat == 'GRBG':
                                log_event("PhotometryEngine: GRBG Bayer detected. Isolating V-Band (Green).")
                                g_mask = np.zeros_like(raw_data, dtype=np.float32)
                                g_mask[0::2, 0::2] = 1.0
                                g_mask[1::2, 1::2] = 1.0
                                g_pixels = raw_data * g_mask
                                kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=np.float32) / 4.0
                                g_interpolated = convolve(g_pixels, kernel)
                                data = g_pixels + g_interpolated * (1.0 - g_mask)
                                
                            elif bayer_pat == 'RGGB':
                                log_event("PhotometryEngine: RGGB Bayer detected. Isolating V-Band (Green).")
                                g_mask = np.zeros_like(raw_data, dtype=np.float32)
                                g_mask[0::2, 1::2] = 1.0
                                g_mask[1::2, 0::2] = 1.0
                                g_pixels = raw_data * g_mask
                                kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=np.float32) / 4.0
                                g_interpolated = convolve(g_pixels, kernel)
                                data = g_pixels + g_interpolated * (1.0 - g_mask)
                                
                            else:
                                # The "Ghost File" Fallback
                                log_event(f"PhotometryEngine: BAYERPAT '{bayer_pat}' missing/unknown. Assuming Mono.")
                                data = raw_data
                        break
                
                if data is None:
                    return None

                height, width = data.shape
                box_size = 15
                margin = self.r_out + 2
                
                if not (margin < x_init < width - margin and margin < y_init < height - margin):
                    return None

                half_box = box_size // 2
                x_min = max(0, int(x_init) - half_box)
                x_max = min(width, int(x_init) + half_box + 1)
                y_min = max(0, int(y_init) - half_box)
                y_max = min(height, int(y_init) + half_box + 1)
                
                cutout = data[y_min:y_max, x_min:x_max]
                
                xc_cutout, yc_cutout = centroid_com(cutout)
                x_refined = x_min + xc_cutout
                y_refined = y_min + yc_cutout
                
                pos = (x_refined, y_refined)
                aperture = CircularAperture(pos, r=self.r_ap)
                annulus = CircularAnnulus(pos, r_in=self.r_in, r_out=self.r_out)
                
                annulus_masks = annulus.to_mask(method='center')
                annulus_data = annulus_masks.multiply(data)
                annulus_data_1d = annulus_data[annulus_masks.data > 0]
                
                _, sky_median, _ = sigma_clipped_stats(annulus_data_1d, sigma=3.0)
                
                phot_table = aperture_photometry(data, aperture)
                raw_flux = phot_table['aperture_sum'][0]
                
                bkg_sum = sky_median * aperture.area
                instrumental_flux = raw_flux - bkg_sum
                
                return {
                    "x_ref": x_refined,
                    "y_ref": y_refined,
                    "raw_flux": raw_flux,
                    "sky_bkg": sky_median,
                    "inst_flux": instrumental_flux
                }
                
        except Exception as e:
            log_event(f"PhotometryEngine: Failed to extract flux: {e}", level="error")
            return None

phot_engine = PhotometryEngine()
