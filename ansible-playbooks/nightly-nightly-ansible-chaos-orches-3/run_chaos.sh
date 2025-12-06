#!/bin/bash

# Nightly Ansible Chaos Orchestrator Runner
# Usage: ./run_chaos.sh [options]

set -e

# Default values
CHAOS_DURATION=30
CHAOS_INTENSITY="medium"
CHAOS_SCENARIOS="network,resource,service,time,random"
INVENTORY="inventory"
LIMIT=""
DRY_RUN=false
VERBOSE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -d, --duration DURATION    Chaos duration in seconds (1-300, default: 30)"
    echo "  -i, --intensity LEVEL      Chaos intensity: low, medium, high (default: medium)"
    echo "  -s, --scenarios SCENARIOS  Comma-separated chaos scenarios (default: all)"
    echo "  -I, --inventory FILE       Inventory file (default: inventory)"
    echo "  -l, --limit HOSTS          Limit to specific hosts/groups"
    echo "  -n, --dry-run             Perform a dry run without actual chaos"
    echo "  -v, --verbose             Enable verbose output"
    echo "  -h, --help                Show this help message"
    echo ""
    echo "Chaos Scenarios: network, resource, service, time, random"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Run all scenarios with medium intensity"
    echo "  $0 -d 60 -i high                    # Run with high intensity for 60 seconds"
    echo "  $0 -s network,resource              # Run only network and resource chaos"
    echo "  $0 -l production -i low             # Run low intensity chaos on production hosts"
    echo "  $0 -n -v                            # Perform a verbose dry run"
}

print_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              Nightly Ansible Chaos Orchestrator            ║"
    echo "║                    Embrace the Chaos!                      ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

validate_inputs() {
    # Validate duration
    if ! [[ "$CHAOS_DURATION" =~ ^[0-9]+$ ]] || [ "$CHAOS_DURATION" -lt 1 ] || [ "$CHAOS_DURATION" -gt 300 ]; then
        echo -e "${RED}Error: Chaos duration must be a number between 1 and 300${NC}"
        exit 1
    fi
    
    # Validate intensity
    if [[ ! "$CHAOS_INTENSITY" =~ ^(low|medium|high)$ ]]; then
        echo -e "${RED}Error: Chaos intensity must be one of: low, medium, high${NC}"
        exit 1
    fi
    
    # Validate inventory file
    if [ ! -f "$INVENTORY" ]; then
        echo -e "${RED}Error: Inventory file '$INVENTORY' not found${NC}"
        exit 1
    fi
}

build_extra_vars() {
    local extra_vars=""
    
    # Add duration
    extra_vars+="chaos_duration=$CHAOS_DURATION "
    
    # Add intensity
    extra_vars+="chaos_intensity=$CHAOS_INTENSITY "
    
    # Add scenarios
    IFS=',' read -ra SCENARIO_ARRAY <<< "$CHAOS_SCENARIOS"
    scenario_json="["
    for scenario in "${SCENARIO_ARRAY[@]}"; do
        scenario=$(echo "$scenario" | xargs) # trim whitespace
        if [[ ! "$scenario" =~ ^(network|resource|service|time|random)$ ]]; then
            echo -e "${RED}Error: Invalid scenario '$scenario'. Valid scenarios: network, resource, service, time, random${NC}"
            exit 1
        fi
        scenario_json+="\"$scenario\","
    done
    scenario_json="${scenario_json%,}]" # remove trailing comma
    extra_vars+="chaos_scenarios='$scenario_json' "
    
    # Add dry run flag
    if [ "$DRY_RUN" = true ]; then
        extra_vars+="chaos_enabled=false "
        extra_vars+="cleanup_enabled=false "
        extra_vars+="report_enabled=false "
    fi
    
    echo "$extra_vars"
}

run_playbook() {
    local extra_vars="$1"
    local ansible_cmd="ansible-playbook chaos_orchestrator.yml "
    
    # Add inventory
    ansible_cmd+="-i $INVENTORY "
    
    # Add limit if specified
    if [ -n "$LIMIT" ]; then
        ansible_cmd+="--limit $LIMIT "
    fi
    
    # Add verbosity
    if [ "$VERBOSE" = true ]; then
        ansible_cmd+="-vvv "
    fi
    
    # Add extra variables
    ansible_cmd+="-e '$extra_vars'"
    
    echo -e "${GREEN}Running chaos playbook...${NC}"
    echo -e "${YELLOW}Command: $ansible_cmd${NC}"
    echo ""
    
    # Execute the playbook
    eval $ansible_cmd
}

show_summary() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                        Chaos Summary                         ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo -e "${BLUE}Chaos Duration:${NC} $CHAOS_DURATION seconds"
    echo -e "${BLUE}Chaos Intensity:${NC} $CHAOS_INTENSITY"
    echo -e "${BLUE}Chaos Scenarios:${NC} $CHAOS_SCENARIOS"
    echo -e "${BLUE}Inventory:${NC} $INVENTORY"
    if [ -n "$LIMIT" ]; then
        echo -e "${BLUE}Limit:${NC} $LIMIT"
    fi
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}Mode: DRY RUN (no actual chaos executed)${NC}"
    fi
    echo ""
    echo -e "${BLUE}Reports will be generated in: /tmp/chaos_working/${NC}"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--duration)
            CHAOS_DURATION="$2"
            shift 2
            ;;
        -i|--intensity)
            CHAOS_INTENSITY="$2"
            shift 2
            ;;
        -s|--scenarios)
            CHAOS_SCENARIOS="$2"
            shift 2
            ;;
        -I|--inventory)
            INVENTORY="$2"
            shift 2
            ;;
        -l|--limit)
            LIMIT="$2"
            shift 2
            ;;
        -n|--dry-run)
            DRY_RUN=true
            shift
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
            echo -e "${RED}Unknown option: $1${NC}"
            print_usage
            exit 1
            ;;
esac
done

# Main execution
print_banner
validate_inputs
show_summary

EXTRA_VARS=$(build_extra_vars)
run_playbook "$EXTRA_VARS"

if [ "$DRY_RUN" = false ]; then
    echo ""
    echo -e "${GREEN}Chaos engineering experiment completed successfully!${NC}"
    echo -e "${BLUE}Check the generated reports in /tmp/chaos_working/ for detailed results.${NC}"
else
    echo ""
    echo -e "${YELLOW}Dry run completed. No actual chaos was executed.${NC}"
fi
