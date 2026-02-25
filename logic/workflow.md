# 🌌 S30-PRO Master Workflow (v1.0 Kwetal)

This document defines the chronological, end-to-end lifecycle of the observatory. It dictates exactly what the Orchestrator, the Hardware, and the Processing Engine must do every single night.

## PHASE 1: 🌅 The Prelude (Daytime Planning)
*Executed daily by cron or manual trigger before sunset.*
1. **Target Refresh:** `librarian.py` checks AAVSO for new alerts or priority changes.
2. **The Filter:** `nightly_planner.py` evaluates the master target list against tonight's Haarlem ephemeris (altitude > 30°, Moon avoidance) and horizon vetoes.
3. **The Manifest:** Generates `data/tonights_plan.json`.

## PHASE 2: 🔭 The Acquisition (Nighttime Ops - Per Object)
*Executed by the Butler (`orchestrator.py`) and Block 1 (`alpaca_client.py`).*
1. **Safety Gate:** Verify clear skies (Fog/IR monitor) and dark horizon (Sun < -18°).
2. **Slew & Center:** Butler injects the "1x1 Mosaic Payload" for the first target. Bridge commands telescope to slew, plate-solve, and center.
3. **Autofocus:** Telescope calibrates focus for the current temperature.
4. **Integration:** Telescope captures $X exposures of $Y seconds.
5. **Sync:** `sync_manager.py` pulls the raw `.fits` and `.fit` files to the local Pi buffer.



## PHASE 3: 💻 The Processing Forge (Per Object Data Pipeline)
*Triggered immediately after Phase 2 completes for an object, while the telescope slews to the next target.*
1. **Calibration:** Apply Master Darks and Master Bias to the raw FITS to remove sensor noise and thermal glow.
2. **Debayering:** Convert the monochrome raw sensor data into color (or extract the specific Green/V-band channel for photometry).
3. **Registration:** Align the calibrated frames perfectly based on star centroids.
4. **Stacking:** Combine the aligned frames into a single high-SNR Master FITS file.
5. **Astrometry:** Plate-solve the Master FITS (via ASTAP or local index) to inject precise WCS (World Coordinate System) headers.
6. **Sequence Matching:** Load the AAVSO comparison star JSON (`data/sequences/`) for this specific target.
7. **Photometry:** `photometry_engine.py` maps the comp star RA/Dec to pixel X/Y. It measures instrumental flux for the variable and the comp stars, computing the standard V-band magnitude.
8. **Archiving:** Move the final Master FITS, the photometry log, and the raw subs to the NAS `/mnt/astronas/`.
9. **Garbage Collection:** Delete the intermediate unstacked/debayered files from the Pi's SD card to prevent out-of-memory errors.
10. **AAVSO Formatting:** Append the computed magnitude and error margin to a staging file formatted to the AAVSO Extended File Format.

## PHASE 4: 📝 The Epilogue (End of Night)
*Executed at Astronomical Dawn, or when clouds abort the session.*
1. **Park:** Telescope is commanded to sleep/park.
2. **Log Cooldown:** Objects successfully observed are logged so they are skipped for the next $time.period (e.g., don't shoot a 300-day Mirid every single night).
3. **Report:** Dashboard/Notifier sends a Telegram or terminal summary: *"Night complete. 12 targets observed. 1440 frames stacked. 12 AAVSO reports staged."*
