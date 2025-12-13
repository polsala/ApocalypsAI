#!/bin/bash

# Nightly Chaos Garden Orchestrator Runner
# A whimsical script to unleash controlled chaos on your infrastructure

set -e

CHAOS_PLAYBOOK="chaos_garden_orchestrator.yml"
INVENTORY="inventory.ini"
LOG_DIR="chaos_logs"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="$LOG_DIR/chaos_session_$TIMESTAMP.log"

# Colors for whimsical output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print whimsical header
print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                 🌱 Chaos Garden Runner 🌱                 ║"
    echo "║                    Unleash the Whimsy!                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to print footer
print_footer() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              🌱 Chaos Session Complete! 🌱                ║"
    echo "║          Your infrastructure is stronger now!              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    if ! command -v ansible &> /dev/null; then
        echo -e "${RED}Error: Ansible is not installed or not in PATH${NC}"
        exit 1
    fi
    
    if [ ! -f "$INVENTORY" ]; then
        echo -e "${RED}Error: Inventory file '$INVENTORY' not found${NC}"
        exit 1
    fi
    
    if [ ! -f "$CHAOS_PLAYBOOK" ]; then
        echo -e "${RED}Error: Playbook '$CHAOS_PLAYBOOK' not found${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Prerequisites check passed${NC}"
}

# Function to create log directory
setup_logging() {
    mkdir -p "$LOG_DIR"
    echo "Chaos session log: $LOG_FILE"
}

# Function to run chaos playbook
run_chaos() {
    echo -e "${BLUE}Unleashing chaos upon your infrastructure...${NC}"
    
    # Run the ansible playbook with verbose output
    ansible-playbook \
        -i "$INVENTORY" \
        "$CHAOS_PLAYBOOK" \
        -v \
        --extra-vars "chaos_timestamp=$TIMESTAMP" \
        2>&1 | tee "$LOG_FILE"
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo -e "${GREEN}✓ Chaos execution completed successfully${NC}"
    else
        echo -e "${RED}✗ Chaos execution failed - check logs for details${NC}"
        exit 1
    fi
}

# Function to display chaos summary
show_summary() {
    echo -e "${YELLOW}Chaos Session Summary:${NC}"
    echo "  Timestamp: $TIMESTAMP"
    echo "  Log file: $LOG_FILE"
    echo "  Inventory: $INVENTORY"
    echo "  Playbook: $CHAOS_PLAYBOOK"
}

# Main execution
main() {
    print_header
    check_prerequisites
    setup_logging
    show_summary
    echo ""
    run_chaos
    echo ""
    print_footer
}

# Handle command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  -h, --help     Show this help message"
            echo "  -i, --inventory  Specify inventory file (default: inventory.ini)"
            echo "  -p, --playbook   Specify playbook file (default: chaos_garden_orchestrator.yml)"
            echo ""
            echo "Environment Variables:"
            echo "  CHAOS_INTENSITY  Set chaos intensity (low|medium|high)"
            echo "  CHAOS_DURATION   Set chaos duration in seconds"
            echo ""
            exit 0
            ;;
        -i|--inventory)
            INVENTORY="$2"
            shift 2
            ;;
        -p|--playbook)
            CHAOS_PLAYBOOK="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main function
main
