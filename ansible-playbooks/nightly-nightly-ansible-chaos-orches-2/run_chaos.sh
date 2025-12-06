#!/bin/bash

# Nightly Ansible Chaos Orchestrator - Run Script
# Inspired by post-apocalyptic chaos engineering

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
PLAYBOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAYBOOK="${PLAYBOOK_DIR}/chaos_orchestrator.yml"
INVENTORY="${PLAYBOOK_DIR}/inventory"
TAGS=""
EXTRA_VARS=""
DRY_RUN=false
VERBOSE=false
HELP=false

# Function to print usage
usage() {
    cat << EOF
${BLUE}🌪️  Nightly Ansible Chaos Orchestrator${NC}

Usage: $0 [OPTIONS]

Options:
    -t, --tags TAGS           Run specific chaos tags (network,service,resource,time,random)
    -e, --extra-vars VARS     Extra variables (e.g., "chaos_duration=600")
    -i, --inventory FILE      Inventory file (default: ${INVENTORY})
    -p, --playbook FILE       Playbook file (default: ${PLAYBOOK})
    -d, --dry-run             Perform a dry run without making changes
    -v, --verbose             Enable verbose output
    -h, --help                Show this help message

Examples:
    $0                                    # Run all chaos experiments
    $0 -t network,service               # Run network and service chaos
    $0 -e "chaos_duration=600"          # Run with custom duration
    $0 -d -v                            # Dry run with verbose output
    $0 -t cleanup                       # Cleanup only

Safety:
    Use --dry-run to preview changes before applying them.
    Always test in non-production environments first.

EOF
}

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

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."

    # Check if ansible is installed
    if ! command -v ansible &> /dev/null; then
        print_error "Ansible is not installed. Please install Ansible first."
        exit 1
    fi

    # Check if playbook exists
    if [[ ! -f "$PLAYBOOK" ]]; then
        print_error "Playbook not found: $PLAYBOOK"
        exit 1
    fi

    # Check if inventory exists
    if [[ ! -f "$INVENTORY" ]]; then
        print_warning "Inventory file not found: $INVENTORY"
        print_warning "Please update the inventory file with your target hosts."
        print_warning "For testing, you can use localhost (be careful!):"
        print_warning "  localhost ansible_connection=local"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    # Check ansible version
    ANSIBLE_VERSION=$(ansible --version | head -1 | awk '{print $2}' | cut -d'.' -f1,2)
    if [[ $(echo "$ANSIBLE_VERSION < 2.10" | bc -l 2>/dev/null || echo 0) -eq 1 ]]; then
        print_warning "Ansible version $ANSIBLE_VERSION detected. Some features may not be available."
        print_warning "Consider upgrading to Ansible 2.10 or later."
    fi

    print_success "Prerequisites check completed"
}

# Function to run ansible-playbook
run_playbook() {
    local cmd=("ansible-playbook")

    # Add inventory
    if [[ -f "$INVENTORY" ]]; then
        cmd+=("-i" "$INVENTORY")
    fi

    # Add tags if specified
    if [[ -n "$TAGS" ]]; then
        cmd+=("--tags" "$TAGS")
    fi

    # Add extra vars if specified
    if [[ -n "$EXTRA_VARS" ]]; then
        cmd+=("-e" "$EXTRA_VARS")
    fi

    # Add dry run flag
    if [[ "$DRY_RUN" == "true" ]]; then
        cmd+=("--check")
        print_warning "Running in DRY RUN mode - no changes will be made"
    fi

    # Add verbose flag
    if [[ "$VERBOSE" == "true" ]]; then
        cmd+=("-v")
    fi

    # Add playbook
    cmd+=("$PLAYBOOK")

    # Print command
    print_status "Running: ${cmd[*]}"
    echo

    # Execute command
    if "${cmd[@]}"; then
        print_success "Chaos engineering playbook completed successfully!"
        echo
        print_status "Review the chaos report generated on each target host."
        print_status "Reports are saved to /tmp/chaos_report_*.txt on each host."
    else
        print_error "Chaos engineering playbook failed!"
        echo
        print_warning "Check the output above for errors."
        print_warning "Ensure your inventory is correct and hosts are accessible."
        print_warning "Verify that required tools (tc, stress, etc.) are installed on target hosts."
        exit 1
    fi
}

# Function to show safety warnings
show_safety_warnings() {
    if [[ "$DRY_RUN" != "true" ]]; then
        print_warning "⚠️  WARNING: You are about to run chaos engineering experiments! ⚠️"
        echo
        print_warning "This playbook will intentionally introduce failures and stress your systems."
        print_warning "Only run this in controlled, non-production environments."
        echo
        print_status "Safety features enabled:"
        print_status "  - Automatic cleanup after chaos"
        print_status "  - Rollback on failure"
        print_status "  - Time limits and safety timeouts"
        echo
        read -p "Do you want to continue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Chaos engineering cancelled."
            exit 0
        fi
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--tags)
            TAGS="$2"
            shift 2
            ;;
        -e|--extra-vars)
            EXTRA_VARS="$2"
            shift 2
            ;;
        -i|--inventory)
            INVENTORY="$2"
            shift 2
            ;;
        -p|--playbook)
            PLAYBOOK="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            HELP=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
esac
done

# Show help if requested
if [[ "$HELP" == "true" ]]; then
    usage
    exit 0
fi

# Main execution
main() {
    echo -e "${BLUE}🌪️  Nightly Ansible Chaos Orchestrator${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo

    # Check prerequisites
    check_prerequisites

    # Show safety warnings
    show_safety_warnings

    # Run the playbook
    run_playbook

    # Show post-run instructions
    echo
    print_success "Chaos engineering completed!"
    echo
    print_status "Next steps:"
    print_status "1. Review the chaos reports on each target host"
    print_status "2. Check system logs for any issues"
    print_status "3. Validate that all services are running normally"
    print_status "4. Analyze system performance metrics"
    print_status "5. Update chaos scenarios based on findings"
    echo
    print_status "For cleanup only, run: $0 -t cleanup"
    print_status "For help, run: $0 -h"
}

# Run main function
main "$@"
