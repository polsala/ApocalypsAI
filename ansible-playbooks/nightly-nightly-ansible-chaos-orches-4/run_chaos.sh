#!/bin/bash

# Nightly Ansible Chaos Orchestrator Runner
# Usage: ./run_chaos.sh [inventory] [chaos_duration] [chaos_intensity]

set -e

INVENTORY=${1:-"inventory.ini"}
CHAOS_DURATION=${2:-60}
CHAOS_INTENSITY=${3:-"medium"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Nightly Ansible Chaos Orchestrator ===${NC}"
echo -e "Inventory: ${YELLOW}${INVENTORY}${NC}"
echo -e "Duration: ${YELLOW}${CHAOS_DURATION}s${NC}"
echo -e "Intensity: ${YELLOW}${CHAOS_INTENSITY}${NC}"
echo

# Validate inventory file exists
if [ ! -f "${INVENTORY}" ]; then
    echo -e "${RED}Error: Inventory file '${INVENTORY}' not found!${NC}"
    echo "Please create an inventory file or specify one with: ./run_chaos.sh <inventory_file>"
    exit 1
fi

# Validate chaos intensity
VALID_INTENSITIES=("low" "medium" "high")
VALID=false
for intensity in "${VALID_INTENSITIES[@]}"; do
    if [ "${CHAOS_INTENSITY}" = "${intensity}" ]; then
        VALID=true
        break
    fi
done

if [ "${VALID}" = false ]; then
    echo -e "${RED}Error: Invalid chaos intensity '${CHAOS_INTENSITY}'${NC}"
    echo "Valid intensities: low, medium, high"
    exit 1
fi

# Run the chaos playbook
ansible-playbook -i "${INVENTORY}" chaos_orchestrator.yml \
    --extra-vars "chaos_enabled=true chaos_duration=${CHAOS_DURATION} chaos_intensity=${CHAOS_INTENSITY}"

EXIT_CODE=$?

if [ ${EXIT_CODE} -eq 0 ]; then
    echo -e "\n${GREEN}=== Chaos Engineering Complete! ===${NC}"
    echo -e "${GREEN}Systems tested for resilience successfully!${NC}"
else
    echo -e "\n${RED}=== Chaos Engineering Failed! ===${NC}"
    echo -e "${RED}Please check the logs above for details.${NC}"
    exit ${EXIT_CODE}
fi
