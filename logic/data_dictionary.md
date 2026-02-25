# 🗂️ S30-PRO Data Dictionary (v1.0 Kwetal)

This document defines the strict schema and purpose of every file in the `data/` directory to prevent corruption by automated cron jobs or future logic scripts.

## 📂 The Master Files (Phase 1: Planning)

### `targets.json`
* **Purpose:** The Master AAVSO Target Library. Updated monthly by `core/librarian.py` or `utils/harvest_aavso.py`. 
* **Schema Contract:**
  * `star_name` (String): The AAVSO target name (e.g., "CH Cyg").
  * `ra` (Float): Right Ascension in **Decimal Degrees**.
  * `dec` (Float): Declination in **Decimal Degrees**.
  * `filter` (String): Preferred photometric filter (e.g., "B", "V").
  * `priority` (Boolean/Int): Determines observation urgency.

### `tonights_plan.json`
* **Purpose:** The Daily Itinerary. Overwritten every afternoon by `core/nightly_planner.py`. Read exclusively by `core/orchestrator.py` (The Butler).
* **Schema Contract:**
  * `date` (String): YYYY-MM-DD UTC.
  * `targets` (Array): Filtered list of targets that pass the horizon veto. 
  * *Note: The planner converts Decimal Degree RA into Decimal Hours (0-24) to satisfy the Seestar Alpaca API requirements.*

## 📂 The Reference Files (Phase 3: Photometry)

### `comp_stars/` (Directory)
* **Purpose:** Contains individual JSON files (e.g., `ch_cyg.json`) detailing the AAVSO comparison star sequences for specific variables. 
* **Usage:** Read *only* by `core/photometry_engine.py` during image processing to calculate the variable's magnitude. It is NEVER read by the telescope acquisition loop.

## 📂 The Operational Files (Hardware & Logs)

### `local_buffer/` (Directory)
* **Purpose:** The "Lifeboat." Temporary holding area for raw `.fits` files pulled from the Seestar by `core/sync_manager.py` before they are processed and shipped to the NAS.
