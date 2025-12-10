#!/bin/bash

# Nightly Ansible Chaos Orchestrator
# Usage: ./run_chaos.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAYBOOK="${SCRIPT_DIR}/chaos_orchestrator.yml"
INVENTORY="${SCRIPT_DIR}/inventory.ini"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${RED}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                 Chaos Engineering Suite                    ║"
    echo "║                    ApocalypsAI Edition                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

check_requirements() {
    if ! command -v ansible &> /dev/null; then
        echo -e "${RED}Error: Ansible is not installed. Please install it first.${NC}"
        echo "Run: pip install ansible"
        exit 1
    fi

    if [ ! -f "$INVENTORY" ]; then
        echo -e "${RED}Error: Inventory file not found at $INVENTORY${NC}"
        exit 1
    fi

    if [ ! -f "$PLAYBOOK" ]; then
        echo -e "${RED}Error: Playbook not found at $PLAYBOOK${NC}"
        exit 1
    fi
}

check_safety() {
    echo -e "${YELLOW}Safety Check:${NC}"
    echo "This tool is designed for testing environments only."
    echo ""
    read -p "Are you sure you want to proceed? (yes/no): " -r
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Aborted by user."
        exit 1
    fi
    echo ""
}

run_chaos() {
    echo -e "${GREEN}Running chaos engineering playbook...${NC}"
    ansible-playbook -i "$INVENTORY" "$PLAYBOOK" --ask-become-pass
}

main() {
    print_banner
    check_requirements
    check_safety
    run_chaos
}

main "$@"
