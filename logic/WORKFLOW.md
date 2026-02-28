# 🛰️ S30-PRO Federation: Master Workflow

> **Objective:** Outlines the end-to-end human-readable data lifecycle and pointers for the S30-PRO Federation.
> **Version:** 1.2.0 (Garmt)

## 🏁 PHASE 1: PRE-FLIGHT (The Funnel)
1. **INITIAL HARVEST** (Manual/Once)
   -- Executed by: `core/preflight/harvester.py`
   --- Generates: `data/targets.json` (The Master Catalog)
2. **MONTHLY UPDATES** (Cron: 15th of month)
   -- Executed by: `core/preflight/librarian.py`
   --- Reads : `AAVSO Alert Feed`
   --- Generates: `data/targets.json` (Appends new science)
3. **REFINEMENT** (Daily Cron: 17:00)
   -- Executed by: `core/preflight/nightly_planner.py`
   --- Reads : `data/targets.json` + `config.toml` (Horizon/GPS)
   --- Generates: `data/tonights_plan.json` (The Optimized Schedule)

## 🛡️ PHASE 2: THE HANDOVER (The Gatekeeper)
5. **SYSTEM AUDIT** (Real-time / 5min loop)
   -- Executed by: `core/flight/preflight_check.py`
   --- Reads : `Weather API` + `Disk Vitals` + `tonights_plan.json`
6. **MISSION CONTROL** (The Decision)
   -- Executed by: `core/pre-to-flight-handover.py`
   --- Output : [GREEN] -> Pass control to Orchestrator / [RED] -> Scrub Mission

## 🚀 PHASE 3: FLIGHT (The Acquisition Loop)
10. **STORAGE VALIDATION**
    -- Executed by: `core/flight/orchestrator.py`
    --- Logic: Check [/mnt/usb_buffer] -> Failover to [~/data/local_buffer]
12. **EXPOSURE INTEGRATION**
    -- Executed by: `core/flight/orchestrator.py`
    --- Action: PUT [/camera/0/startexposure]
    --- Result: FITS stream routed to Active Storage Path.
