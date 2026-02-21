#!/bin/bash
# Seestar Organizer Service Launcher

source .venv/bin/activate

echo "Starting Organizer Engine..."
python3 -m services.organizer > /dev/null 2>&1 &
echo $! > logs/organizer.pid

echo "Starting Telescope Link..."
python3 -m services.telescope > /dev/null 2>&1 &
echo $! > logs/telescope.pid

echo "Starting Weather Safety..."
python3 -m services.weather_safety > /dev/null 2>&1 &
echo $! > logs/weather.pid

echo "Starting Target Manager..."
python3 -m services.target_manager > /dev/null 2>&1 &
echo $! > logs/target.pid

echo "All services started in background."
