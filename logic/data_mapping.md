# 🧠 S30-PRO Data Lifecycle

Data in SeestarJoost follows a "Funnel" pattern:

1. **RAW FETCH**: `sync_catalog.py` pulls thousands of lines from AAVSO -> `targets.json`.
2. **REFINEMENT**: `nightly_planner.py` reads `targets.json`, applies GPS/Horizon math -> `tonights_plan.json`.
3. **ENRICHMENT**: `fetch_sequences.py` reads `targets.json`, hits VSP API -> `sequences/*.json`.
4. **EXECUTION**: `orchestrator.py` reads `tonights_plan.json` to command slews.
5. **RESULT**: `sync_manager.py` moves FITS images into `local_buffer/`.
