# Seestar Organizer Roadmap - Feb 2026

## 🟢 v0.7: The Librarian (Status: Operational)
- [x] AAVSO API integration and harvest logic.
- [x] Sequence and comparison star cataloging.
- [x] Local JSON vault for observation targets.

## 🟡 v0.8: The Sighted Analyst (Status: In Progress)
- [x] Native ARM64 Plate-solver (Astrometry.net) installed.
- [x] V17 Photometry Database (.290 files) inflated and indexed.
- [x] Coordinate mapping logic (Celestial -> Pixel) established.
- [ ] **NEXT:** Header injection for "Hinted" solving (Guaranteed Solve).
- [ ] **NEXT:** Batch solve utility for Seestar FITS directories.

## ⚪ v0.9: The Aperture Grip (Status: Pending)
- [ ] Centroid detection for sub-pixel accuracy.
- [ ] Background-subtracted flux extraction (Aperture Photometry).
- [ ] Comparison star magnitude lookup via local V17 DB.

## ⚪ v1.0: The Photometrist (Status: Pending)
- [ ] Differential magnitude calculation logic.
- [ ] Light curve generator (.csv / .png).
- [ ] Automated reporting for AAVSO submissions.
