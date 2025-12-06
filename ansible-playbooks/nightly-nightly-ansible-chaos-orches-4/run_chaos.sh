#!/bin/bash

# Nightly Ansible Chaos Orchestrator Runner
# A whimsical-yet-useful script to execute chaos engineering experiments

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAYBOOK="${SCRIPT_DIR}/chaos_orchestrator.yml"
INVENTORY="${SCRIPT_DIR}/inventory"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║               Nightly Ansible Chaos Orchestrator           ║"
    echo "║                    Whimsical Chaos Engineering             ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -i, --inventory FILE    Use custom inventory file (default: inventory)"
    echo "  -p, --playbook FILE     Use custom playbook file (default: chaos_orchestrator.yml)"
    echo "  -l, --limit HOSTS       Limit execution to specific hosts"
    echo "  -v, --verbose           Enable verbose output"
    echo "  -h, --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Run with default settings"
    echo "  $0 -l server1,server2                 # Limit to specific hosts"
    echo "  $0 -v                                 # Enable verbose output"
    echo "  $0 -i custom_inventory -p custom.yml  # Use custom files"
}

# Parse command line arguments
VERBOSE=""
LIMIT=""

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
            VERBOSE="-v"
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            print_usage
            exit 1
            ;;
esac
done

# Check if required files exist
if [[ ! -f "$PLAYBOOK" ]]; then
    echo -e "${RED}Error: Playbook file not found: $PLAYBOOK${NC}"
    exit 1
fi

if [[ ! -f "$INVENTORY" ]]; then
    echo -e "${RED}Error: Inventory file not found: $INVENTORY${NC}"
    exit 1
fi

# Print banner
print_banner

# Check if Ansible is installed
if ! command -v ansible &> /dev/null; then
    echo -e "${RED}Error: Ansible is not installed or not in PATH${NC}"
    echo "Please install Ansible: pip install ansible"
    exit 1
fi

# Build ansible-playbook command
ANSIBLE_CMD="ansible-playbook $VERBOSE -i $INVENTORY $PLAYBOOK"

# Add limit if specified
if [[ -n "$LIMIT" ]]; then
    ANSIBLE_CMD="$ANSIBLE_CMD --limit $LIMIT"
fi

# Execute the playbook
echo -e "${GREEN}Executing chaos engineering playbook...${NC}"
echo -e "${YELLOW}Command: $ANSIBLE_CMD${NC}"
echo ""

$ANSIBLE_CMD

# Check exit code
if [[ $? -eq 0 ]]; then
    echo ""
    echo -e "${GREEN}🎉 Chaos engineering execution completed successfully!${NC}"
    echo -e "${BLUE}📊 Check the generated HTML reports for detailed results.${NC}"
else
    echo ""
    echo -e "${RED}❌ Chaos engineering execution failed!${NC}"
    exit 1
fi
