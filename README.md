cat << 'EOF' > ~/seestar_organizer/README.md
# Seestar Organizer

> **Objective:** Primary documentation for the automated variable star observation pipeline, outlining the Modular 3-Block Architecture and Single Responsibility Principle.
> **Version:** 1.2.0 (Garmt)

**Automated Variable Star Observation Pipeline**

## 🔭 Project Overview
This project automates the entire lifecycle of variable star observation: from planning and capture to photometry and final AAVSO submission. Optimized for the **ZWO Seestar S30-pro** and its **IMX585 sensor**.

## 🏰 Architecture & The "Golden Bridge"
Because the native Seestar app is a closed ecosystem, this project utilizes `seestar_alp` as a Chief of Staff to handle low-level hardware communication. To ensure strict stability, the v1.2 Garmt release enforces a **Modular 3-Block Architecture** based on the Single Responsibility Principle:

## 🛫 PREFLIGHT (Daytime Operations)
*The hardware is off. The Pi prepares the data.*
* **Phase 1: Planning & Vetting**
    * **Preflight A (Harvester):** Downloads active campaigns from AAVSO, vetoing targets outside the Seestar's physical FOV constraints.
    * **Preflight B (Fetcher):** Secures local AAVSO comparison star sequences (`comp_stars/*.json`), verifying reference stars are within the FOV.
    * **Preflight C (Scheduler):** `nightly_planner.py` scores the surviving targets against tonight's specific ephemeris. It enforces Lunar avoidance, rewards Westward setting targets, and caps the daily itinerary to the Top 20 targets (`tonights_plan.json`).
    * **Preflight D (Audit):** Tags 'done' objects until a new observation is required for slow-cadence targets.

## 🚀 FLIGHT (Nighttime Operations)
*The hardware is active. The pipeline is closed.*
* **Phase 2: Acquisition**
    * The **Butler (`orchestrator.py`)** verifies the Safety Gate (Weather/Fog) and commands the **Communicator (`alpaca_client.py`)**.
    * The 1x1 Mosaic payload is injected. The Seestar slews, auto-focuses, and captures raw FITS files without human intervention.

## 🧪 POSTFLIGHT (Processing & Archiving)
*The telescope slews to the next target. Data is processed asynchronously.*
* **Phase 3: The Forge (Per-Object)**
    * `sync_manager.py` pulls raw FITS. Calibration, stacking, and plate-solving are performed via ASTAP.
    * `photometry_engine.py` extracts flux, cross-references `comp_stars`, and computes V-band magnitude.
* **Phase 4: The Epilogue (Morning)**
    * The system updates the local Cadence Ledger and formats data for AAVSO WebObs submission.

## 🍷 Slotwoord van een Heer van Stand
"Het is een hele zorg, nietwaar? De sterrenhemel is onmetelijk en de techniek staat voor niets, maar men moet wel de juiste middelen hebben om de zaken in goede banen te leiden. Een heer weet wanneer hij moet delegeren; ik laat het sorteren en organiseren van de opnamen dan ook graag over aan deze voortreffelijke eenvoudige software. Het is, zoals mijn goede vader placht te zeggen, een kwestie van fijn van draad blijven. Mocht u onvolkomenheden aantreffen, schroom dan niet om een ambtelijk schrijven (of een Issue) achter te laten. Maar let wel: wij handelen hier volgens de regelen van het fatsoen!"
