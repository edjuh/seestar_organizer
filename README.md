# S30-PRO Autonomy Pilot

An autonomous, offline-first observation orchestrator for variable star photometry. Designed to run on a Raspberry Pi 5, commanding a Seestar S30/S50 via the Alpaca protocol.

## Core Philosophy
1. **Hardware-First:** If the GPS or persistent storage are down, the system halts.
2. **Offline-Tolerant:** The autonomy loop does not rely on live internet. Targets and sequences are cached locally.
3. **Polite Scraping:** AAVSO servers are queried slowly and respectfully during daytime syncs.

## Photometry Parameters (S30-PRO)
The Seestar S30-PRO has physical limits. This orchestrator is designed around the "Sweet Spot" of 30mm optics:

* **Mount Limits (Exposure Times):**
  * `Alt/Az Mode`: Max 10s exposures. Field rotation limits us to brighter targets (Mag ~5.0 to ~11.0).
  * `EQ Mode` (Hardware Wedge): Max 30-60s exposures. Unlocks fainter targets (Mag ~13.0).
* **Target Classes:** We strictly filter the AAVSO target list for slow-changing, bright variables:
  * **M** (Miras)
  * **SR** (Semi-Regulars)
  * **ZAND** (Symbiotics)
  * **CEP / DCEP** (Cepheids)
* **Debayering Strategy (The V-Band Proxy):** The S30-PRO uses a One-Shot Color (OSC) CMOS sensor with an RGGB Bayer matrix. To match professional Johnson V-Band photometry, we extract only the Green channels (G1/G2), discarding Red and Blue pixels entirely.

## Architecture
* **Environment:** Debian Bookworm (64-bit), Python 3.13.5
* **Timekeeping:** Stratum 2 local chrony synced via `gpsd` (SHM).
* **Target Data:** AAVSO TargetTool & VSP API - Cached to local JSON.
