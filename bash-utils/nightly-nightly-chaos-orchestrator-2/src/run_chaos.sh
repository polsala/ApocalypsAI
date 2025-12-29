#!/bin/bash

# Nightly Chaos Orchestrator
# A whimsical chaos engineering tool

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAYBOOK="${SCRIPT_DIR}/chaos_orchestrator.yml"
INVENTORY="${SCRIPT_DIR}/inventory.ini"
DRY_RUN=false
SCENARIO_FILTER=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Nightly Chaos Orchestrator - Inject controlled mayhem into your systems!

OPTIONS:
    -i, --inventory FILE    Use custom inventory file (default: ${INVENTORY})
    -s, --scenario SCENARIO Apply specific chaos scenario
    -d, --dry-run          Show what would be done without executing
    -h, --help             Show this help message

EXAMPLES:
    $0                                    # Run with default configuration
    $0 --inventory custom_inventory.ini   # Use custom inventory
    $0 --scenario network_partition       # Run specific scenario
    $0 --dry-run                          # Preview chaos without execution

EOF
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

check_requirements() {
    local missing=()

    if ! command -v ansible &> /dev/null; then
        missing+=("ansible")
    fi

    if ! command -v python3 &> /dev/null; then
        missing+=("python3")
    fi

    if [ ${#missing[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing[*]}"
        log_info "Please install: sudo apt install ansible python3"
        exit 1
    fi
}

validate_inventory() {
    if [ ! -f "$1" ]; then
        log_error "Inventory file not found: $1"
        exit 1
    fi

    # Basic validation - check if it has [targets] section
    if ! grep -q "\[targets\]" "$1"; then
        log_warn "Inventory file may not have [targets] section: $1"
    fi
}

run_chaos() {
    local inventory_file="$1"
    local extra_args=()

    log_info "Starting chaos engineering session"
    log_info "Target inventory: $inventory_file"

    # Build ansible-playbook command
    local ansible_cmd=("ansible-playbook")

    if [ "$DRY_RUN" = true ]; then
        ansible_cmd+=("--check" "--diff")
        log_warn "DRY RUN MODE - No actual chaos will be applied"
    fi

    if [ -n "$SCENARIO_FILTER" ]; then
        ansible_cmd+=("-e" "scenario_filter=$SCENARIO_FILTER")
        log_info "Filtering scenarios: $SCENARIO_FILTER"
    fi

    ansible_cmd+=("-i" "$inventory_file" "$PLAYBOOK")

    log_info "Executing: ${ansible_cmd[*]}"

    # Execute the playbook
    if "${ansible_cmd[@]}"; then
        log_success "Chaos engineering session completed successfully"
    else
        log_error "Chaos engineering session failed"
        exit 1
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--inventory)
            INVENTORY="$2"
            shift 2
            ;;
        -s|--scenario)
            SCENARIO_FILTER="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Main execution
main() {
    log_info "=== Nightly Chaos Orchestrator v1.0 ==="
    log_info "Embracing chaos, one system at a time..."

    check_requirements
    validate_inventory "$INVENTORY"
    run_chaos "$INVENTORY"

    log_success "Chaos engineering session complete!"
    log_info "Check the generated reports for details."
}

# Run main function
main
