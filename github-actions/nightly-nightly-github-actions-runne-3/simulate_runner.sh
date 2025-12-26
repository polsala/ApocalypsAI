#!/bin/bash

# Nightly GitHub Actions Runner Simulator
# Simulates GitHub Actions workflows locally for testing

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_DIR="${SCRIPT_DIR}/.nightly_simulator_temp"
DEBUG=false
ENV_FILE=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Supported actions
SUPPORTED_ACTIONS=(
    "actions/checkout"
    "actions/setup-node"
    "actions/setup-python"
    "actions/setup-go"
    "actions/cache"
    "docker/build-push-action"
    "docker/login-action"
)

# Usage function
usage() {
    cat << EOF
Usage: $0 [OPTIONS] WORKFLOW_FILE

Simulate GitHub Actions workflow locally.

OPTIONS:
    -d, --debug           Enable debug output
    -e, --env-file FILE   Load environment variables from file
    -h, --help            Show this help message

EXAMPLES:
    $0 .github/workflows/deploy.yml
    $0 --debug .github/workflows/test.yml
    $0 --env-file .env.local .github/workflows/build.yml

EOF
}

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    if [[ "$DEBUG" == "true" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $1"
    fi
}

# Cleanup function
cleanup() {
    log_debug "Cleaning up temporary directory: $TEMP_DIR"
    rm -rf "$TEMP_DIR"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--debug)
            DEBUG=true
            shift
            ;;
        -e|--env-file)
            ENV_FILE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            WORKFLOW_FILE="$1"
            shift
            ;;
    esac
done

# Check if workflow file is provided
if [[ -z "${WORKFLOW_FILE:-}" ]]; then
    log_error "Workflow file is required"
    usage
    exit 1
fi

# Check if workflow file exists
if [[ ! -f "$WORKFLOW_FILE" ]]; then
    log_error "Workflow file not found: $WORKFLOW_FILE"
    exit 1
fi

# Load environment file if provided
if [[ -n "$ENV_FILE" ]]; then
    if [[ -f "$ENV_FILE" ]]; then
        log_info "Loading environment from: $ENV_FILE"
        set -a
        source "$ENV_FILE"
        set +a
    else
        log_warning "Environment file not found: $ENV_FILE"
    fi
fi

# Setup trap for cleanup
trap cleanup EXIT

# Create temporary directory
mkdir -p "$TEMP_DIR"

log_info "Starting GitHub Actions simulation for: $WORKFLOW_FILE"
log_debug "Temporary directory: $TEMP_DIR"
log_debug "Debug mode: $DEBUG"

# Function to check if action is supported
is_supported_action() {
    local action_name="$1"
    for supported in "${SUPPORTED_ACTIONS[@]}"; do
        if [[ "$action_name" == "$supported"* ]]; then
            return 0
        fi
    done
    return 1
}

# Function to simulate checkout action
simulate_checkout() {
    local repo_url="$1"
    local ref="$2"
    local path="$3"
    
    log_info "Simulating checkout: $repo_url@$ref"
    
    if [[ -n "$path" ]]; then
        mkdir -p "$path"
        cd "$path"
    fi
    
    if [[ -d ".git" ]]; then
        log_info "Repository already exists, pulling latest changes"
        git pull --quiet || log_warning "Failed to pull, repository might be modified"
    else
        log_info "Cloning repository"
        git clone --depth 1 --single-branch ${ref:+--branch $ref} "$repo_url" . || {
            log_error "Failed to clone repository"
            return 1
        }
    fi
    
    log_success "Checkout completed"
}

# Function to simulate setup-node action
simulate_setup_node() {
    local node_version="$1"
    
    log_info "Simulating setup-node: $node_version"
    
    if command -v node &> /dev/null; then
        current_version=$(node --version)
        log_info "Node.js already installed: $current_version"
    else
        log_warning "Node.js not found, skipping setup"
    fi
    
    log_success "Node.js setup completed"
}

# Function to simulate setup-python action
simulate_setup_python() {
    local python_version="$1"
    
    log_info "Simulating setup-python: $python_version"
    
    if command -v python3 &> /dev/null; then
        current_version=$(python3 --version)
        log_info "Python already installed: $current_version"
    else
        log_warning "Python not found, skipping setup"
    fi
    
    log_success "Python setup completed"
}

# Function to simulate cache action
simulate_cache() {
    local path="$1"
    local key="$2"
    
    log_info "Simulating cache: $path with key $key"
    
    cache_dir="$TEMP_DIR/cache/$key"
    mkdir -p "$cache_dir"
    
    if [[ -d "$path" ]]; then
        log_info "Caching directory: $path"
        cp -r "$path"/* "$cache_dir/" 2>/dev/null || true
        log_success "Cache saved"
    else
        log_info "Cache miss, directory not found: $path"
    fi
}

# Function to simulate docker actions
simulate_docker() {
    local action_name="$1"
    
    log_info "Simulating Docker action: $action_name"
    
    if command -v docker &> /dev/null; then
        log_info "Docker is available"
    else
        log_warning "Docker not found, skipping"
        return 0
    fi
    
    case "$action_name" in
        "docker/login-action")
            log_info "Simulating Docker login"
            ;;
        "docker/build-push-action")
            log_info "Simulating Docker build and push"
            ;;
    esac
    
    log_success "Docker action completed"
}

# Function to parse and simulate workflow
simulate_workflow() {
    local workflow_file="$1"
    
    log_info "Parsing workflow file: $workflow_file"
    
    # Check if yq is available for YAML parsing
    if ! command -v yq &> /dev/null; then
        log_warning "yq not found, using basic parsing. Install yq for better YAML support."
        log_info "Please install yq: https://github.com/mikefarah/yq"
        return 1
    fi
    
    # Extract jobs from workflow
    local jobs
    jobs=$(yq '.jobs | keys | .[]' "$workflow_file" 2>/dev/null || echo "")
    
    if [[ -z "$jobs" ]]; then
        log_error "No jobs found in workflow file"
        return 1
    fi
    
    log_info "Found jobs: $jobs"
    
    # Process each job
    for job_name in $jobs; do
        log_info "Processing job: $job_name"
        
        # Extract steps for this job
        local steps
        steps=$(yq ".jobs.$job_name.steps[] | .uses // .run" "$workflow_file" 2>/dev/null || echo "")
        
        if [[ -z "$steps" ]]; then
            log_warning "No steps found for job: $job_name"
            continue
        fi
        
        # Process each step
        while IFS= read -r step; do
            if [[ -z "$step" ]]; then
                continue
            fi
            
            log_debug "Processing step: $step"
            
            # Check if it's an action (contains '/')
            if [[ "$step" == *"/"* ]]; then
                # It's an action
                if is_supported_action "$step"; then
                    log_info "Executing supported action: $step"
                    
                    case "$step" in
                        "actions/checkout"*)
                            # Extract parameters
                            local repo_url ref path
                            repo_url=$(yq ".jobs.$job_name.steps[] | select(.uses == \"$step\") | .with.repository // \"$GITHUB_REPOSITORY\"" "$workflow_file" 2>/dev/null || echo "")
                            ref=$(yq ".jobs.$job_name.steps[] | select(.uses == \"$step\") | .with.ref // \"$GITHUB_REF\"" "$workflow_file" 2>/dev/null || echo "")
                            path=$(yq ".jobs.$job_name.steps[] | select(.uses == \"$step\") | .with.path // \"\"" "$workflow_file" 2>/dev/null || echo "")
                            simulate_checkout "$repo_url" "$ref" "$path"
                            ;;
                        "actions/setup-node"*)
                            local node_version
                            node_version=$(yq ".jobs.$job_name.steps[] | select(.uses == \"$step\") | .with.node-version // \"16\"" "$workflow_file" 2>/dev/null || echo "16")
                            simulate_setup_node "$node_version"
                            ;;
                        "actions/setup-python"*)
                            local python_version
                            python_version=$(yq ".jobs.$job_name.steps[] | select(.uses == \"$step\") | .with.python-version // \"3.9\"" "$workflow_file" 2>/dev/null || echo "3.9")
                            simulate_setup_python "$python_version"
                            ;;
                        "actions/cache"*)
                            local path key
                            path=$(yq ".jobs.$job_name.steps[] | select(.uses == \"$step\") | .with.path" "$workflow_file" 2>/dev/null || echo "")
                            key=$(yq ".jobs.$job_name.steps[] | select(.uses == \"$step\") | .with.key" "$workflow_file" 2>/dev/null || echo "")
                            simulate_cache "$path" "$key"
                            ;;
                        "docker/login-action"*)
                            simulate_docker "docker/login-action"
                            ;;
                        "docker/build-push-action"*)
                            simulate_docker "docker/build-push-action"
                            ;;
                        *)
                            log_warning "Action not fully supported, simulating as generic action: $step"
                            ;;
                    esac
                else
                    log_warning "Unsupported action: $step"
                    log_info "Add support for this action by extending the SUPPORTED_ACTIONS array"
                fi
            else
                # It's a run command
                log_info "Executing command: $step"
                if [[ "$DEBUG" == "true" ]]; then
                    log_debug "Running in directory: $(pwd)"
                    log_debug "Environment: $(env | grep -E '^(GITHUB_|CI|RUNNER_)' | head -10)"
                fi
                
                # Execute the command
                eval "$step" || {
                    log_error "Command failed: $step"
                    return 1
                }
            fi
        done <<< "$steps"
        
        log_success "Job completed: $job_name"
    done
}

# Main execution
main() {
    log_info "=== Nightly GitHub Actions Runner Simulator ==="
    log_info "Workflow: $WORKFLOW_FILE"
    log_info "Debug: $DEBUG"
    log_info "Environment file: ${ENV_FILE:-none}"
    echo
    
    # Run the simulation
    if simulate_workflow "$WORKFLOW_FILE"; then
        log_success "Workflow simulation completed successfully!"
        echo
        log_info "Note: This was a simulation. No actual GitHub Actions were triggered."
        log_info "To run the real workflow, commit and push your changes to GitHub."
    else
        log_error "Workflow simulation failed!"
        echo
        log_info "Check the output above for errors and fix your workflow file."
        exit 1
    fi
}

# Run main function
main
