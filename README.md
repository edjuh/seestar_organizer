# S30-PRO Autonomy Pilot

An autonomous, offline-first observation orchestrator for variable star photometry. Designed to run on a Raspberry Pi 5, commanding a Seestar S50/S30 via the Alpaca protocol.

## Core Philosophy
1. **Hardware-First:** If the GPS (`gpsd` at `/dev/ttyACM0`) or persistent storage (`fstab` mounts) are down, the system halts. No silent failures.
2. **Offline-Tolerant:** The autonomy loop (`The Brain`) does not rely on live internet. Target sequences and comparison stars are ingested during the day and cached locally.
3. **No API Keys in Git:** All secrets live in a `.env` file; system configurations live in `config.toml`.

## Architecture
* **Environment:** Debian Bookworm (64-bit), Python 3.13.5
* **Sensors:** Local GPS module (time/location), Open-Meteo API (keyless weather fallback).
* **Target Data:** AAVSO TargetTool (Basic Auth) - Cached to local JSON.
* **Control:** `seestar_alp` Alpaca Bridge wrapper.
* **Storage:** Local NVMe/USB (`/mnt/data_ssd`) for fast FITS buffering; NAS (`/mnt/astronas`) for archival.
