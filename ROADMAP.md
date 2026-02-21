# S30-PRO Roadmap (The Bommel Saga)

- [x] **v0.0 [Beunhaas]: The Raw Foundation**
  - Verified `/dev/ttyACM0` streams NMEA via `gpsd`.
  - Verified persistent storage via `fstab` (USB & NAS).
  - Switched from Meteoblue to keyless Open-Meteo.
  - Authenticated AAVSO TargetTool API via Basic Auth.
  
- [ ] **v0.1 [Brigadier Snuf]: Hardware Abstraction**
  - Implement thread-safe `GPSSensor` to poll `gpsd` socket.
  - Implement `WeatherStation` for Open-Meteo conditions.
  - Establish `config.toml` and `.env` unified loader.

- [ ] **v0.2 [Zedekia Zwederkoorn]: Data Ingestion (The Airgap)**
  - Build `AAVSOClient` to fetch REDA targets and comparison sequences.
  - Build `SequenceCache` to store JSON data locally for offline night-time ops.

- [ ] **v0.3 [Joris Goedbloed]: The Alpaca Bridge**
  - Integrate `seestar_alp`.
  - Build/configure the "Virtual Seestar" mock to prevent `KeyError: 0` bridge crashes.

- [ ] **v0.4 [Zachtzalver]: Target Acquisition & Command**
  - Filter cached targets by current GPS altitude and Open-Meteo cloud cover.
  - Send Slew/Sync commands to the Alpaca bridge.

- [ ] **v0.5 [Hiep Hieper]: The Orchestrator**
  - The headless autonomy loop: Check Weather -> Pick Target -> Slew -> Track -> Expose.

- [ ] **v0.6 [Insp. Priembickel]: Hardening & Dashboard**
  - Dash-based UI for monitoring state.
  - Watchdog timers for systemd services.
