# SeeStar Simulator & ALP Bridge Logic (The ET Protocol)

This document outlines the networking and state logic required to synchronize the SeeStar ALP Bridge with the SeeStar Simulator on a Raspberry Pi environment.

## 🔍 1. The Core Conflict
By default, the Bridge and Simulator were locked in a "Loopback Prison." The Bridge searched for a hostname (`seestar.local`) that didn't resolve, while the Simulator listened only on a local address (`127.0.0.1`) invisible to the Bridge's network threads.

## ⚙️ 2. Networking Logic
To establish a stable "Federation," we moved from dynamic discovery to **Fixed IP Alignment**.

### Binding Strategy
* **Simulator Bind**: The Simulator is forced to listen on `0.0.0.0` (all interfaces). This allows it to receive UDP broadcasts and TCP commands from the Bridge regardless of whether they originate from `127.0.0.1` or the physical IP `192.168.178.55`.
* **Bridge Targeting**: The Bridge `config.toml` was updated to point directly to the physical IP `192.168.178.55`. This bypasses mDNS/DNS failures associated with `seestar.local`.

## 🛰️ 3. State & Location Logic (The Bouncer)
The ALP Bridge implements a "Presence-First" requirement. It acts as a "Bouncer," rejecting any configuration commands if a live socket connection to a telescope is not detected.

### Location Injection Method
1.  **Handshake**: A `PUT` request to `/connected` is sent to flip the internal state to `true`.
2.  **Memory Overwrite**: While the connection is live, `SiteLatitude` and `SiteLongitude` are injected via the Alpaca API.
3.  **Synchronization**: The Simulator's internal state was manually patched to match the Haarlem coordinates (52.3874, 4.6462) to ensure Mosaic math and Sidereal Time are accurate.

## 📋 4. Verified Capabilities
As of 2026-02-26, the following features are operational:
* **Device Status**: Reporting as Seestar S50, Firmware 4.70, EQ Mode.
* **Vitals**: 100% Battery, 49.2 GB Free Storage.
* **Scheduler**: Successfully processing Mosaic JSON templates for targets like `polaris` and `CH Cyg`.

## 🚀 5. Automation Hook
Future scripts (like GPS autonomy) should use the following API sequence:
`CONNECT` -> `SET LAT` -> `SET LON` -> `VERIFY LST`
