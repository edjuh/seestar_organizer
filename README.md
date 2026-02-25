# Seestar Organizer

**Automated Variable Star Observation Pipeline**

## 🔭 Project Overview
This project automates the entire lifecycle of variable star observation: from planning and capture to photometry and final AAVSO submission. Optimized for the **ZWO Seestar S30-pro** and its **IMX585 sensor**.

## 🏛️ Architecture & The "Golden Bridge"
Because the native Seestar app is a closed ecosystem, this project utilizes `seestar_alp` as a Chief of Staff to handle low-level hardware communication. 

To ensure strict stability, the v1.0 Kwetal release enforces a **Modular 3-Block Architecture** based on the Single Responsibility Principle:

## 🛫 PREFLIGHT (Daytime Operations)
*The hardware is off. The Pi prepares the data.*
* **Phase 1: Planning & Vetting**
    * **Preflight A (Harvester):** Downloads active campaigns from AAVSO, vetoing targets outside the Seestar's physical FOV constraints.
    * **Preflight B (Fetcher):** Secures local AAVSO comparison star sequences (`comp_stars/*.json`), verifying reference stars are within the FOV.
    * **Preflight C (Scheduler):** `nightly_planner.py` scores the surviving targets against tonight's specific ephemeris. It enforces Lunar avoidance, rewards Westward setting targets, and caps the daily itinerary to the Top 20 targets (`tonights_plan.json`).

### 🚀 FLIGHT (Nighttime Operations)
*The hardware is active. The pipeline is closed.*
* **Phase 2: Acquisition**
    * The **Butler (`orchestrator.py`)** verifies the Safety Gate (Weather/Fog) and commands the **Communicator (`alpaca_client.py`)**.
    * The 1x1 Mosaic payload is injected. The Seestar slews, auto-focuses, and captures raw FITS files without human intervention.

### 🛬 POSTFLIGHT (Processing & Archiving)
*The telescope slews to the next target. Data is processed asynchronously.*
* **Phase 3: The Forge (Per-Object)**
    * `sync_manager.py` pulls the raw FITS.
    * The pipeline calibrates (darks/bias), aligns, stacks, and plate-solves the master image.
    * `photometry_engine.py` extracts the instrumental flux, cross-references the `comp_stars` JSON, and computes the scientific V-band magnitude.
* **Phase 4: The Epilogue (Morning)**
    * The system updates the local Cadence Ledger to prevent over-observing the same targets.
    * Extracted photometry is formatted for AAVSO WebObs submission.

### 1. The Communicator (Block 1)
The exclusive bridge to the hardware API. It translates Python method calls into API endpoints and manages connection states. It makes zero operational decisions and is the *only* component permitted to send HTTP GET/PUT requests to the telescope.

### 2. The Brain (Block 2)
The Python Orchestrator lives here and executes the master loop:
1. **Sensor Check:** Polls OpenWeatherMap and GPS APIs. If unsafe, it waits.
2. **Target Acquisition:** Scans a deduplicated, offline JSON database of AAVSO targets.
3. **The 1x1 Mosaic Trick:** Formats targets into a mock `1x1 Mosaic` JSON payload to bypass Alpaca sequence limitations.
4. **Federation Injection:** Payload is POSTed directly to the `seestar_alp` Federation Controller (Device 0).
5. **Autonomous Execution:** Orchestrator fires an HTMX toggle to initiate autofocus and scientific exposure.

### 3. The Watchdog (Block 3)
A passive telemetry dashboard for the terminal. "Look, but do not touch." It requests current state data from the Communicator and reads the Orchestrator's logs to generate a UI. It is strictly forbidden from forcing coordinates or triggering connections.

## 📂 Project Structure
* `api/` - The Communicator (Hardware Abstraction Layer).
* `core/` - Long-running engines (Orchestrator, Harvester, Sensor APIs).
* `scripts/` - Passive telemetry and dashboarding (Watchdogs).
* `utils/` - Human-triggered CLI scripts (AAVSO Scraper, Math converters).
* `data/` - Offline JSON caches for targets, weather states, and sequence lists.

## 🏗️ Hardware & Software
- **Hardware:** RPi5 (Bookworm), GPS Module, ZWO Seestar S30-pro.
- **Software:** Seestar ALP, Python 3.13, ASTAP.

## 📜 Slotwoord van een Heer van Stand
"Het is een hele zorg, nietwaar? De sterrenhemel is onmetelijk en de techniek staat voor niets, maar men moet wel de juiste middelen hebben om de zaken in goede banen te leiden. Een heer weet wanneer hij moet delegeren; ik laat het sorteren en organiseren van de opnamen dan ook graag over aan deze voortreffelijke eenvoudige software. Het is, zoals mijn goede vader placht te zeggen, een kwestie van fijn van draad blijven. Mocht u onvolkomenheden aantreffen, schroom dan niet om een ambtelijk schrijven (of een Issue) achter te laten. Maar let wel: wij handelen hier volgens de regelen van het fatsoen!"
