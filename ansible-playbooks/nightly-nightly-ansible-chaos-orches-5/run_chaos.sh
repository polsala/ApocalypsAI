#!/bin/bash

# Nightly Ansible Chaos Orchestrator Runner
# Execute chaos engineering experiments with style!

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAYBOOK="${SCRIPT_DIR}/chaos_orchestrator.yml"
INVENTORY="${SCRIPT_DIR}/inventory.ini"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${RED}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                 🚨 CHAOS ENGINE 🚨                        ║"
    echo "║              Ansible Edition v1.0                        ║"
    echo "║                                                            ║"
    echo "║  Unleash controlled chaos upon your infrastructure!      ║"
    echo "║  May your backups be plentiful and rollbacks swift!      ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_usage() {
    echo -e "${BLUE}Usage:${NC} $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -i, --inventory FILE    Specify inventory file (default: inventory.ini)"
    echo "  -p, --playbook FILE     Specify playbook file (default: chaos_orchestrator.yml)"
    echo "  -l, --limit HOSTS       Limit chaos to specific hosts/groups"
    echo "  -v, --verbose           Enable verbose output"
    echo "  -h, --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Run chaos on all hosts"
    echo "  $0 -l webservers                     # Run chaos only on webservers"
    echo "  $0 -i custom_inventory.ini -v        # Use custom inventory with verbose output"
    echo ""
    echo -e "${YELLOW}Safety First:${NC}"
    echo "  - Always test in staging first"
    echo "  - Monitor your chaos reports"
    echo "  - Have a rollback plan ready"
}

check_dependencies() {
    if ! command -v ansible &> /dev/null; then
        echo -e "${RED}Error:${NC} Ansible is not installed or not in PATH"
        echo "Please install Ansible before running this script"
        exit 1
    fi

    if ! command -v ansible-playbook &> /dev/null; then
        echo -e "${RED}Error:${NC} Ansible-playbook is not installed or not in PATH"
        exit 1
    fi
}

validate_files() {
    if [ ! -f "$PLAYBOOK" ]; then
        echo -e "${RED}Error:${NC} Playbook not found: $PLAYBOOK"
        exit 1
    fi

    if [ ! -f "$INVENTORY" ]; then
        echo -e "${RED}Error:${NC} Inventory file not found: $INVENTORY"
        echo "Please create an inventory file or specify one with -i/--inventory"
        exit 1
    fi
}

run_chaos() {
    local extra_args=""

    if [ -n "$LIMIT" ]; then
        extra_args="$extra_args --limit $LIMIT"
    fi

    if [ "$VERBOSE" = true ]; then
        extra_args="$extra_args -v"
    fi

    echo -e "${GREEN}🚀 Initiating chaos sequence...${NC}"
    echo -e "${BLUE}Playbook:${NC} $PLAYBOOK"
    echo -e "${BLUE}Inventory:${NC} $INVENTORY"
    if [ -n "$LIMIT" ]; then
        echo -e "${BLUE}Limit:${NC} $LIMIT"
    fi
    echo ""

    ansible-playbook $extra_args -i "$INVENTORY" "$PLAYBOOK"

    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}🎉 Chaos execution completed successfully!${NC}"
        echo -e "${BLUE}Check the generated chaos reports in /tmp/chaos_logs/${NC}"
    else
        echo ""
        echo -e "${RED}💥 Chaos execution failed!${NC}"
        echo -e "${YELLOW}Check the logs above for details${NC}"
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
        -p|--playbook)
            PLAYBOOK="$2"
            shift 2
            ;;
        -l|--limit)
            LIMIT="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option:${NC} $1"
            print_usage
            exit 1
            ;;
esac
done

# Main execution
print_banner
check_dependencies
validate_files
run_chaos
