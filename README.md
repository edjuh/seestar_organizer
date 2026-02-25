cat << 'EOF' > ~/seestar_organizer/README.md
# Seestar Organizer

**Automated Variable Star Observation Pipeline**

## 🔭 Project Overview
This project automates the entire lifecycle of variable star observation: from planning and capture to photometry and final AAVSO submission.  Optimized for the **ZWO Seestar S30-pro** and its **IMX585 sensor**. [cite: 2]

## 🏛️ Architecture & The "Golden Bridge"
Because the native Seestar app is a closed ecosystem, this project utilizes `seestar_alp` as a Chief of Staff to handle low-level hardware communication. [cite: 3] To ensure strict stability, the v1.0 Kwetal release enforces a **Modular 3-Block Architecture** based on the Single Responsibility Principle: 

## 🛫 PREFLIGHT (Daytime Operations)
*The hardware is off. The Pi prepares the data.* [cite: 4, 5]
* **Phase 1: Planning & Vetting**
    * **Preflight A (Harvester):** Downloads active campaigns from AAVSO, vetoing targets outside the Seestar's physical FOV constraints. 
    * **Preflight B (Fetcher):** Secures local AAVSO comparison star sequences (`comp_stars/*.json`), verifying reference stars are within the FOV. [cite: 6]
    * **Preflight C (Scheduler):** `nightly_planner.py` scores the surviving targets against tonight's specific ephemeris.  It enforces Lunar avoidance, rewards Westward setting targets, and caps the daily itinerary to the Top 20 targets (`tonights_plan.json`). 
    * **Preflight D (Audit):** Tags 'done' objects until a new observation is required for slow-cadence targets. [cite: 15]

## 🚀 FLIGHT (Nighttime Operations)
*The hardware is active. The pipeline is closed.* [cite: 16]
* **Phase 2: Acquisition**
    * The **Butler (`orchestrator.py`)** verifies the Safety Gate (Weather/Fog) and commands the **Communicator (`alpaca_client.py`)**. [cite: 16]
    * The 1x1 Mosaic payload is injected. The Seestar slews, auto-focuses, and captures raw FITS files without human intervention. [cite: 17]

## 🛬 POSTFLIGHT (Processing & Archiving)
*The telescope slews to the next target. Data is processed asynchronously.* [cite: 18, 19]
* **Phase 3: The Forge (Per-Object)**
    * `sync_manager.py` pulls raw FITS. [cite: 19] Calibration, stacking, and plate-solving are performed via ASTAP. [cite: 20]
    * `photometry_engine.py` extracts flux, cross-references `comp_stars`, and computes V-band magnitude. [cite: 21]
* **Phase 4: The Epilogue (Morning)**
    * The system updates the local Cadence Ledger and formats data for AAVSO WebObs submission. [cite: 22, 23]

## 📜 Slotwoord van een Heer van Stand
"Het is een hele zorg, nietwaar? De sterrenhemel is onmetelijk en de techniek staat voor niets, maar men moet wel de juiste middelen hebben om de zaken in goede banen te leiden. Een heer weet wanneer hij moet delegeren; ik laat het sorteren en organiseren van de opnamen dan ook graag over aan deze voortreffelijke eenvoudige software. Het is, zoals mijn goede vader placht te zeggen, een kwestie van fijn van draad blijven. Mocht u onvolkomenheden aantreffen, schroom dan niet om een ambtelijk schrijven (of een Issue) achter te laten. Maar let wel: wij handelen hier volgens de regelen van het fatsoen!" [cite: 38, 39]
EOF
