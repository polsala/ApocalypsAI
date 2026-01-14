#!/bin/bash

# Default values
SURVIVAL_LEVEL=5
RESOURCES=100
DAYS=7

show_help() {
  echo "Usage: $0 [OPTIONS]"
  echo "Calculate your daily chaos budget for post-apocalyptic survival."
  echo ""
  echo "Options:"
  echo "  -h, --help              Show this help message"
  echo "  -s, --survival-level    Set survival level (1-10, default: 5)"
  echo "  -r, --resources         Available resources (default: 100)"
  echo "  -d, --days              Number of days to plan for (default: 7)"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      show_help
      exit 0
      ;;
    -s|--survival-level)
      SURVIVAL_LEVEL="$2"
      shift 2
      ;;
    -r|--resources)
      RESOURCES="$2"
      shift 2
      ;;
    -d|--days)
      DAYS="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      show_help
      exit 1
      ;;
  esac
done

# Validate inputs
if ! [[ "$SURVIVAL_LEVEL" =~ ^[0-9]+$ ]] || [ "$SURVIVAL_LEVEL" -lt 1 ] || [ "$SURVIVAL_LEVEL" -gt 10 ]; then
  echo "Error: Survival level must be an integer between 1 and 10."
  exit 1
fi

if ! [[ "$RESOURCES" =~ ^[0-9]+$ ]] || [ "$RESOURCES" -lt 0 ]; then
  echo "Error: Resources must be a non-negative integer."
  exit 1
fi

if ! [[ "$DAYS" =~ ^[0-9]+$ ]] || [ "$DAYS" -lt 1 ]; then
  echo "Error: Days must be a positive integer."
  exit 1
fi

# Calculate chaos budget
CHAOS_FACTOR=$((11 - SURVIVAL_LEVEL))
DAILY_BUDGET=$((RESOURCES * CHAOS_FACTOR / 100 / DAYS))

# Output result
echo "=== CHAOS BUDGET CALCULATION ==="
echo "Survival Level: $SURVIVAL_LEVEL/10"
echo "Available Resources: $RESOURCES units"
echo "Planning Period: $DAYS days"
echo "-------------------------------"
echo "Daily Chaos Budget: $DAILY_BUDGET units"
echo "-------------------------------"

# Fun messages based on chaos level
if [ "$DAILY_BUDGET" -gt 10 ]; then
  echo "You're living dangerously! Better stock up on snacks."
elif [ "$DAILY_BUDGET" -gt 5 ]; then
  echo "Moderate chaos levels. Stay alert!"
else
  echo "Low chaos day. Perfect time for meditation."
fi
