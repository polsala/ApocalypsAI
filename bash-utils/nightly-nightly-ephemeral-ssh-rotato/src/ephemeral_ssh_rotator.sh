#!/bin/bash

# Nightly Ephemeral SSH Rotator
# Generates and rotates ephemeral SSH key pairs with automatic cleanup
# Author: ApocalypsAI
# License: MIT

set -euo pipefail

# Configuration
KEY_TTL_HOURS=${KEY_TTL_HOURS:-24}
KEY_DIR=${KEY_DIR:-"$HOME/.ephemeral_ssh"}
LOG_FILE=${LOG_FILE:-"$KEY_DIR/audit.log"}
KEY_PREFIX="ephemeral_key"
SSH_KEYGEN=${SSH_KEYGEN:-"ssh-keygen"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level="$1"
    local message="$2"
    local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Print colored output
print_status() {
    local color="$1"
    local message="$2"
    echo -e "${color}$message${NC}"
}

# Print error and exit
error_exit() {
    print_status "$RED" "ERROR: $1"
    log "ERROR" "$1"
    exit 1
}

# Print success message
success() {
    print_status "$GREEN" "✓ $1"
    log "INFO" "SUCCESS: $1"
}

# Print info message
info() {
    print_status "$BLUE" "ℹ $1"
    log "INFO" "$1"
}\n
# Print warning message
warning() {
    print_status "$YELLOW" "⚠ $1"
    log "WARN" "$1"
}

# Ensure directories exist
ensure_dirs() {
    if ! mkdir -p "$KEY_DIR" 2>/dev/null; then
        error_exit "Failed to create directory: $KEY_DIR"
    fi
    # Ensure log file exists
    touch "$LOG_FILE" 2>/dev/null || error_exit "Failed to create log file: $LOG_FILE"
}

# Check dependencies
check_deps() {
    if ! command -v "$SSH_KEYGEN" >/dev/null 2>&1; then
        error_exit "ssh-keygen not found. Please install OpenSSH."
    fi
    
    if ! command -v date >/dev/null 2>&1; then
        error_exit "date command not found."
    fi
}

# Generate unique key name with timestamp
generate_key_name() {
    local timestamp="$(date '+%Y%m%d_%H%M%S')"
    echo "${KEY_PREFIX}_${timestamp}"
}

# Generate SSH key pair
generate_key() {
    ensure_dirs
    check_deps
    
    local key_name="$(generate_key_name)"
    local key_path="$KEY_DIR/$key_name"
    
    info "Generating ephemeral SSH key: $key_name"
    
    # Generate the key pair
    if $SSH_KEYGEN -t rsa -b 4096 -f "$key_path" -N "" -C "ephemeral-key-$(date '+%s')" >/dev/null 2>&1; then
        success "Generated key pair: $key_name"
        log "INFO" "GENERATED key: $key_name"
        
        # Set secure permissions
        chmod 600 "$key_path" 2>/dev/null || warning "Failed to set permissions on private key"
        chmod 644 "$key_path.pub" 2>/dev/null || warning "Failed to set permissions on public key"
        
        # Display key info
        echo
        info "Key details:"
        echo "  Private key: $key_path"
        echo "  Public key:  $key_path.pub"
        echo "  Expires in:  $KEY_TTL_HOURS hours"
        echo "  Fingerprint: $($SSH_KEYGEN -lf "$key_path" | cut -d' ' -f2)"
        echo
        success "Key generation complete!"
    else
        error_exit "Failed to generate SSH key pair"
    fi
}

# Get file age in hours
get_file_age_hours() {
    local file="$1"
    if [[ -f "$file" ]]; then
        local current_time
        local file_time
        local age_seconds
        
        # Get current time in seconds
        current_time=$(date +%s)
        
        # Get file modification time in seconds
        file_time=$(stat -c %Y "$file" 2>/dev/null || stat -f %m "$file" 2>/dev/null || echo "$current_time")
        
        # Calculate age in hours
        age_seconds=$((current_time - file_time))
        echo $((age_seconds / 3600))
    else
        echo "9999" # File doesn't exist, treat as very old
    fi
}

# List all ephemeral keys
list_keys() {
    ensure_dirs
    
    info "Ephemeral SSH keys in $KEY_DIR:"
    echo
    
    local found_keys=false
    for key_file in "$KEY_DIR"/${KEY_PREFIX}_*; do
        if [[ -f "$key_file" ]]; then
            found_keys=true
            local key_name="$(basename "$key_file")"
            local pub_key="$key_file.pub"
            local age_hours
            age_hours=$(get_file_age_hours "$key_file")
            local status="Active"
            
            if [[ $age_hours -ge $KEY_TTL_HOURS ]]; then
                status="Expired"
            fi
            
            echo "  $key_name"
            echo "    Status: $status ($age_hours hours old)"
            echo "    Private: $key_file"
            if [[ -f "$pub_key" ]]; then
                echo "    Public:  $pub_key"
                echo "    Fingerprint: $($SSH_KEYGEN -lf "$key_file" 2>/dev/null | cut -d' ' -f2 || echo 'N/A')"
            else
                echo "    Public:  Missing"
            fi
            echo
        fi
    done
    
    if [[ "$found_keys" == "false" ]]; then
        warning "No ephemeral SSH keys found."
    fi
}

# Clean up expired keys
cleanup_expired() {
    ensure_dirs
    
    info "Cleaning up keys older than $KEY_TTL_HOURS hours..."
    
    local cleaned_count=0
    
    for key_file in "$KEY_DIR"/${KEY_PREFIX}_*; do
        if [[ -f "$key_file" ]]; then
            local key_name="$(basename "$key_file")"
            local age_hours
            age_hours=$(get_file_age_hours "$key_file")
            
            if [[ $age_hours -ge $KEY_TTL_HOURS ]]; then
                local pub_key="$key_file.pub"
                
                # Remove private key
                if rm -f "$key_file" 2>/dev/null; then
                    success "Removed expired private key: $key_name"
                    log "INFO" "REMOVED expired private key: $key_name"
                else
                    error_exit "Failed to remove private key: $key_file"
                fi
                
                # Remove public key if exists
                if [[ -f "$pub_key" ]]; then
                    if rm -f "$pub_key" 2>/dev/null; then
                        success "Removed expired public key: $key_name.pub"
                        log "INFO" "REMOVED expired public key: $key_name.pub"
                    else
                        warning "Failed to remove public key: $pub_key"
                    fi
                fi
                
                cleaned_count=$((cleaned_count + 1))
            fi
        fi
    done
    
    if [[ $cleaned_count -eq 0 ]]; then
        info "No expired keys found."
    else
        success "Cleaned up $cleaned_count expired key(s)."
    fi
}

# Rotate keys (generate new + cleanup old)
rotate_keys() {
    info "Starting key rotation..."
    generate_key
    cleanup_expired
    success "Key rotation complete!"
}

# Show audit log
show_log() {
    ensure_dirs
    
    if [[ -s "$LOG_FILE" ]]; then
        info "Audit log contents:"
        echo
        cat "$LOG_FILE"
    else
        warning "Audit log is empty or does not exist."
    fi
}

# Clear audit log
clear_log() {
    ensure_dirs
    
    if > "$LOG_FILE" 2>/dev/null; then
        success "Cleared audit log."
        log "INFO" "LOG_CLEARED"
    else
        error_exit "Failed to clear audit log."
    fi
}

# Show help
show_help() {
    cat << EOF
Nightly Ephemeral SSH Rotator

USAGE:
    $0 <command> [options]

COMMANDS:
    generate    Generate a new ephemeral SSH key pair
    cleanup     Remove expired SSH keys
    rotate      Generate new key and clean up expired ones
    list        List all ephemeral SSH keys
    log         Show audit log
    clear-log   Clear audit log
    help        Show this help message

OPTIONS:
    --help      Show this help message

ENVIRONMENT VARIABLES:
    KEY_TTL_HOURS   Time-to-live for keys in hours (default: 24)
    KEY_DIR         Directory to store keys (default: ~/.ephemeral_ssh)
    LOG_FILE        Audit log file path (default: ~/.ephemeral_ssh/audit.log)
    SSH_KEYGEN      Path to ssh-keygen command (default: ssh-keygen)

EXAMPLES:
    $0 generate
    $0 rotate
    $0 cleanup
    $0 list
    $0 log
    KEY_TTL_HOURS=12 $0 rotate

EOF
}

# Main function
main() {
    local command="${1:-help}"
    
    case "$command" in
        generate)
            generate_key
            ;;
        cleanup)
            cleanup_expired
            ;;
        rotate)
            rotate_keys
            ;;
        list)
            list_keys
            ;;
        log)
            show_log
            ;;
        clear-log)
            clear_log
            ;;
        --help|-h|help|'')
            show_help
            ;;
        *)
            error_exit "Unknown command: $command. Use '$0 help' for usage."
            ;;
    esac
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
