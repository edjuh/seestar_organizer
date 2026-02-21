# S30-PRO Roadmap (The Bommel Saga)

- [x] **v0.0 [Beunhaas]: The Raw Foundation**
  - Verified hardware, persistent storage, and API connections.

- [x] **v0.1 [Brigadier Snuf]: Hardware Abstraction**
  - Thread-safe `GPSSensor` and `WeatherSensor`.
  - Config/Env unified loader.
  - Stratum 2 GPS time synchronization via `chrony`.

- [x] **v0.2 [Zedekia Zwederkoorn]: Data Ingestion (The Airgap)**
  - Built `AAVSOClient` to securely fetch target lists.
  - Built polite `fetch_sequences` scraper for local offline caching.
  - Filtered target list down to ~191 S30-PRO physical candidates (M, SR, ZAND, CEP).

- [ ] **v0.3 [Joris Goedbloed]: The Alpaca Bridge**
  - Integrate ASCOM Alpaca protocol wrapper (`AlpacaClient`).
  - Build "Virtual Seestar" mock REST server to simulate the telescope while waiting for hardware delivery.

- [ ] **v0.4 [Zachtzalver]: Target Acquisition & Command**
- [ ] **v0.5 [Hiep Hieper]: The Orchestrator**
- [ ] **v0.6 [Insp. Priembickel]: Hardening & Dashboard**
