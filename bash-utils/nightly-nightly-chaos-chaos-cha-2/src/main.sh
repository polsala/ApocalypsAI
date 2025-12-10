#!/bin/bash

# Nightly Chaos Chaos Cha
# A whimsical chaos orchestrator for testing resilience

set -euo pipefail

# Configuration
MODE=${1:--m}
DURATION=${2:--d}

# Colors for whimsical output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print whimsical messages
print_chaos() {
  echo -e "${RED}CHAOS!${NC} ${YELLOW}CHAOS!${NC} ${GREEN}CHA!${NC}"
}

# Function to introduce network latency
introduce_network_latency() {
  echo "Introducing network latency..."
  # Use tc to add latency (requires root)
  sudo tc qdisc add dev lo root netem delay 100ms 2>/dev/null || true
  print_chaos
}

# Function to remove network latency
remove_network_latency() {
  echo "Removing network latency..."
  sudo tc qdisc del dev lo root 2>/dev/null || true
}

# Function to introduce CPU load
introduce_cpu_load() {
  echo "Introducing CPU load..."
  # Start background processes to consume CPU
  for i in {1..2}; do
    yes > /dev/null &
  done
  print_chaos
}

# Function to remove CPU load
remove_cpu_load() {
  echo "Removing CPU load..."
  pkill -f yes || true
}

# Function to introduce memory pressure
introduce_memory_pressure() {
  echo "Introducing memory pressure..."
  # Allocate memory in background
  dd if=/dev/zero of=/tmp/chaos_memory bs=1M count=100 2>/dev/null &
  print_chaos
}

# Function to remove memory pressure
remove_memory_pressure() {
  echo "Removing memory pressure..."
  rm -f /tmp/chaos_memory || true
}

# Function to run chaos scenario
run_chaos_scenario() {
  local mode=$1
  local duration=$2
  
  case $mode in
    "chaos-chaos-cha")
      introduce_network_latency
      introduce_cpu_load
      introduce_memory_pressure
      sleep $duration
      remove_network_latency
      remove_cpu_load
      remove_memory_pressure
      ;;
    "network-only")
      introduce_network_latency
      sleep $duration
      remove_network_latency
      ;;
    "cpu-only")
      introduce_cpu_load
      sleep $duration
      remove_cpu_load
      ;;
    "memory-only")
      introduce_memory_pressure
      sleep $duration
      remove_memory_pressure
      ;;
    *)
      echo "Unknown mode: $mode"
      echo "Available modes: chaos-chaos-cha, network-only, cpu-only, memory-only"
      exit 1
      ;;
  esac
}

# Function to show usage
show_usage() {
  echo "Usage: $0 --mode <mode> --duration <seconds>"
  echo "Modes: chaos-chaos-cha, network-only, cpu-only, memory-only"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -m|--mode)
      MODE="$2"
      shift 2
      ;;
    -d|--duration)
      DURATION="$2"
      shift 2
      ;;
    -h|--help)
      show_usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      show_usage
      exit 1
      ;;
  esac
done

# Validate arguments
if [[ -z "$MODE" || -z "$DURATION" ]]; then
  echo "Error: Both mode and duration are required."
  show_usage
  exit 1
fi

# Run the chaos scenario
run_chaos_scenario "$MODE" "$DURATION"
echo "Chaos scenario completed successfully!"
