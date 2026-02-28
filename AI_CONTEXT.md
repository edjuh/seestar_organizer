cat << 'EOF' > ~/seestar_organizer/AI_CONTEXT.md
# AI Project Context - Seestar Photometry Engine (Rommeldam Edition)

> **Objective:** Provides definitive architectural rules, environment snapshots, and logic constraints for AI-assisted development of the Seestar Federation.
> **Version:** 1.2.0 (Garmt)

## 🏰 Architectural Logic & Current Status
- **v1.2 Garmt (Current):** Unified PEP 257 standardization across all core scripts.
- **v0.5 Hiep Hieper (The Orchestrator):** Manages the "Golden Bridge" between AAVSO JSON vaults and the Alpaca client.
- **v0.9 Terpen Tijn:** "Het is prut!" Implements the "Aperture Grip"—handling western priority, sub-pixel centroiding logic, and enforcing a >30° altitude floor for science-grade photons.
- **Environment:** Raspberry Pi 5 (Headless, Debian Bookworm).
- **Hardware:** S30-Pro IMX585 (GRBG color matrix, 4.6° Telephoto FOV).

## 🏰 The "Garmt" Header Standard
Every `.py` file MUST start with a unified PEP 257 docstring containing:
1. **Filename:** Explicit path tracking.
2. **Version:** Current project epoch (1.2.0 Garmt).
3. **Objective:** A single-sentence declaration of responsibility.

## 🛠️ Technical Snapshot
1. **Analyst:** Plate-solver (Astrometry.net) configured for narrow-field Seestar optics.
2. **Mapper:** Python WCS-to-Pixel bridge for instrumental flux extraction.
3. **Registry:** `data/sequences/` contains 390+ AAVSO targets.

## 🛰️ Seestar Federation Alpaca Handshake
- **Endpoint:** `http://127.0.0.1:5432/0/schedule`
- **Device Index:** `/0/`
- **Method:** `POST` with unique `schedule_item_id` (UUID4).

| Source Field (AAVSO JSON) | Target Field (Alpaca) | Logic |
| :--- | :--- | :--- |
| `auid` or `comments` | `target_name` | Primary: `auid`; Fallback: `comments`. |
| `ra` ("HH:MM:SS") | `ra` | Must use `unit=(u.hourangle, u.deg)`. |
| `dec` ("DD:MM:SS") | `dec` | Preserved colon-string for parser. |
| N/A | `is_j2000` | Always `True`. |
| N/A | `panel_time_sec` | Standardized to `60`s for variable stars. |

## 🧪 Critical Handshake Logic
- **List-Wrapped:** AAVSO files are `raw_json`.
- **Simulation:** `SIMULATION_MODE=True` bypasses weather/sun but maintains real-time Alt/Az calculation.
- **Westward Priority:** Objects in Azimuth 180-350 with low altitude take priority to ensure capture before setting.

## 🏮 The "Aperture Grip" (Terpen Tijn Logic)
- **Westward Priority:** To avoid losing targets to the horizon, the Selector prioritizes objects with Azimuth 180°-350°.
- **Priority Score:** $(100 - Altitude)$ for Western targets; $(Altitude / 2)$ for Eastern/Zenith targets.
- **Handshake Name:** Always use `target['display_name']` to avoid `None` errors in the Alpaca bridge.

