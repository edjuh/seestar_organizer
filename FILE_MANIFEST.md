# Seestar Organizer: File Manifest (Phase 1.4)

## 🏗️ Core Engine (The Brain & Muscle)
* `core/orchestrator.py`: The central logic handler (linked to main.py).
* `core/alpaca_client.py`: The bridge to Seestar Federation (Port 5432).
* `core/weather.py` & `core/fog_monitor.py`: Real-time safety sensors.
* `core/ephemeris.py`: Solar/Lunar/Target position calculator.
* `core/selector.py`: Logic for picking the "Zenith King" from the vault.
* `core/hardware_profiles.py`: Specs for S30, S30 Pro, and S50.
* `core/horizon.py`: Custom Az/Alt obstruction mapping.
* `core/photometry_engine.py`: Science-grade light curve analysis logic.
* `core/analyst.py` & `core/master_analyst.py`: Plate-solving and coordinate verification.

## 📚 Data Management (The Librarian)
* `core/librarian.py`: Handles AAVSO delta-fetching and local storage.
* `core/sequence_repository.py`: Manages the 392+ JSON observation templates.
* `core/vault_manager.py`: Legacy altitude gatekeeper (integrated into Selector).
* `core/sync_manager.py`: Keeps local data in sync with remote catalogs.

## 🧪 Tests & Simulation
* `tests/virtual_seestar.py`: A local mock for testing without a real telescope.
* `tests/test_sight.py`: Verifies astronomical math.
* `tests/test_weather.py`: Simulates rain/cloud events.
* `tests/test_selector.py`: Audits the vault for winning targets.

## 🛠️ Utilities
* `utils/fetch_sequences.py`: The manual pull tool for AAVSO targets.
* `utils/verify_library.py`: Checks for corrupted or empty JSON targets.
* `utils/astro.py`: Low-level coordinate conversion helpers.
