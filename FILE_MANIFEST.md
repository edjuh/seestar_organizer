# Seestar Organizer: File Manifest (Phase 1.1)

## 🏗️ Core Engine
* `core/analyst.py`: Plate-solver wrapper.
* `core/master_analyst.py`: RA/Dec to Pixel bridge.
* `core/pixel_mapper.py`: WCS transformation logic.
* `core/vault_manager.py`: TOML-driven librarian/altitude gatekeeper.
* `core/planner.py`: Solar ephemeris & darkness window calculator.
* `core/sequence_engine.py`: Nightly prioritize & mission planner.
* `core/logger.py`: Centralized logging.

## 🧪 Tests (The Lab)
* `tests/samples/`: Golden Four FITS samples.
* `tests/test_bridge.py`: Solver functional test.
* `tests/test_golden_four.py`: Batch validation sweep (100% success).
* `tests/test_vault.py`: Real-time altitude check.
* `tests/test_mission_control.py`: Priority briefing logic.
* `tests/test_future_plan.py`: Future date solar calculations.

## ⚙️ Configuration
* `config.toml`: System-wide settings (Station, Solver, Paths).
