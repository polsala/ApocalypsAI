#!/bin/bash

# Nightly Ephemeral SSH Key Rotator
# Automates SSH key rotation for ephemeral servers

set -euo pipefail

# Configuration
DEFAULT_KEY_NAME="ephemeral_key"
DEFAULT_KEY_DIR="$HOME/.ssh"
LOG_FILE="/tmp/ssh_key_rotation.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
  log "${RED}ERROR: $1${NC}" >&2
  exit 1
}

# Success message
success() {
  log "${GREEN}SUCCESS: $1${NC}"
}

# Warning message
warning() {
  log "${YELLOW}WARNING: $1${NC}"
}

# Usage information
usage() {
  cat << EOF
Usage: $0 [OPTIONS]

Automates SSH key rotation for ephemeral servers.

OPTIONS:
  -h, --hosts-file FILE   Path to file containing hostnames/IPs (one per line)
  -k, --key-name NAME     Name for the new SSH key pair (default: $DEFAULT_KEY_NAME)
  -d, --key-dir DIR       Directory to store SSH keys (default: $DEFAULT_KEY_DIR)
  -v, --verbose           Enable verbose output
  -h, --help              Show this help message

EXAMPLES:
  $0 --hosts-file hosts.txt --key-name my-key
  $0 -h hosts.txt -k my-key -v

EOF
}

# Parse command line arguments
parse_args() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      -h|--hosts-file)
        HOSTS_FILE="$2"
        shift 2
        ;;
      -k|--key-name)
        KEY_NAME="$2"
        shift 2
        ;;
      -d|--key-dir)
        KEY_DIR="$2"
        shift 2
        ;;
      -v|--verbose)
        VERBOSE=true
        shift
        ;;
      --help)
        usage
        exit 0
        ;;
      *)
        error_exit "Unknown option: $1"
        ;;
    esac
  done
}

# Validate arguments
validate_args() {
  if [[ -z "$HOSTS_FILE" ]]; then
    error_exit "Hosts file is required. Use -h or --hosts-file to specify."
  fi

  if [[ ! -f "$HOSTS_FILE" ]]; then
    error_exit "Hosts file not found: $HOSTS_FILE"
  fi

  if [[ -z "$KEY_NAME" ]]; then
    KEY_NAME="$DEFAULT_KEY_NAME"
  fi

  if [[ -z "$KEY_DIR" ]]; then
    KEY_DIR="$DEFAULT_KEY_DIR"
  fi

  # Create key directory if it doesn't exist
  mkdir -p "$KEY_DIR"
}

# Generate new SSH key pair
generate_key_pair() {
  local key_path="$KEY_DIR/$KEY_NAME"
  local pub_key_path="$key_path.pub"

  if [[ -f "$key_path" ]]; then
    warning "Key already exists: $key_path"
    warning "Backing up existing key..."
    mv "$key_path" "$key_path.backup.$(date +%s)"
    mv "$pub_key_path" "$pub_key_path.backup.$(date +%s)"
  fi

  log "Generating new SSH key pair..."
  ssh-keygen -t rsa -b 4096 -f "$key_path" -N "" -C "ephemeral-key-$(date +%s)" >/dev/null 2>&1

  if [[ $? -eq 0 ]]; then
    success "SSH key pair generated: $key_path"
  else
    error_exit "Failed to generate SSH key pair"
  fi
}

# Get public key content
get_public_key() {
  cat "$KEY_DIR/$KEY_NAME.pub"
}

# Distribute public key to a host
distribute_key_to_host() {
  local host="$1"
  local pub_key="$2"

  log "Distributing key to $host..."

  # Try to copy the key using ssh-copy-id
  if ssh-copy-id -i "$KEY_DIR/$KEY_NAME.pub" "$host" >/dev/null 2>&1; then
    success "Key distributed to $host"
  else
    warning "Failed to distribute key to $host using ssh-copy-id, trying manual method..."
    
    # Manual method: append to authorized_keys
    if ssh -o StrictHostKeyChecking=no "$host" "mkdir -p ~/.ssh && echo '$pub_key' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"; then
      success "Key manually distributed to $host"
    else
      error_exit "Failed to distribute key to $host"
    fi
  fi
}

# Test SSH connection
test_connection() {
  local host="$1"
  local key_path="$2"

  log "Testing connection to $host..."
  
  if ssh -i "$key_path" -o BatchMode=yes -o ConnectTimeout=10 "$host" "echo 'Connection successful'" >/dev/null 2>&1; then
    success "Connection test passed for $host"
    return 0
  else
    warning "Connection test failed for $host"
    return 1
  fi
}

# Clean up old keys from authorized_keys
cleanup_old_keys() {
  local host="$1"
  local pub_key="$2"

  log "Cleaning up old keys from $host..."
  
  # Remove any existing keys with the same comment
  local key_comment=$(echo "$pub_key" | awk '{print $3}')
  
  if ssh -o StrictHostKeyChecking=no "$host" "sed -i '/$key_comment/d' ~/.ssh/authorized_keys"; then
    success "Old keys cleaned up from $host"
  else
    warning "Failed to clean up old keys from $host"
  fi
}

# Main execution function
main() {
  log "Starting SSH key rotation process..."

  # Initialize variables
  HOSTS_FILE=""
  KEY_NAME=""
  KEY_DIR=""
  VERBOSE=false

  # Parse arguments
  parse_args "$@"
  validate_args

  # Generate new key pair
  generate_key_pair
  
  # Get public key content
  PUB_KEY=$(get_public_key)

  # Read hosts and process each one
  success "Processing hosts from: $HOSTS_FILE"
  
  while IFS= read -r host || [[ -n "$host" ]]; do
    # Skip empty lines and comments
    if [[ -z "$host" ]] || [[ "$host" =~ ^#.* ]]; then
      continue
    fi

    log "Processing host: $host"

    # Distribute key
    distribute_key_to_host "$host" "$PUB_KEY"

    # Test connection
    if test_connection "$host" "$KEY_DIR/$KEY_NAME"; then
      # Clean up old keys
      cleanup_old_keys "$host" "$PUB_KEY"
    else
      warning "Skipping cleanup for $host due to connection test failure"
    fi
  done < "$HOSTS_FILE"

  success "SSH key rotation completed successfully!"
  success "Keys stored in: $KEY_DIR/$KEY_NAME"
  success "Log file: $LOG_FILE"
}

# Run main function with all arguments
main "$@"
