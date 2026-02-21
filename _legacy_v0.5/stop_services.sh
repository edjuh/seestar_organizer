#!/bin/bash
# Seestar Organizer Service Stopper

[ -f logs/organizer.pid ] && kill $(cat logs/organizer.pid) && rm logs/organizer.pid
[ -f logs/telescope.pid ] && kill $(cat logs/telescope.pid) && rm logs/telescope.pid
[ -f logs/weather.pid ] && kill $(cat logs/weather.pid) && rm logs/weather.pid

echo "All background services stopped."
