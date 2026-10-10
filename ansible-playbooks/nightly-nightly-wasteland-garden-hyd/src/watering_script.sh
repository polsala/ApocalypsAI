#!/bin/bash
# This script simulates watering a wasteland garden plot.
# It logs a hydration event.

LOG_DIR="/tmp/wasteland_garden_logs"
LOG_FILE="${LOG_DIR}/hydration_log_$(date +%Y-%m-%d).log"

mkdir -p "$LOG_DIR"
echo "$(date '+%Y-%m-%d %H:%M:%S') - Garden plot hydrated!" >> "$LOG_FILE"
echo "Wasteland garden plot hydrated. Logged to $LOG_FILE"
