#!/bin/bash

# Nightly Bash Quickstart Generator
# Generates project quickstart guides from template files

set -euo pipefail

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
TEMPLATE_FILE=""
OUTPUT_FILE="quickstart.md"
INTERACTIVE_MODE=false
BATCH_DIR=""
OUTPUT_DIR=""
VALUES_FILE=""
VERBOSE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Help function
show_help() {
    cat << EOF
Nightly Bash Quickstart Generator

Generates project quickstart guides from template files with customizable placeholders.

Usage: $0 [OPTIONS]

OPTIONS:
    --template <file>     Input template file
    --output <file>       Output file (default: quickstart.md)
    --interactive         Run in interactive mode
    --batch <dir>         Process all templates in directory
    --output-dir <dir>    Output directory for batch mode
    --values <file>       JSON file with placeholder values
    --verbose             Enable verbose output
    --help                Show this help message

EXAMPLES:
    # Generate from template
    $0 --template my-template.md --output quickstart.md

    # Interactive mode
    $0 --interactive

    # Batch processing
    $0 --batch templates/ --output-dir guides/

    # With values file
    $0 --template template.md --values config.json

EOF
}

# Check dependencies
check_dependencies() {
    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed."
        log_info "Install with: sudo apt-get install jq (Ubuntu/Debian) or brew install jq (macOS)"
        exit 1
    fi
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --template)
                TEMPLATE_FILE="$2"
                shift 2
                ;;
            --output)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            --interactive)
                INTERACTIVE_MODE=true
                shift
                ;;
            --batch)
                BATCH_DIR="$2"
                shift 2
                ;;
            --output-dir)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            --values)
                VALUES_FILE="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Interactive mode - prompt user for inputs
interactive_mode() {
    log_info "Entering interactive mode..."

    # Get template file
    while [[ -z "$TEMPLATE_FILE" ]] || [[ ! -f "$TEMPLATE_FILE" ]]; do
        read -rp "Enter template file path: " TEMPLATE_FILE
        if [[ ! -f "$TEMPLATE_FILE" ]]; then
            log_error "Template file not found: $TEMPLATE_FILE"
        fi
    done

    # Get output file
    read -rp "Enter output file path [$OUTPUT_FILE]: " user_output
    if [[ -n "$user_output" ]]; then
        OUTPUT_FILE="$user_output"
    fi

    # Check if values file exists
    read -rp "Enter values JSON file path (leave empty to skip): " VALUES_FILE
    if [[ -n "$VALUES_FILE" ]] && [[ ! -f "$VALUES_FILE" ]]; then
        log_warning "Values file not found: $VALUES_FILE"
        VALUES_FILE=""
    fi
}

# Extract placeholders from template
extract_placeholders() {
    local template="$1"
    grep -o '{{[^}]*}}' "$template" | sed 's/{{//g; s/}}//g' | sort | uniq
}

# Get user input for a placeholder
get_placeholder_value() {
    local placeholder="$1"
    local default_value="$2"
    local value=""

    if [[ "$INTERACTIVE_MODE" == "true" ]]; then
        if [[ -n "$default_value" ]]; then
            read -rp "Enter value for $placeholder [$default_value]: " value
            if [[ -z "$value" ]]; then
                value="$default_value"
            fi
        else
            read -rp "Enter value for $placeholder: " value
        fi
    else
        value="$default_value"
    fi

    echo "$value"
}

# Load values from JSON file
load_values_from_json() {
    local json_file="$1"
    local placeholder="$2"

    if [[ -f "$json_file" ]]; then
        jq -r ".$placeholder // empty" "$json_file" 2>/dev/null || echo ""
    else
        echo ""
    fi
}

# Replace placeholders in template
replace_placeholders() {
    local template="$1"
    local output="$2"
    local temp_file="$output.tmp"

    # Copy template to temp file
    cp "$template" "$temp_file"

    # Get all placeholders
    local placeholders
    placeholders=$(extract_placeholders "$template")

    if [[ -z "$placeholders" ]]; then
        log_warning "No placeholders found in template."
        mv "$temp_file" "$output"
        return 0
    fi

    # Process each placeholder
    while IFS= read -r placeholder; do
        if [[ -z "$placeholder" ]]; then
            continue
        fi

        # Try to get value from JSON file first
        local value=""
        if [[ -n "$VALUES_FILE" ]]; then
            value=$(load_values_from_json "$VALUES_FILE" "$placeholder")
        fi

        # If not found in JSON or interactive mode, prompt user
        if [[ -z "$value" ]] && [[ "$INTERACTIVE_MODE" == "true" ]]; then
            value=$(get_placeholder_value "$placeholder" "")
        fi

        # If still empty, use default or leave placeholder
        if [[ -z "$value" ]]; then
            value="{{${placeholder}}}"
            log_warning "No value provided for placeholder: $placeholder"
        fi

        # Replace placeholder in temp file
        sed -i "s/{{${placeholder}}}/${value//\/\\}/g" "$temp_file"

        if [[ "$VERBOSE" == "true" ]]; then
            log_info "Replaced $placeholder with: $value"
        fi

    done <<< "$placeholders"

    # Move temp file to output
    mv "$temp_file" "$output"
}

# Process single template
process_template() {
    local template="$1"
    local output="$2"

    if [[ ! -f "$template" ]]; then
        log_error "Template file not found: $template"
        return 1
    fi

    log_info "Processing template: $template"
    log_info "Output file: $output"

    # Create output directory if it doesn't exist
    mkdir -p "$(dirname "$output")"

    # Replace placeholders
    replace_placeholders "$template" "$output"

    log_success "Generated quickstart guide: $output"
}

# Process batch of templates
process_batch() {
    local batch_dir="$1"
    local output_dir="$2"

    if [[ ! -d "$batch_dir" ]]; then
        log_error "Batch directory not found: $batch_dir"
        return 1
    fi

    # Create output directory
    mkdir -p "$output_dir"

    local count=0
    local processed=0

    # Find all template files
    while IFS= read -r -d '' template; do
        count=$((count + 1))
        local filename="$(basename "$template")"
        local output_name="${filename%.*}_quickstart.md"
        local output_path="$output_dir/$output_name"

        if process_template "$template" "$output_path"; then
            processed=$((processed + 1))
        fi
    done < <(find "$batch_dir" -name '*.md' -o -name '*.txt' -o -name '*.template' -print0)

    log_success "Batch processing complete: $processed/$count templates processed"
}

# Main function
main() {
    # Check dependencies
    check_dependencies

    # Parse arguments
    parse_args "$@"

    # Handle interactive mode
    if [[ "$INTERACTIVE_MODE" == "true" ]]; then
        interactive_mode
    fi

    # Validate inputs
    if [[ -n "$BATCH_DIR" ]]; then
        if [[ -z "$OUTPUT_DIR" ]]; then
            log_error "Output directory required for batch mode"
            exit 1
        fi
        process_batch "$BATCH_DIR" "$OUTPUT_DIR"
    elif [[ -n "$TEMPLATE_FILE" ]]; then
        process_template "$TEMPLATE_FILE" "$OUTPUT_FILE"
    else
        log_error "No template specified. Use --template or --interactive"
        show_help
        exit 1
    fi
}

# Run main function with all arguments
main "$@"
