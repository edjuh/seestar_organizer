# Seestar Organizer

**Automated Variable Star Observation Pipeline**

## 🔭 Project Overview
This project automates the entire lifecycle of variable star observation: from planning and capture to photometry and final AAVSO submission. 

The system is specifically optimized for the **ZWO Seestar S30-pro**, leveraging its superior **IMX585 sensor** and wide-field capabilities to capture multiple scientific targets within a single FOV.

## 🏗️ Hardware Stack
- **Compute:** Raspberry Pi (Debian Bookworm)
- **Positioning:** GPS Module (for precision time/location sync)
- **Imaging:** ZWO Seestar S30-pro

## 💻 Software Stack
- **Seestar ALP:** API interface for telescope control and state monitoring.
- **Python 3.13:** Core logic for the Harvester and Analyst services.
- **ASTAP:** Used for high-precision plate solving and stellar identification.

## 🛠️ System Architecture
- **Harvester:** Automates FITS ingest from telescope to NAS/SSD.
- **Analyst:** Handles photometry and AAVSO report generation.

---
**Current Development Phase:** v0.7.4 (Infrastructure Verified)
