# Seestar Organizer: Purified Manifest

## 🛫 PREFLIGHT
* `core/preflight/asassn_validator.py`: Queries ASAS-SN for current magnitudes to ensure targets are
* `core/preflight/audit.py`: Tags done objects until new observation is required based on cadence.
* `core/preflight/fetcher.py`: Fetches AAVSO data with query-string auth and a file-lock to prevent collisions.
* `core/preflight/fog_monitor.py`: Infrared sky-clarity monitor using MLX90614 to prevent imaging in fog.
* `core/preflight/gps.py`: Manages geographic coordinates using config.toml as the source of truth.
* `core/preflight/harvester.py`: Downloads active campaigns from AAVSO, vetoing targets outside FOV constraints.
* `core/preflight/horizon.py`: Veto targets based on local obstructions (Trees, Buildings) using Az/Alt mapping.
* `core/preflight/librarian.py`: Monthly cron tool to fetch NEW targets from AAVSO.
* `core/preflight/nightly_planner.py`: Generates prioritized target lists based on real-time altitude,
* `core/preflight/preflight_master.py`: Orchestrates sequential fetching, coordinate normalization,
* `core/preflight/target_evaluator.py`: Audits the nightly plan for freshness and quantity.
* `core/preflight/weather.py`: Calculates astronomical dark, fetches Open-Meteo & Buienradar forecasts, and returns a UTF-8 evaluated status.
* `core/planning/nightly_planner.py`: Score 1,240 targets against tonights sky and pick the Top 20.

## 🚀 FLIGHT
* `core/flight/block_injector.py`: Transforms tonights_plan.json into 15-minute science blocks using config-driven coordinates.
* `core/flight/env_loader.py`: Centralized configuration and environment variable manager.
* `core/flight/fill_the_night.py`: Stress-test utility to saturate the Federation schedule for maximum night capacity.
* `core/flight/get_manifest.py`: Human-readable reporter for the current Alpaca Bridge flight schedule.
* `core/flight/hardware_profiles.py`: Define sensor specs for Annie (S50), Williamina (S30-Pro), and Henrietta (S30-Pro Fast).
* `core/flight/orchestrator.py`: The primary background daemon (Kwetal) that manages the Alpaca
* `core/flight/preflight_check.py`: Executes full system validation including Targets, GPS, Bridge, Weather, and Disk.
* `core/flight/sequence_engine.py`: Prioritizes targets without crashing on vault attributes.
* `core/flight/vault_manager.py`: Manages secure access to observational metadata and ensures

## 🧪 POSTFLIGHT
* `core/postflight/analyst.py`: Analyzes FITS image quality, FWHM, and basic observational metrics.
* `core/postflight/analyzer.py`: Validates FITS headers and calculates basic QC metrics.
* `core/postflight/calibration_engine.py`: Manages Zero-Point (ZP) offsets and flat-field corrections for the IMX585.
* `core/postflight/master_analyst.py`: High-level plate-solving coordinator for narrow-field Seestar frames.
* `core/postflight/notifier.py`: Outbound alert management via Telegram and system bells.
* `core/postflight/pastinakel_math.py`: Logic for saturation detection and dynamic aperture scaling.
* `core/postflight/photometry_engine.py`: Instrumental flux extraction and science-grade lightcurve generation.
* `core/postflight/pixel_mapper.py`: Converts celestial WCS coordinates to local sensor pixel X/Y coordinates.
* `core/postflight/sync_manager.py`: Manages file synchronization between Seestar, Local Buffer, and NAS.

## 🛠️ UTILS
* `utils/aavso_client.py`: No objective defined.
* `utils/astro.py`: Core library for RA/Dec parsing, sidereal time, and coordinate math.
* `utils/audit_setup.py`: Dumps current Horizon and Target configuration for architectural review.
* `utils/auto_header.py`: not in content:
* `utils/campaign_auditor.py`: Unpacks the JSON envelope and cross-references campaign targets with available AAVSO comparison charts via coordinates.
* `utils/campaign_cleaner.py`: Deduplicates root campaign targets and securely links them via robust coordinate parsing.
* `utils/check_headers.py`: Utility to verify all project Python files contain a Purpose header.
* `utils/cleanup.py`: Housekeeping for temporary files and logs.
* `utils/comp_purger.py`: Scans comparison charts and deletes any file that is empty, malformed, or missing coordinate data.
* `utils/coordinate_converter.py`: Ensures data validity by converting sexagesimal AAVSO coordinates
* `utils/fix_imports.py`: No objective defined.
* `utils/generate_manifest.py`: \s*(.*)', content)
* `utils/ghost_photometry.py`: No objective defined.
* `utils/history_tracker.py`: Scans the Seestar observation storage to update last_observed
* `utils/inject_location.py`: Dynamically synchronizes Bridge/Simulator location using config.toml as the source of truth.
* `utils/inspect_comp.py`: No objective defined.
* `utils/inspect_comp_deep.py`: No objective defined.
* `utils/manifest_auditor.py`: Links 71 targets to 404 comp charts via AUID/Coords.
* `utils/notifier.py`: Sends mission summaries to the Commander via Telegram.
* `utils/platesolve_analyst.py`: No objective defined.
* `utils/quick_phot.py`: No objective defined.
* `utils/undo_header_mess.py`: No objective defined.
* `utils/wvs_ingester.py`: Downloads and parses the KNVWS Werkgroep Veranderlijke Sterren
* `core/utils/disk_monitor.py`: Verifies NAS and local USB/buffer storage availability across all flight phases.
* `core/utils/gps_monitor.py`: Monitors GPSD natively via TCP socket and updates RAM-disk status.
* `core/utils/observer_math.py`: Calculates 6-character Maidenhead grid squares.
* `core/flight-to-post-handover.py`: Secures data after a mission, stops hardware bridges, and triggers post-flight analysis.
* `core/post_to_pre_feedback.py`: Updates targets.json with successful observation dates.
* `core/pre-to-flight-handover.py`: Evaluates the final preflight vitals. If safe, authorizes the FLIGHT phase. If unsafe, aborts the mission.
* `core/selector.py`: Prioritize targets setting in the West during the dark window.
* `core/sequence_repository.py`: Local cache manager for AAVSO V-band comparison sequences.

