# 🛰️ S30-PRO Federation: Master Workflow (v1.3)
# Human-Readable Data Lifecycle & Pointers

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

4. **ENRICHMENT** (Immediate following Planner)
   -- Executed by: `core/preflight/fetcher.py`
   --- Reads : `data/tonights_plan.json`
   --- Generates: `data/sequences/*.json` (Comp-stars for photometry)

## 🛡️ PHASE 2: THE HANDOVER (The Gatekeeper)

5. **SYSTEM AUDIT** (Real-time / 5min loop)
   -- Executed by: `core/flight/preflight_check.py`
   --- Reads : `Weather API` + `Disk Vitals` + `tonights_plan.json`
   --- Generates: `core/flight/data/preflight_status.json` (Dashboard Feed)

6. **MISSION CONTROL** (The Decision)
   -- Executed by: `core/pre-to-flight-handover.py`
   --- Reads : `preflight_status.json`
   --- Output : [GREEN] -> Pass control to Orchestrator / [RED] -> Scrub Mission

## 🚀 PHASE 3: FLIGHT (The Acquisition Loop)
The repetitive cycle executed for each of the 71 targets.

7. **TARGET INITIALIZATION**
   -- Executed by: `core/flight/orchestrator.py`
   --- Reads : `data/tonights_plan.json`
   --- Action: Commands Alpaca `SlewToCoordinatesAsync` (Port 5555)

8. **CENTERING & FOCUS**
   -- Executed by: `core/flight/block_injector.py`
   --- Action: Injects centering payload and triggers autofocus.
   --- Result: Target confirmed in FOV center.

9. **INTEGRATION**
   -- Executed by: `core/flight/orchestrator.py`
   --- Reads : `exposure_sec` from plan.
   --- Action: Commands `StartExposure`.
   --- Result: 16.6MB raw frame generated in telescope memory.

10. **BUFFER TRANSFER**
   -- Executed by: `core/flight/sync_manager.py` (Active Mode)
   --- Action: Pulls `.fits` from Seestar to `/mnt/usb_buffer`.
   --- Logic: If USB fails, redirects to `lifeboat_dir` (SD Card).

## 🚀 PHASE 3: FLIGHT (Acquisition Loop)
10. **STORAGE VALIDATION**
    -- Executed by: `core/flight/orchestrator.py`
    --- Logic: Check [/mnt/usb_buffer] -> Failover to [~/data/local_buffer]

11. **COORDINATE INJECTION**
    -- Executed by: `core/flight/orchestrator.py`
    --- Reads: `tonights_plan.json`
    --- Action: PUT [/telescope/0/slewtocoordinatesasync]

12. **EXPOSURE INTEGRATION**
    -- Executed by: `core/flight/orchestrator.py`
    --- Action: PUT [/camera/0/startexposure]
    --- Result: FITS stream routed to Active Storage Path.
