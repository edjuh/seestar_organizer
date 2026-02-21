#!/bin/bash
# Seestar Organizer Setup Script

echo "--- Seestar Organizer v0.6.9 Initialization ---"

# 1. Check Virtual Env
if [ ! -d ".venv" ]; then
    echo "[*] Creating .venv..."
    python3 -m venv .venv
fi
source .venv/bin/activate

# 2. Dependency Check
pip install rich requests astropy tomli

# 3. Secure .env creation
if [ ! -f ".env" ]; then
    echo "[!] Security: Creating .env"
    read -p "Enter AAVSO Code (e.g. REDA): " code
    read -p "Enter Full Name: " name
    echo "AAVSO_CODE=$code" > .env
    echo "OBSERVER_NAME=\"$name\"" >> .env
fi

# 4. Final Sync
python3 utils/fetch_aavso_targets.py

echo "[OK] Setup finished. Try 'python3 main.py' now."
