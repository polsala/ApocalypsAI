#!/bin/bash

# Nightly Ansible Chaos Orchestrator Runner
# A whimsical script to execute controlled chaos experiments

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAYBOOK="${SCRIPT_DIR}/chaos_orchestrator.yml"
INVENTORY="${SCRIPT_DIR}/inventory"
REPORT_DIR="${SCRIPT_DIR}/reports"
REPORT_FILE="${REPORT_DIR}/chaos_report_$(date +%Y%m%d_%H%M%S).txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to display usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Nightly Ansible Chaos Orchestrator - Execute controlled chaos experiments

OPTIONS:
    -h, --help              Show this help message
    -i, --inventory FILE    Specify inventory file (default: ./inventory)
    -s, --scenario NAME     Specify chaos scenario name
    -t, --target HOST       Specify target host (default: all)
    -v, --verbose           Enable verbose output
    --list-scenarios        List available chaos scenarios
    --dry-run               Perform a dry run without executing chaos

EXAMPLES:
    $0                                    # Run default scenario on all hosts
    $0 -s network_latency -t server-01     # Run network latency on specific host
    $0 --list-scenarios                   # Show available scenarios

EOF
    exit 1
}

# Function to list available scenarios
list_scenarios() {
    echo "Available Chaos Scenarios:"
    echo "  - network_latency: Add network latency to simulate slow connections"
    echo "  - network_packet_loss: Drop packets to simulate unreliable networks"
    echo "  - service_restart: Restart services to simulate failures"
    echo "  - service_stop: Stop services to simulate outages"
    echo "  - cpu_stress: Stress CPU to simulate high load"
    echo "  - memory_stress: Consume memory to simulate memory pressure"
    echo "  - disk_io_stress: Stress disk I/O to simulate slow storage"
    echo "  - time_warp: Manipulate system time (for testing time-sensitive apps)"
    echo "  - random_kill: Randomly kill processes"
    echo "  - random_reboot: Randomly reboot systems"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            ;;
        -i|--inventory)
            INVENTORY="$2"
            shift 2
            ;;
        -s|--scenario)
            CHAOS_SCENARIO="$2"
            shift 2
            ;;
        -t|--target)
            TARGET_HOST="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        --list-scenarios)
            list_scenarios
            exit 0
            ;;
        --dry-run)
            DRY_RUN="--check"
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            ;;
    esac
done

# Check if inventory file exists
if [[ ! -f "$INVENTORY" ]]; then
    print_error "Inventory file not found: $INVENTORY"
    echo "Please create an inventory file or specify one with -i/--inventory"
    exit 1
fi

# Create reports directory
mkdir -p "$REPORT_DIR"

# Build ansible-playbook command
ANSIBLE_CMD="ansible-playbook $VERBOSE $DRY_RUN -i $INVENTORY $PLAYBOOK"

# Add scenario variable if specified
if [[ -n "$CHAOS_SCENARIO" ]]; then
    ANSIBLE_CMD="$ANSIBLE_CMD -e chaos_scenario_name=$CHAOS_SCENARIO"
fi

# Add target host if specified
if [[ -n "$TARGET_HOST" ]]; then
    ANSIBLE_CMD="$ANSIBLE_CMD -l $TARGET_HOST"
fi

# Display banner
print_status "========================================"
print_status "    Nightly Ansible Chaos Orchestrator"
print_status "========================================"
print_status "Inventory: $INVENTORY"
print_status "Report: $REPORT_FILE"
if [[ -n "$CHAOS_SCENARIO" ]]; then
    print_status "Scenario: $CHAOS_SCENARIO"
fi
if [[ -n "$TARGET_HOST" ]]; then
    print_status "Target: $TARGET_HOST"
fi
print_status "========================================"

# Execute the playbook
print_status "Executing chaos experiment..."
if $ANSIBLE_CMD; then
    print_success "Chaos experiment completed successfully!"
    print_status "Check the report: $REPORT_FILE"
else
    print_error "Chaos experiment failed!"
    exit 1
fi

# Display post-execution message
print_warning "Remember: With great power comes great responsibility!"
print_status "Monitor your systems and ensure they recover properly."
