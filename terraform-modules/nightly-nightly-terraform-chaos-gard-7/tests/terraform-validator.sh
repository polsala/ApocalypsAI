#!/bin/bash

# Terraform Validator Script for Chaos Garden Orchestrator
# This script validates the Terraform configuration and runs basic tests

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Check if Terraform is installed
check_terraform() {
    if ! command -v terraform &> /dev/null; then
        error "Terraform is not installed. Please install Terraform first."
        exit 1
    fi
    
    TERRAFORM_VERSION=$(terraform version -json | jq -r '.terraform_version')
    log "Terraform version: $TERRAFORM_VERSION"
}

# Validate Terraform configuration
validate_terraform() {
    log "Validating Terraform configuration..."
    
    cd "$ROOT_DIR"
    
    # Init
    terraform init -backend=false
    
    # Validate
    if terraform validate; then
        log "Terraform configuration is valid!"
    else
        error "Terraform validation failed!"
        exit 1
    fi
}

# Check for required files
check_required_files() {
    log "Checking for required files..."
    
    required_files=(
        "$ROOT_DIR/main.tf"
        "$ROOT_DIR/variables.tf"
        "$ROOT_DIR/outputs.tf"
        "$ROOT_DIR/versions.tf"
        "$ROOT_DIR/README.md"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            error "Required file missing: $file"
            exit 1
        fi
    done
    
    log "All required files present!"
}

# Check for examples
check_examples() {
    log "Checking examples..."
    
    if [[ -d "$ROOT_DIR/examples" ]]; then
        log "Examples directory found"
        
        # Check basic example
        if [[ -d "$ROOT_DIR/examples/basic" ]]; then
            log "Basic example found"
            
            # Validate basic example
            cd "$ROOT_DIR/examples/basic"
            if terraform init -backend=false &> /dev/null && terraform validate &> /dev/null; then
                log "Basic example is valid!"
            else
                warn "Basic example validation failed"
            fi
        else
            warn "Basic example not found"
        fi
    else
        warn "Examples directory not found"
    fi
}

# Check for modules
check_modules() {
    log "Checking for modules..."
    
    if [[ -d "$ROOT_DIR/modules" ]]; then
        log "Modules directory found"
        
        # Check chaos container module
        if [[ -d "$ROOT_DIR/modules/chaos-container" ]]; then
            log "Chaos container module found"
            
            # Check Dockerfile
            if [[ -f "$ROOT_DIR/modules/chaos-container/Dockerfile" ]]; then
                log "Chaos container Dockerfile found"
            else
                warn "Chaos container Dockerfile missing"
            fi
            
            # Check chaos scripts
            if [[ -d "$ROOT_DIR/modules/chaos-container/chaos-scripts" ]]; then
                log "Chaos scripts directory found"
            else
                warn "Chaos scripts directory missing"
            fi
        else
            warn "Chaos container module not found"
        fi
    else
        warn "Modules directory not found"
    fi
}

# Check variable validation
check_variable_validation() {
    log "Checking variable validation..."
    
    # Check if failure_rate has validation
    if grep -q "validation.*failure_rate" "$ROOT_DIR/variables.tf"; then
        log "Failure rate validation found"
    else
        warn "Failure rate validation missing"
    fi
    
    # Check if whimsy_level has validation
    if grep -q "validation.*whimsy_level" "$ROOT_DIR/variables.tf"; then
        log "Whimsy level validation found"
    else
        warn "Whimsy level validation missing"
    fi
}

# Check for security best practices
check_security() {
    log "Checking security best practices..."
    
    # Check for sensitive variables
    if grep -q "sensitive.*=.*true" "$ROOT_DIR/variables.tf"; then
        log "Sensitive variables found"
    else
        warn "No sensitive variables detected"
    fi
    
    # Check for hardcoded secrets (bad practice)
    if grep -r "password\|secret\|key" "$ROOT_DIR" | grep -v "#" | grep -v "\.git" | grep -v "test" | grep -v "example" | grep -v "README"; then
        warn "Potential hardcoded secrets found"
    else
        log "No hardcoded secrets detected"
    fi
}

# Generate summary report
generate_report() {
    log "Generating validation report..."
    
    REPORT_FILE="$ROOT_DIR/validation-report.md"
    
    cat > "$REPORT_FILE" << EOF
# Terraform Validation Report

Generated on: $(date)

## Summary

- Terraform Version: $TERRAFORM_VERSION
- Configuration Status: Valid
- Required Files: Present
- Examples: $(if [[ -d "$ROOT_DIR/examples" ]]; then echo "Present"; else echo "Missing"; fi)
- Modules: $(if [[ -d "$ROOT_DIR/modules" ]]; then echo "Present"; else echo "Missing"; fi)

## Files Checked

- main.tf ✓
- variables.tf ✓
- outputs.tf ✓
- versions.tf ✓
- README.md ✓

## Examples

$(if [[ -d "$ROOT_DIR/examples/basic" ]]; then echo "- Basic example ✓"; else echo "- Basic example ✗"; fi)

## Modules

$(if [[ -d "$ROOT_DIR/modules/chaos-container" ]]; then echo "- Chaos container module ✓"; else echo "- Chaos container module ✗"; fi)

## Security

- Sensitive variables: $(if grep -q "sensitive.*=.*true" "$ROOT_DIR/variables.tf"; then echo "Present ✓"; else echo "Missing ✗"; fi)
- Hardcoded secrets: $(if grep -r "password\|secret\|key" "$ROOT_DIR" | grep -v "#" | grep -v "\.git" | grep -v "test" | grep -v "example" | grep -v "README" > /dev/null; then echo "Found ✗"; else echo "None ✓"; fi)

## Variable Validation

- Failure rate validation: $(if grep -q "validation.*failure_rate" "$ROOT_DIR/variables.tf"; then echo "Present ✓"; else echo "Missing ✗"; fi)
- Whimsy level validation: $(if grep -q "validation.*whimsy_level" "$ROOT_DIR/variables.tf"; then echo "Present ✓"; else echo "Missing ✗"; fi)

---

*This report was generated automatically by the Terraform validator script.*
EOF
    
    log "Validation report saved to: $REPORT_FILE"
}

# Main execution
main() {
    log "Starting Terraform validation for Chaos Garden Orchestrator"
    
    check_terraform
    check_required_files
    validate_terraform
    check_examples
    check_modules
    check_variable_validation
    check_security
    generate_report
    
    log "Terraform validation completed successfully!"
}

# Run main function
main "$@"
