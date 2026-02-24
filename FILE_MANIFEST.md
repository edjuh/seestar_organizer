# Seestar Organizer: File Manifest (Phase 1.0 - Kwetal)

## 🏗️ Core Engine
* `core/orchestrator.py`: Central logic.
* `core/alpaca_client.py`: Handshake with Federation (Port 5432).
* `core/selector.py`: Westward-priority target selection.
* `main.py`: The root entry point for the Sentry.

## 🧪 Sentry & Tests
* `seestar_sentry.service`: The systemd daemon configuration.
* `tests/test_night_plan.py`: Forecasts the "Westward" setting priority.
* `tests/test_selector.py`: Audits the vault for 390+ JSONs.

## 📚 Data & Utils
* `data/sequences/`: The 390+ target vault.
* `utils/fetch_sequences.py`: AAVSO scraper.
