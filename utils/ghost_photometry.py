#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: utils/ghost_photometry.py
Version: 1.2.0 (Pee Pastinakel)
Objective: Diagnostic tool for identifying internal reflection artifacts and calculating system zero-points using reference comparison stars.
"""

import os
import json
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from photutils.aperture import SkyCircularAperture, aperture_photometry

SAMPLE_DIR = os.path.expanduser("~/seestar_organizer/tests/samples")
COMP_DIR = os.path.expanduser("~/seestar_organizer/data/comp_stars")
TEMP_DIR = os.path.join(SAMPLE_DIR, "solve_temp")

def run_ghost_math(fits_name, comp_json_name):
    img_path = os.path.join(SAMPLE_DIR, fits_name)
    wcs_path = os.path.join(TEMP_DIR, fits_name.replace(".fits", ".wcs"))
    comp_path = os.path.join(COMP_DIR, comp_json_name)

    if not os.path.exists(wcs_path) or not os.path.exists(comp_path):
        print(f"❌ Missing files for {fits_name}. Check solve or comp_stars folder.")
        return

    try:
        data = fits.getdata(img_path)
        w = WCS(fits.getheader(wcs_path))
        with open(comp_path, 'r') as f:
            comp_data = json.load(f)

        print(f"📊 Analyzing {fits_name} using {comp_json_name}...")

        offsets = []
        for star in comp_data.get('comp_stars', [])[:3]:
            ra, dec = star['ra'], star['dec']
            ref_mag = star['v_mag']
            
            aperture = SkyCircularAperture([[ra, dec]], r=0.005)
            phot = aperture_photometry(data, aperture, wcs=w)
            flux = phot['aperture_sum']
            
            if flux > 0:
                inst_mag = -2.5 * np.log10(flux)
                zp = ref_mag - inst_mag
                offsets.append(zp)
                print(f"   ✨ Comp Star ({star['label']}): Inst {round(inst_mag,2)} | Ref {ref_mag} | ZP {round(zp,2)}")

        if offsets:
            avg_zp = np.mean(offsets)
            print(f"✅ Calculated System Zero-Point: {round(avg_zp, 2)}")
        else:
            print("⚠️ No valid flux found for comparison stars.")

    except Exception as e:
        print(f"❌ Ghost Math Error: {e}")

if __name__ == "__main__":
    run_ghost_math("rr_lyrae.fits", "RR_Lyr.json")
