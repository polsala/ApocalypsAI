#!/bin/bash

# Nightly Survival Health Check Report
# This script provides a quick overview of critical system resources.

echo "---"
echo "Nightly Survival Health Check Report"
echo "Date: $(date)"
echo "---"

echo "\n[ Disk Usage (Root Partition) ]"
df -h /

echo "\n[ Memory Usage ]"
free -h

echo "\n[ CPU Load Averages ]"
uptime

echo "\n[ Top 5 CPU-Consuming Processes ]"
ps aux --sort=-%cpu | head -n 6

echo "\n[ Network Connections (LISTEN state) ]"
sudo ss -tuln | head -n 6

echo "---"
