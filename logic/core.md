# 🧠 S30-PRO Core Logic Flow

This document defines the operational sequence of the SeestarJoost system.

## 🛰️ Operational Pipeline
The system follows a linear chain of command:

1. **The Harvest**: `AAVSO Client` fetches targets from the Alert Corps.
2. **The Ingest**: `Librarian` (SequenceRepository) saves them to the JSON library.
3. **The Manifest**: `Nightly Planner` (Alexander Pieps) filters targets >30° for Haarlem.
4. **The Safety Gate**: `Orchestrator` checks `Fog Monitor` (Hardware) and `Weather` (Forecast).
5. **The Action**: `Alpaca Client` commands the Seestar to slew and track.
6. **The Cleanup**: `Sync Manager` detects new FITS files and moves them to the NAS/Lifeboat.

## 🏛️ Guiding Principle
*Do not live in the moment. Plan for the astronomical night.*
