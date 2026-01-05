#!/bin/bash

# Nightly SysGuard - System Health Monitor with Apocalyptic Flair
# Version 1.0.0

# Default thresholds
DEFAULT_CPU_THRESHOLD=85
DEFAULT_MEMORY_THRESHOLD=90
DEFAULT_DISK_THRESHOLD=80

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
CPU_THRESHOLD=$DEFAULT_CPU_THRESHOLD
MEMORY_THRESHOLD=$DEFAULT_MEMORY_THRESHOLD
DISK_THRESHOLD=$DEFAULT_DISK_THRESHOLD
JSON_OUTPUT=false
CHECK_MODE=false

# Whimsical messages
get_cpu_message() {
    local usage=$1
    if [ $usage -lt 50 ]; then
        echo "CPU running cool"
    elif [ $usage -lt 80 ]; then
        echo "CPU warming up"
    else
        echo "CPU overheating!"
    fi
}

get_memory_message() {
    local usage=$1
    if [ $usage -lt 70 ]; then
        echo "Supplies well stocked"
    elif [ $usage -lt 90 ]; then
        echo "Supplies running low!"
    else
        echo "Critical supply shortage!"
    fi
}

get_disk_message() {
    local usage=$1
    if [ $usage -lt 70 ]; then
        echo "Storage bunkers secure"
    elif [ $usage -lt 85 ]; then
        echo "Storage getting tight"
    else
        echo "Storage bunkers full!"
    fi
}

# Get system metrics
get_cpu_usage() {
    # Get CPU usage percentage (1-minute average)
    if command -v top >/dev/null 2>&1; then
        top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}' | cut -d. -f1
    elif command -v vmstat >/dev/null 2>&1; then
        vmstat 1 2 | tail -1 | awk '{print 100 - $15}'
    else
        echo "0"
    fi
}

get_memory_usage() {
    # Get memory usage percentage
    if command -v free >/dev/null 2>&1; then
        free | grep Mem | awk '{printf("%.0f", ($3/$2) * 100.0)}'
    elif command -v top >/dev/null 2>&1; then
        top -bn1 | grep "MiB Mem" | awk '{printf("%.0f", ($7/$3) * 100.0)}'
    else
        echo "0"
    fi
}

get_disk_usage() {
    # Get disk usage percentage for root filesystem
    df / | tail -1 | awk '{print $5}' | sed 's/%//'
}

# Output functions
print_status_text() {
    local cpu_usage=$1
    local memory_usage=$2
    local disk_usage=$3
    local cpu_status=$4
    local memory_status=$5
    local disk_status=$6

    echo -e "${BLUE}=== NIGHTLY SYSGUARD SYSTEM STATUS ===${NC}\n"
    
    # CPU status
    if [ "$cpu_status" = "normal" ]; then
        echo -e "[✓] CPU Usage: ${cpu_usage}% (Normal)"
    elif [ "$cpu_status" = "warning" ]; then
        echo -e "[⚠] CPU Usage: ${cpu_usage}% (Warning)"
    else
        echo -e "[✗] CPU Usage: ${cpu_usage}% (Critical)"
    fi
    
    # Memory status
    if [ "$memory_status" = "normal" ]; then
        echo -e "[✓] Memory Usage: ${memory_usage}% (Normal)"
    elif [ "$memory_status" = "warning" ]; then
        echo -e "[⚠] Memory Usage: ${memory_usage}% (Warning)"
    else
        echo -e "[✗] Memory Usage: ${memory_usage}% (Critical)"
    fi
    
    # Disk status
    if [ "$disk_status" = "normal" ]; then
        echo -e "[✓] Disk Usage: ${disk_usage}% (Normal)"
    elif [ "$disk_status" = "warning" ]; then
        echo -e "[⚠] Disk Usage: ${disk_usage}% (Warning)"
    else
        echo -e "[✗] Disk Usage: ${disk_usage}% (Critical)"
    fi
    
    echo
    
    # Overall status
    if [ "$cpu_status" = "critical" ] || [ "$memory_status" = "critical" ] || [ "$disk_status" = "critical" ]; then
        echo -e "${RED}Status: SYSTEM CRITICAL - Evacuate non-essential processes!${NC}"
    elif [ "$cpu_status" = "warning" ] || [ "$memory_status" = "warning" ] || [ "$disk_status" = "warning" ]; then
        echo -e "${YELLOW}Status: System needs attention. Keep scavenging!${NC}"
    else
        echo -e "${GREEN}Status: System stable. Keep scavenging!${NC}"
    fi
}

print_status_json() {
    local cpu_usage=$1
    local memory_usage=$2
    local disk_usage=$3
    local cpu_status=$4
    local memory_status=$5
    local disk_status=$6

    local cpu_msg="$(get_cpu_message $cpu_usage)"
    local memory_msg="$(get_memory_message $memory_usage)"
    local disk_msg="$(get_disk_message $disk_usage)"

    local overall_status="ok"
    if [ "$cpu_status" = "critical" ] || [ "$memory_status" = "critical" ] || [ "$disk_status" = "critical" ]; then
        overall_status="critical"
    elif [ "$cpu_status" = "warning" ] || [ "$memory_status" = "warning" ] || [ "$disk_status" = "warning" ]; then
        overall_status="warning"
    fi

    cat <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "cpu": {
    "usage": $cpu_usage,
    "status": "$cpu_status",
    "message": "$cpu_msg",
    "threshold": $CPU_THRESHOLD
  },
  "memory": {
    "usage": $memory_usage,
    "status": "$memory_status",
    "message": "$memory_msg",
    "threshold": $MEMORY_THRESHOLD
  },
  "disk": {
    "usage": $disk_usage,
    "status": "$disk_status",
    "message": "$disk_msg",
    "threshold": $DISK_THRESHOLD
  },
  "overall_status": "$overall_status"
}
EOF
}

# Check thresholds and return status
check_threshold() {
    local usage=$1
    local threshold=$2
    
    if [ $usage -ge $threshold ]; then
        if [ $usage -ge $((threshold + 10)) ]; then
            echo "critical"
        else
            echo "warning"
        fi
    else
        echo "normal"
    fi
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --cpu)
                CPU_THRESHOLD="$2"
                shift 2
                ;;
            --memory)
                MEMORY_THRESHOLD="$2"
                shift 2
                ;;
            --disk)
                DISK_THRESHOLD="$2"
                shift 2
                ;;
            --json)
                JSON_OUTPUT=true
                shift
                ;;
            --check)
                CHECK_MODE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    cat <<EOF
Nightly SysGuard - System Health Monitor

Usage: $0 [OPTIONS]

Options:
  --cpu THRESHOLD    CPU usage warning threshold (default: $DEFAULT_CPU_THRESHOLD%)
  --memory THRESHOLD Memory usage warning threshold (default: $DEFAULT_MEMORY_THRESHOLD%)
  --disk THRESHOLD   Disk usage warning threshold (default: $DEFAULT_DISK_THRESHOLD%)
  --json             Output in JSON format
  --check            Exit with code 1 if any threshold exceeded, 0 otherwise
  --help, -h         Show this help message

Examples:
  $0                           # Run with default thresholds
  $0 --cpu 80 --memory 90      # Custom thresholds
  $0 --json                    # JSON output
  $0 --check && echo OK || echo CRITICAL  # Check mode
EOF
}

# Main execution
main() {
    # Parse arguments
    parse_args "$@"
    
    # Get current system metrics
    CPU_USAGE=$(get_cpu_usage)
    MEMORY_USAGE=$(get_memory_usage)
    DISK_USAGE=$(get_disk_usage)
    
    # Check thresholds
    CPU_STATUS=$(check_threshold $CPU_USAGE $CPU_THRESHOLD)
    MEMORY_STATUS=$(check_threshold $MEMORY_USAGE $MEMORY_THRESHOLD)
    DISK_STATUS=$(check_threshold $DISK_USAGE $DISK_THRESHOLD)
    
    # Output results
    if [ "$JSON_OUTPUT" = true ]; then
        print_status_json $CPU_USAGE $MEMORY_USAGE $DISK_USAGE $CPU_STATUS $MEMORY_STATUS $DISK_STATUS
    else
        print_status_text $CPU_USAGE $MEMORY_USAGE $DISK_USAGE $CPU_STATUS $MEMORY_STATUS $DISK_STATUS
    fi
    
    # Exit with appropriate code for check mode
    if [ "$CHECK_MODE" = true ]; then
        if [ "$CPU_STATUS" = "critical" ] || [ "$MEMORY_STATUS" = "critical" ] || [ "$DISK_STATUS" = "critical" ]; then
            exit 2  # Critical
        elif [ "$CPU_STATUS" = "warning" ] || [ "$MEMORY_STATUS" = "warning" ] || [ "$DISK_STATUS" = "warning" ]; then
            exit 1  # Warning
        else
            exit 0  # OK
        fi
    fi
}

# Run main function with all arguments
main "$@"
