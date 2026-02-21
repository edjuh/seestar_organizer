#!/bin/bash
# Seestar Organizer Health Check
# Checks if heartbeats are fresh (older than 600 seconds = FAIL)

CHECK_TIME=$(date +%s)
MAX_AGE=600

for status_file in logs/*.json; do
    FILE_TIME=$(stat -c %Y "$status_file")
    AGE=$((CHECK_TIME - FILE_TIME))
    
    if [ $AGE -gt $MAX_AGE ]; then
        echo " [FAIL] $status_file is STALE ($AGE seconds old)"
    else
        echo " [OK]   $status_file is fresh ($AGE seconds old)"
    fi
done
