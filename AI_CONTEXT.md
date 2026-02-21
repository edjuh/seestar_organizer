# S30-PRO Autonomy : AI Context & Long-Term Memory

**Dear AI:** This file serves as the Long-Term Memory for the Seestar S30-PRO Autonomy project. It contains project lore, architectural rules, solved bugs, and hardware research. Use this to avoid regression and maintain the "Gemini Style" architecture.

## 1. Project Philosophy & Lore
* **The "Tower of Pisa" Rule:** We are not building software to take the 500th pretty picture of the Orion Nebula. The goal is scientific output (AAVSO photometry) and parallel array imaging.
* **Bommelsaga Naming:** * *Joost (v0.8):* The reliable servant (Time-sync, basic loops, atomic files).
  * *Wammes Waggel (v0.9):* First hardware light. Expect chaos and hardware timeouts.
  * *Kwetal (v1.0):* The autonomous mastermind.
  * *Ambtenaar Dorknoper:* "Regels zijn regels." The FITS Organizer module that strictly enforces AAVSO metadata standards.

## 2. Hardware Research & "The Swarm" (v3.0)
* **Current Middleware (`seestar_alp`):** Translates ASCOM Alpaca REST API to ZWO's proprietary WebSocket protocol. 
  * *Known Bug:* Changing IP to `0.0.0.0` in the Alpaca GUI wipes the `[seestars]` config array. Workaround: Keep on `127.0.0.1` or `chmod 444 config.toml`.
* **ZeroConf / mDNS:** Seestars broadcast as `seestar.local`. A swarm utilizes `alpha.local`, `beta.local`, etc.
* **S30-PRO Hardware Specs (Early 2026):**
  * *Sensors:* Dual array. Primary = IMX585 (Deep Sky). Secondary = IMX586 (Wide, 48MP, 63° FOV).
  * *Filters:* Built-in wheel (UV/IR Cut, Duo-band H-alpha/OIII, Dark).
  * *API:* S30-PRO supports **Native ASCOM Alpaca**. We may bypass `seestar_alp` entirely in the future.
  * *Mount:* Native Equatorial (EQ) mode supported, unlocking >10s exposures without field rotation.

## 3. Core Architectural Rules ("Gemini Style")
* **State Snapshot (Decoupled UI):** The UI (Dash) MUST NOT query hardware directly. The `AutonomyEngine` thread maintains a `self._state` dictionary locked via `threading.Lock()`. The UI only reads a deep copy via `get_state()` at 1Hz.
* **Atomic File Operations:** Wait for `st_size` to stabilize over 1-2 seconds before touching FITS files over Wi-Fi to prevent header corruption.
* **Stop-Traps & Safety:**
  * *Weather:* Meteoblue API checks. If `safe == False`, immediately stop slewing/exposing.
  * *Hardware Backoff:* Use exponential backoff (up to 60s) for API timeouts to avoid bricking the Seestar's web server.
  * *Lifeboat Protocol:* If the NAS (`/mnt/astro_nas`) drops, fallback to local SD card storage (`local_buffer`).

## 4. Solved Bugs & Technical Landmines
* **The Sexagesimal Trap:** AAVSO coords often arrive as strings (`21:42:42.8`). Do not blindly use `float()`. Use `astropy.coordinates.SkyCoord` to parse and convert to decimal degrees.
* **Barycentric/Heliocentric Julian Dates:** When using `Time` in `astropy` to calculate BJD/HJD, you *must* pass the observatory's `location=self.location` (EarthLocation), otherwise the calculation fails because it lacks the Earth's rotational position.

## 5. Reference URLs
* AAVSO VPHOT Requirements: [https://www.aavso.org/vphot](https://www.aavso.org/vphot)
* ASCOM Alpaca API Reference: [https://ascom-standards.org/api/](https://ascom-standards.org/api/)
* Simple Seestar Controller (SSC) / Swarm concepts: [https://github.com/smart-telescope/seestar_alp](https://github.com/smart-telescope/seestar_alp)

## 6. Workflow & Output Generation
* **The Heredoc Method:** When providing code updates to the user, ALWAYS use the `cat << 'EOF' > filename` (or `>>` for appending) method. This allows the user to safely copy and paste the entire block into their SSH terminal without wrestling with `vim` or clipboard formatting errors.
* **Code Context:** Do not store full source code in this memory file. Instead, ask the user to provide the current file state if needed, and rely on your knowledge of the "Gemini Style" architecture.

## The Golden Rules of Engagement:
7. **Never Assume:** If a state, hardware condition, or environment variable is unknown, ASK or run a discovery script. Verify with the user when in doubt. 
8. **Tooling:** Exclusively use `vim` for interactive edits and `heredoc` (`cat << 'EOF'`) for code deployment. Do not suggest `nano` or GUI tools.
9. **No Ghost Code:** Do not generate code that relies on unverified assumptions about the AAVSO REDA campaign data structure or the Seestar S30-PRO's Alpaca bridging capabilities.
