# 🗂️ S30-PRO Data Dictionary

> **Objective:** Defines the strict schema and purpose of every file in the data/ directory to prevent corruption.
> **Version:** 1.2.0 (Garmt)

## 📂 The Master Files (Phase 1: Planning)
### `targets.json`
* **Purpose:** The Master AAVSO Target Library. Updated monthly.
* **Schema Contract:** `star_name`, `ra` (Decimal Deg), `dec` (Decimal Deg), `filter`, `priority`.

### `tonights_plan.json`
* **Purpose:** The Daily Itinerary. Read exclusively by `core/orchestrator.py`.
* **Schema Contract:** `date` (YYYY-MM-DD), `targets` (Filtered array).

## 📂 The Reference Files (Phase 3: Photometry)
### `comp_stars/` (Directory)
* **Purpose:** Contains AAVSO comparison star sequences for specific variables.
* **Usage:** Read *only* by `core/photometry_engine.py`. NEVER read by the telescope acquisition loop.

## 📂 The Operational Files (Hardware & Logs)
### `local_buffer/` (Directory)
* **Purpose:** The "Lifeboat" temporary holding area for raw `.fits` files.
