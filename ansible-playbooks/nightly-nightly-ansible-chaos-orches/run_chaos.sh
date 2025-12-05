#!/bin/bash
# Nightly Ansible Chaos Orchestrator - Convenience Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
CHAOS_TYPE="random"
CHAOS_DURATION=60
INVENTORY="inventory"
PLAYBOOK="chaos_orchestrator.yml"
VERBOSE=""
DRY_RUN=false

# Help function
show_help() {
    cat << EOF
🎭 Nightly Ansible Chaos Orchestrator

Usage: $0 [CHAOS_TYPE] [DURATION] [OPTIONS]

Arguments:
    CHAOS_TYPE      Type of chaos to apply (network|resource|service|time|random)
    DURATION        Duration in seconds (default: 60)

Options:
    -i, --inventory FILE    Inventory file (default: inventory)
    -p, --playbook FILE     Playbook file (default: chaos_orchestrator.yml)
    -v, --verbose          Verbose output
    -d, --dry-run          Show what would be done without executing
    -h, --help             Show this help message

Examples:
    $0 network 120                    # Network chaos for 2 minutes
    $0 resource 300                   # Resource chaos for 5 minutes
    $0 service 60 -v                  # Verbose service chaos for 1 minute
    $0 time 30 -i my_inventory.ini    # Time chaos with custom inventory
    $0 random 90 --dry-run            # Random chaos in dry-run mode

Available Chaos Types:
    network     - Simulate latency, packet loss, bandwidth throttling
    resource    - Apply CPU stress, memory pressure, I/O throttling
    service     - Restart/stop services, block ports
    time        - Manipulate timezone, NTP, system clock
    random      - Randomly select from available chaos types

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -i|--inventory)
            INVENTORY="$2"
            shift 2
            ;;
        -p|--playbook)
            PLAYBOOK="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            if [[ -z "$CHAOS_TYPE" ]]; then
                CHAOS_TYPE="$1"
            elif [[ -z "$CHAOS_DURATION" ]]; then
                CHAOS_DURATION="$1"
            else
                echo -e "${RED}Error: Unknown argument: $1${NC}" >&2
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate chaos type
VALID_TYPES=("network" "resource" "service" "time" "random")
if [[ ! " ${VALID_TYPES[@]} " =~ " ${CHAOS_TYPE} " ]]; then
    echo -e "${RED}Error: Invalid chaos type: ${CHAOS_TYPE}${NC}" >&2
    echo -e "${YELLOW}Valid types: ${VALID_TYPES[*]}${NC}" >&2
    exit 1
fi

# Validate duration
if ! [[ "$CHAOS_DURATION" =~ ^[0-9]+$ ]] || [ "$CHAOS_DURATION" -le 0 ]; then
    echo -e "${RED}Error: Invalid duration: ${CHAOS_DURATION}${NC}" >&2
    echo -e "${YELLOW}Duration must be a positive integer (seconds)${NC}" >&2
    exit 1
fi

# Check if inventory file exists
if [ ! -f "$INVENTORY" ]; then
    echo -e "${RED}Error: Inventory file not found: ${INVENTORY}${NC}" >&2
    echo -e "${YELLOW}Please create an inventory file or specify a different one with -i${NC}" >&2
    exit 1
fi

# Check if playbook exists
if [ ! -f "$PLAYBOOK" ]; then
    echo -e "${RED}Error: Playbook not found: ${PLAYBOOK}${NC}" >&2
    exit 1
fi

# Check if ansible is installed
if ! command -v ansible-playbook &> /dev/null; then
    echo -e "${RED}Error: ansible-playbook not found${NC}" >&2
    echo -e "${YELLOW}Please install Ansible: pip install ansible${NC}" >&2
    exit 1
fi

# Display execution plan
echo -e "${BLUE}🎭 Nightly Ansible Chaos Orchestrator${NC}"
echo -e "${BLUE}====================================${NC}"
echo -e "${GREEN}Chaos Type:${NC}    ${CHAOS_TYPE}"
echo -e "${GREEN}Duration:${NC}     ${CHAOS_DURATION} seconds"
echo -e "${GREEN}Inventory:${NC}    ${INVENTORY}"
echo -e "${GREEN}Playbook:${NC}     ${PLAYBOOK}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}Mode:${NC}         DRY RUN - No changes will be made"
fi
echo

# Confirmation prompt
if [ "$DRY_RUN" = false ]; then
    echo -e "${YELLOW}⚠️  Warning: This will apply chaos engineering to your systems!${NC}"
    echo -e "${YELLOW}   Only run this in development environments!${NC}"
    echo
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted by user."
        exit 0
    fi
fi

# Execute ansible-playbook
echo -e "${GREEN}🚀 Executing chaos playbook...${NC}"

if [ "$DRY_RUN" = true ]; then
    ansible-playbook $VERBOSE --check -i "$INVENTORY" "$PLAYBOOK" \
        --extra-vars "chaos_type=${CHAOS_TYPE} chaos_duration=${CHAOS_DURATION} dry_run=true"
else
    ansible-playbook $VERBOSE -i "$INVENTORY" "$PLAYBOOK" \
        --extra-vars "chaos_type=${CHAOS_TYPE} chaos_duration=${CHAOS_DURATION}"
fi

# Check exit code
if [ $? -eq 0 ]; then
    echo
    echo -e "${GREEN}✅ Chaos engineering session completed successfully!${NC}"
    echo -e "${BLUE}📁 Check the chaos logs in /tmp/chaos_logs/ on target hosts${NC}"
else
    echo
    echo -e "${RED}❌ Chaos engineering session failed!${NC}"
    echo -e "${YELLOW}Check the ansible output above for error details${NC}"
    exit 1
fi
