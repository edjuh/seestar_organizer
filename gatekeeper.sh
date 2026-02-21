#!/bin/bash
# S30-PRO Lifecycle Manager - SURGICAL EDITION
# v1.1 - Added Unbuffered Output (-u) for real-time logging

LOCK_FILE="/tmp/s30_pro.lock"

case "$1" in
    stop)
        echo "[!] Stopping S30-PRO processes..."
        
        # 1. Kill the Main Unit
        pkill -f "python3 main.py" && echo " -> Killed main.py"
        
        # 2. Kill any lingering legacy services (just in case)
        pkill -f "services/launcher.py" && echo " -> Killed launcher.py"
        pkill -f "core/organizer.py" && echo " -> Killed organizer.py"
        
        # 3. Cleanup Lock
        if [ -f "$LOCK_FILE" ]; then
            rm "$LOCK_FILE"
            echo " -> Lock file removed."
        fi
        
        echo "[+] Stop complete. SSH safe."
        ;;
    start)
        $0 stop
        echo "[+] Starting S30-PRO Single Unit..."
        
        # KEY CHANGE HERE: added '-u' flag to python3
        # This forces stdout/stderr to be unbuffered
        nohup .venv/bin/python3 -u main.py > logs/system.log 2>&1 &
        
        echo "[+] System launched. Check logs/system.log"
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
esac
