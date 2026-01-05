#!/bin/bash

# Nightly Bash Quickstart Generator
# Generates project quickstart guides from template files

set -euo pipefail

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
TEMPLATE_FILE=""
OUTPUT_FILE=""
CONFIG_FILE="config.json"
INTERACTIVE=false
BATCH=false
TEMPLATES_DIR=""
OUTPUT_DIR=""
VALUES=()

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

# Usage information
usage() {
  cat << EOF
Usage: $0 [OPTIONS]

Generate project quickstart guides from template files.

OPTIONS:
  -t, --template FILE       Template file to process
  -o, --output FILE         Output file path
  -c, --config FILE         Configuration file (default: config.json)
  -i, --interactive         Run in interactive mode
  -b, --batch               Process multiple templates
  -d, --templates-dir DIR   Directory containing templates (for batch mode)
  -D, --output-dir DIR      Directory for output files (for batch mode)
  -v, --values KEY=VALUE    Set placeholder values (can be used multiple times)
  -h, --help                Show this help message

EXAMPLES:
  # Generate a quickstart guide
  $0 --template templates/project-template.md --output docs/QUICKSTART.md

  # Interactive mode
  $0 --interactive

  # Batch processing
  $0 --batch --templates-dir templates/ --output-dir docs/

  # With custom values
  $0 --template template.md --output output.md --values "PROJECT_NAME=My App" "VERSION=1.0"

EOF
}

# Parse command line arguments
parse_args() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      -t|--template)
        TEMPLATE_FILE="$2"
        shift 2
        ;;
      -o|--output)
        OUTPUT_FILE="$2"
        shift 2
        ;;
      -c|--config)
        CONFIG_FILE="$2"
        shift 2
        ;;
      -i|--interactive)
        INTERACTIVE=true
        shift
        ;;
      -b|--batch)
        BATCH=true
        shift
        ;;
      -d|--templates-dir)
        TEMPLATES_DIR="$2"
        shift 2
        ;;
      -D|--output-dir)
        OUTPUT_DIR="$2"
        shift 2
        ;;
      -v|--values)
        VALUES+=("$2")
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        log_error "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
  done
}

# Check dependencies
check_dependencies() {
  local missing_deps=()
  
  command -v jq >/dev/null 2>&1 || missing_deps+=("jq")
  command -v sed >/dev/null 2>&1 || missing_deps+=("sed")
  command -v awk >/dev/null 2>&1 || missing_deps+=("awk")
  
  if [[ ${#missing_deps[@]} -gt 0 ]]; then
    log_error "Missing required dependencies: ${missing_deps[*]}"
    log_info "Please install them using your package manager."
    exit 1
  fi
}

# Load configuration from JSON file
load_config() {
  if [[ -f "$CONFIG_FILE" ]]; then
    log_info "Loading configuration from $CONFIG_FILE"
    if ! jq -e '.' "$CONFIG_FILE" >/dev/null 2>&1; then
      log_error "Invalid JSON in configuration file: $CONFIG_FILE"
      exit 1
    fi
    return 0
  else
    log_warning "Configuration file not found: $CONFIG_FILE"
    log_info "Creating default configuration file..."
    create_default_config "$CONFIG_FILE"
    return 0
  fi
}

# Create default configuration file
create_default_config() {
  local config_file="$1"
  cat > "$config_file" << 'EOF'
{
  "PROJECT_NAME": "My Project",
  "VERSION": "1.0.0",
  "AUTHOR": "Developer",
  "EMAIL": "dev@example.com",
  "DESCRIPTION": "A sample project",
  "INSTALL_COMMAND": "npm install",
  "USAGE_EXAMPLE": "npm start",
  "PREREQUISITE_1": "Node.js 16+",
  "PREREQUISITE_2": "npm 8+",
  "SUPPORT_EMAIL": "support@example.com"
}
EOF
  log_success "Created default configuration: $config_file"
}

# Get value from config or environment
get_value() {
  local key="$1"
  local default_value="$2"
  
  # Check command line values first
  for value in "${VALUES[@]}"; do
    if [[ "$value" == "$key="* ]]; then
      echo "${value#*=}"
      return 0
    fi
  done
  
  # Check config file
  if [[ -f "$CONFIG_FILE" ]]; then
    local config_value
    config_value=$(jq -r --arg key "$key" '.[$key] // empty' "$CONFIG_FILE" 2>/dev/null || echo "")
    if [[ -n "$config_value" && "$config_value" != "null" ]]; then
      echo "$config_value"
      return 0
    fi
  fi
  
  # Check environment variables
  local env_var="QUICKSTART_${key}"
  if [[ -n "${!env_var:-}" ]]; then
    echo "${!env_var}"
    return 0
  fi
  
  # Return default
  echo "$default_value"
}

# Interactive mode for setting values
interactive_mode() {
  log_info "Entering interactive mode..."
  
  # Get template file
  if [[ -z "$TEMPLATE_FILE" ]]; then
    echo -n "Enter template file path: "
    read -r TEMPLATE_FILE
  fi
  
  # Get output file
  if [[ -z "$OUTPUT_FILE" ]]; then
    echo -n "Enter output file path: "
    read -r OUTPUT_FILE
  fi
  
  # Get values interactively
  local keys=("PROJECT_NAME" "VERSION" "AUTHOR" "EMAIL" "DESCRIPTION")
  for key in "${keys[@]}"; do
    local current_value
    current_value=$(get_value "$key" "")
    echo -n "Enter value for $key [$current_value]: "
    read -r input_value
    if [[ -n "$input_value" ]]; then
      VALUES+=("$key=$input_value")
    fi
  done
}

# Process a single template file
process_template() {
  local template_file="$1"
  local output_file="$2"
  
  if [[ ! -f "$template_file" ]]; then
    log_error "Template file not found: $template_file"
    return 1
  fi
  
  log_info "Processing template: $template_file"
  log_info "Output file: $output_file"
  
  # Create output directory if it doesn't exist
  mkdir -p "$(dirname "$output_file")"
  
  # Copy template to output
  cp "$template_file" "$output_file"
  
  # Find all placeholders in the template
  local placeholders
  placeholders=$(grep -o '{{[A-Z_][A-Z0-9_]*}}' "$template_file" | sed 's/{{//g; s/}}//g' | sort -u)
  
  # Replace each placeholder
  while IFS= read -r placeholder; do
    if [[ -n "$placeholder" ]]; then
      local value
      value=$(get_value "$placeholder" "")
      
      if [[ -z "$value" ]]; then
        log_warning "No value found for placeholder: $placeholder"
        value="[VALUE_NOT_SET]"
      fi
      
      # Escape special characters for sed
      local escaped_value
      escaped_value=$(printf '%s' "$value" | sed 's/[&\/]/\\&/g')
      
      # Replace placeholder in output file
      sed -i "s/{{${placeholder}}}/${escaped_value}/g" "$output_file"
      
      log_info "Replaced $placeholder with: $value"
    fi
  done <<< "$placeholders"
  
  log_success "Generated: $output_file"
}

# Batch processing mode
batch_mode() {
  if [[ -z "$TEMPLATES_DIR" ]]; then
    log_error "Templates directory not specified for batch mode"
    exit 1
  fi
  
  if [[ -z "$OUTPUT_DIR" ]]; then
    log_error "Output directory not specified for batch mode"
    exit 1
  fi
  
  if [[ ! -d "$TEMPLATES_DIR" ]]; then
    log_error "Templates directory not found: $TEMPLATES_DIR"
    exit 1
  fi
  
  mkdir -p "$OUTPUT_DIR"
  
  local processed=0
  local failed=0
  
  # Process all template files
  while IFS= read -r -d '' template_file; do
    local filename
    filename="$(basename "$template_file")"
    local output_file="$OUTPUT_DIR/${filename%.*}-quickstart.${filename##*.}"
    
    if process_template "$template_file" "$output_file"; then
      ((processed++))
    else
      ((failed++))
    fi
  done < <(find "$TEMPLATES_DIR" -name '*.md' -type f -print0)
  
  log_success "Batch processing complete: $processed processed, $failed failed"
}

# Validate template file
validate_template() {
  local template_file="$1"
  
  if [[ ! -f "$template_file" ]]; then
    log_error "Template file not found: $template_file"
    return 1
  fi
  
  # Check if file has placeholders
  if ! grep -q '{{[A-Z_][A-Z0-9_]*}}' "$template_file"; then
    log_warning "No placeholders found in template: $template_file"
  fi
  
  return 0
}

# Main execution function
main() {
  log_info "Nightly Bash Quickstart Generator"
  log_info "=================================="
  
  # Parse arguments
  parse_args "$@"
  
  # Check dependencies
  check_dependencies
  
  # Load configuration
  load_config
  
  # Handle interactive mode
  if [[ "$INTERACTIVE" == "true" ]]; then
    interactive_mode
  fi
  
  # Handle batch mode
  if [[ "$BATCH" == "true" ]]; then
    batch_mode
    exit 0
  fi
  
  # Validate inputs
  if [[ -z "$TEMPLATE_FILE" ]]; then
    log_error "Template file is required"
    usage
    exit 1
  fi
  
  if [[ -z "$OUTPUT_FILE" ]]; then
    log_error "Output file is required"
    usage
    exit 1
  fi
  
  # Validate template
  if ! validate_template "$TEMPLATE_FILE"; then
    exit 1
  fi
  
  # Process template
  if process_template "$TEMPLATE_FILE" "$OUTPUT_FILE"; then
    log_success "Quickstart guide generated successfully!"
  else
    log_error "Failed to generate quickstart guide"
    exit 1
  fi
}

# Run main function with all arguments
main "$@"
