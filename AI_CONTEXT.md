# AI Project Context - Seestar Photometry Engine

## Current Status (2026-02-24)
- **Environment:** Raspberry Pi 5 (Headless, Debian Bookworm).
- **Core Engine:** Astrometry.net (solve-field) with cached `.wcs` maps.
- **Hardware:** S30-Pro IMX585 (GRBG color matrix, 4.6° Telephoto FOV).
- **Photometry:** Phase 0.9 complete. Engine dynamically debayers FITS based on header DNA, extracts instrumental flux, and calculates ZP against offline AAVSO JSON vaults.

## Technical Snapshot
1. **Analyst:** Uses solve-field --config to handle narrow-field S50/S30 images.
2. **Mapper:** Python logic converts WCS celestial data to Pixel X/Y.
3. **Registry:** Targets are stowed in observable_targets.json (User-managed harvest).

## Immediate Goal
Verify plate-solving on real Seestar photons (NAXIS=2 images) and begin instrumental flux extraction (Aperture Photometry).
