# AI Project Context - Seestar Photometry Engine

## Current Status (2026-02-23)
- **Environment:** Raspberry Pi 5 (Headless, Debian Bookworm).
- **Core Engine:** Astrometry.net (solve-field) with local indices (4208-4211).
- **Database:** V17 Johnson-V Photometry catalog installed in ~/.astap.
- **Hardware:** No active Seestar connection; currently testing via harvested FITS files.

## Technical Snapshot
1. **Analyst:** Uses solve-field --config to handle narrow-field S50/S30 images.
2. **Mapper:** Python logic converts WCS celestial data to Pixel X/Y.
3. **Registry:** Targets are stowed in observable_targets.json (User-managed harvest).

## Immediate Goal
Verify plate-solving on real Seestar photons (NAXIS=2 images) and begin instrumental flux extraction (Aperture Photometry).
