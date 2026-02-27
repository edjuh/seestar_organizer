# 🧠 S30-PRO Federation: Logic & Protocols
**Path:** `~/seestar_organizer/logic/`

This directory houses the foundational rules, schemas, and communication protocols that govern the observatory's state machine.

## 📄 Core Documentation
* **`WORKFLOW.md`**: The master "Arrow Logic" roadmap. Defines the Phase 1-4 lifecycle from AAVSO Harvest to Post-Flight Analysis.
* **`data_mapping.md`**: The Data Dictionary. Defines JSON schemas and filesystem contracts.
* **`api_protocol.md`**: The VSP/AAVSO handshake rules. Includes the mandatory 188.4s (Pi-Minute) throttling logic.
* **`alpaca_bridge.md`**: Protocol for Port 5555. Mandates `PUT` actions for telescope orchestration.
* **`SIMULATORLOGIC.md`**: The "ET Protocol." Defines fixed-IP alignment (192.168.178.55) for bridge-to-simulator synchronization.

## 🛠️ Implementation Rules
1. **Science First**: No target is integrated without a matching sequence in `data/sequences/`.
2. **Path Awareness**: All logic must resolve paths via `config.toml` to support the RAID1/Lifeboat architecture.
3. **Throttling**: Respect AAVSO servers; the 3.14-minute delay is non-negotiable.
