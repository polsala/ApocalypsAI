#!/bin/bash

# Nightly Bash Backup Orchestrator
# A whimsical-yet-useful backup utility

set -euo pipefail

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$(dirname "$SCRIPT_DIR")/config"
LOG_DIR="$(dirname "$SCRIPT_DIR")/logs"

# Default configuration
DEFAULT_CONFIG="$CONFIG_DIR/backup_config.conf"
STRATEGY="full"
DRY_RUN=false
VERBOSE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Whimsical messages
WHIMSICAL_MESSAGES=(
  "Backing up your digital treasures like a digital dragon guarding its hoard!"
  "Compressing files with the efficiency of a squirrel preparing for winter!"
  "Encrypting your data with the secrecy of a ninja in a library!"
  "Organizing your files with the precision of a Swiss watchmaker!"
  "Securing your data like a vault in Fort Knox!"
  "Archiving your files with the care of a museum curator!"
  "Protecting your data like a mother bear protects her cubs!"
  "Sorting your files with the speed of a caffeinated librarian!"
  "Backing up with the determination of a determined ant!"
  "Preserving your data like a digital time capsule!"
)

# Logging function
log() {
  local level="$1"
  shift
  local message="$*"
  local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
  
  # Create log directory if it doesn't exist
  mkdir -p "$LOG_DIR"
  
  # Write to log file
  echo "[$timestamp] [$level] $message" >> "$LOG_DIR/backup.log"
  
  # Display to console if verbose or error
  if [[ "$level" == "ERROR" ]] || [[ "$VERBOSE" == true ]]; then
    case "$level" in
      "INFO")
        echo -e "${BLUE}[$timestamp]${NC} $message"
        ;;
      "WARN")
        echo -e "${YELLOW}[$timestamp]${NC} $message"
        ;;
      "ERROR")
        echo -e "${RED}[$timestamp]${NC} $message"
        ;;
      "SUCCESS")
        echo -e "${GREEN}[$timestamp]${NC} $message"
        ;;
      *)
        echo "[$timestamp] $message"
        ;;
    esac
  fi
}

# Whimsical message function
whimsical_message() {
  local random_index=$((RANDOM % ${#WHIMSICAL_MESSAGES[@]}))
  log "INFO" "${WHIMSICAL_MESSAGES[$random_index]}"
}

# Load configuration
load_config() {
  local config_file="$1"
  
  if [[ ! -f "$config_file" ]]; then
    log "ERROR" "Configuration file not found: $config_file"
    exit 1
  fi
  
  # Source the configuration file
  source "$config_file"
  
  log "INFO" "Configuration loaded from: $config_file"
}

# Validate configuration
validate_config() {
  local errors=0
  
  # Check required variables
  [[ -z "${SOURCE_DIRS:-}" ]] && { log "ERROR" "SOURCE_DIRS not configured"; errors=$((errors + 1)); }
  [[ -z "${DESTINATION_DIR:-}" ]] && { log "ERROR" "DESTINATION_DIR not configured"; errors=$((errors + 1)); }
  [[ -z "${RETENTION_DAYS:-}" ]] && { log "ERROR" "RETENTION_DAYS not configured"; errors=$((errors + 1)); }
  
  # Check source directories exist
  if [[ -n "${SOURCE_DIRS:-}" ]]; then
    IFS=',' read -ra dirs <<< "$SOURCE_DIRS"
    for dir in "${dirs[@]}"; do
      if [[ ! -d "$dir" ]]; then
        log "ERROR" "Source directory does not exist: $dir"
        errors=$((errors + 1))
      fi
    done
  fi
  
  # Check destination directory
  if [[ -n "${DESTINATION_DIR:-}" ]] && [[ ! -d "$(dirname "$DESTINATION_DIR")" ]]; then
    log "ERROR" "Destination parent directory does not exist: $(dirname "$DESTINATION_DIR")"
    errors=$((errors + 1))
  fi
  
  # Check encryption if enabled
  if [[ "${ENCRYPT_BACKUP:-false}" == "true" ]] && ! command -v gpg &> /dev/null; then
    log "ERROR" "GPG not found but encryption is enabled"
    errors=$((errors + 1))
  fi
  
  # Check email if enabled
  if [[ "${ENABLE_EMAIL:-false}" == "true" ]] && ! command -v mail &> /dev/null && ! command -v sendmail &> /dev/null; then
    log "ERROR" "Mail command not found but email notifications are enabled"
    errors=$((errors + 1))
  fi
  
  if [[ $errors -gt 0 ]]; then
    log "ERROR" "$errors configuration error(s) found. Please fix and try again."
    exit 1
  fi
  
  log "INFO" "Configuration validation passed"
}

# Create backup directory
create_backup_dir() {
  local backup_dir="$1"
  
  if [[ "$DRY_RUN" == true ]]; then
    log "INFO" "[DRY RUN] Would create backup directory: $backup_dir"
    return 0
  fi
  
  if [[ ! -d "$backup_dir" ]]; then
    mkdir -p "$backup_dir"
    log "INFO" "Created backup directory: $backup_dir"
  fi
}

# Perform full backup
perform_full_backup() {
  local backup_dir="$1"
  local timestamp="$2"
  
  log "INFO" "Starting full backup..."
  whimsical_message
  
  local archive_name="full_backup_$timestamp.tar.gz"
  local archive_path="$backup_dir/$archive_name"
  
  if [[ "$DRY_RUN" == true ]]; then
    log "INFO" "[DRY RUN] Would create full backup: $archive_path"
    return 0
  fi
  
  # Create tar archive
  log "INFO" "Creating archive..."
  if tar -czf "$archive_path" -C / $(echo "$SOURCE_DIRS" | tr ',' ' '); then
    log "SUCCESS" "Full backup created successfully: $archive_path"
    
    # Encrypt if enabled
    if [[ "${ENCRYPT_BACKUP:-false}" == "true" ]]; then
      encrypt_backup "$archive_path"
    fi
    
    # Update full backup marker
    echo "$timestamp" > "$backup_dir/.last_full_backup"
  else
    log "ERROR" "Failed to create full backup"
    return 1
  fi
}

# Perform incremental backup
perform_incremental_backup() {
  local backup_dir="$1"
  local timestamp="$2"
  
  # Check if full backup exists
  if [[ ! -f "$backup_dir/.last_full_backup" ]]; then
    log "WARN" "No full backup found. Creating full backup instead."
    perform_full_backup "$backup_dir" "$timestamp"
    return $?
  fi
  
  log "INFO" "Starting incremental backup..."
  whimsical_message
  
  local archive_name="incremental_backup_$timestamp.tar.gz"
  local archive_path="$backup_dir/$archive_name"
  local last_full_timestamp="$(cat "$backup_dir/.last_full_backup")"
  
  if [[ "$DRY_RUN" == true ]]; then
    log "INFO" "[DRY RUN] Would create incremental backup: $archive_path"
    return 0
  fi
  
  # Create incremental tar archive (only files newer than last full backup)
  log "INFO" "Creating incremental archive..."
  if tar -czf "$archive_path" --newer-mtime="$last_full_timestamp" -C / $(echo "$SOURCE_DIRS" | tr ',' ' '); then
    log "SUCCESS" "Incremental backup created successfully: $archive_path"
    
    # Encrypt if enabled
    if [[ "${ENCRYPT_BACKUP:-false}" == "true" ]]; then
      encrypt_backup "$archive_path"
    fi
  else
    log "ERROR" "Failed to create incremental backup"
    return 1
  fi
}

# Perform differential backup
perform_differential_backup() {
  local backup_dir="$1"
  local timestamp="$2"
  
  # Check if full backup exists
  if [[ ! -f "$backup_dir/.last_full_backup" ]]; then
    log "WARN" "No full backup found. Creating full backup instead."
    perform_full_backup "$backup_dir" "$timestamp"
    return $?
  fi
  
  log "INFO" "Starting differential backup..."
  whimsical_message
  
  local archive_name="differential_backup_$timestamp.tar.gz"
  local archive_path="$backup_dir/$archive_name"
  local last_full_timestamp="$(cat "$backup_dir/.last_full_backup")"
  
  if [[ "$DRY_RUN" == true ]]; then
    log "INFO" "[DRY RUN] Would create differential backup: $archive_path"
    return 0
  fi
  
  # Create differential tar archive (only files newer than last full backup)
  log "INFO" "Creating differential archive..."
  if tar -czf "$archive_path" --newer-mtime="$last_full_timestamp" -C / $(echo "$SOURCE_DIRS" | tr ',' ' '); then
    log "SUCCESS" "Differential backup created successfully: $archive_path"
    
    # Encrypt if enabled
    if [[ "${ENCRYPT_BACKUP:-false}" == "true" ]]; then
      encrypt_backup "$archive_path"
    fi
  else
    log "ERROR" "Failed to create differential backup"
    return 1
  fi
}

# Encrypt backup file
encrypt_backup() {
  local file_path="$1"
  
  if [[ -z "${GPG_RECIPIENT:-}" ]]; then
    log "ERROR" "GPG_RECIPIENT not configured"
    return 1
  fi
  
  log "INFO" "Encrypting backup file..."
  
  if [[ "$DRY_RUN" == true ]]; then
    log "INFO" "[DRY RUN] Would encrypt: $file_path"
    return 0
  fi
  
  if gpg --encrypt --recipient "$GPG_RECIPIENT" --output "$file_path.gpg" "$file_path"; then
    rm "$file_path"
    log "SUCCESS" "Backup encrypted successfully"
  else
    log "ERROR" "Failed to encrypt backup"
    return 1
  fi
}

# Cleanup old backups
cleanup_old_backups() {
  local backup_dir="$1"
  
  log "INFO" "Cleaning up old backups (retention: ${RETENTION_DAYS} days)..."
  
  if [[ "$DRY_RUN" == true ]]; then
    log "INFO" "[DRY RUN] Would cleanup old backups in: $backup_dir"
    return 0
  fi
  
  # Find and remove old backup files
  find "$backup_dir" -name "*.tar.gz" -mtime +"$RETENTION_DAYS" -delete
  find "$backup_dir" -name "*.tar.gz.gpg" -mtime +"$RETENTION_DAYS" -delete
  
  log "INFO" "Old backups cleaned up"
}

# Send email notification
send_email_notification() {
  local subject="$1"
  local message="$2"
  
  if [[ "${ENABLE_EMAIL:-false}" != "true" ]] || [[ -z "${EMAIL_RECIPIENT:-}" ]]; then
    return 0
  fi
  
  if [[ "$DRY_RUN" == true ]]; then
    log "INFO" "[DRY RUN] Would send email to: $EMAIL_RECIPIENT"
    return 0
  fi
  
  if command -v mail &> /dev/null; then
    echo "$message" | mail -s "$subject" "$EMAIL_RECIPIENT"
  elif command -v sendmail &> /dev/null; then
    {
      echo "To: $EMAIL_RECIPIENT"
      echo "Subject: $subject"
      echo
      echo "$message"
    } | sendmail "$EMAIL_RECIPIENT"
  else
    log "WARN" "Mail command not available, skipping email notification"
  fi
}

# Show help
show_help() {
  cat << EOF
Nightly Bash Backup Orchestrator

Usage: $0 [OPTIONS]

OPTIONS:
  --strategy STRATEGY    Backup strategy: full|incremental|differential (default: full)
  --config FILE         Configuration file path (default: $DEFAULT_CONFIG)
  --dry-run            Perform a dry run without making changes
  --verbose            Enable verbose output
  --help               Show this help message

EXAMPLES:
  $0 --strategy full
  $0 --strategy incremental --config /path/to/config.conf
  $0 --dry-run --verbose

EOF
}

# Parse command line arguments
parse_args() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      --strategy)
        STRATEGY="$2"
        shift 2
        ;;
      --config)
        DEFAULT_CONFIG="$2"
        shift 2
        ;;
      --dry-run)
        DRY_RUN=true
        shift
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
        log "ERROR" "Unknown option: $1"
        show_help
        exit 1
        ;;
    esac
  done
}

# Main execution
main() {
  local start_time=$(date +%s)
  local backup_dir="$DESTINATION_DIR/$(date '+%Y%m%d_%H%M%S')"
  local timestamp="$(date '+%Y%m%d_%H%M%S')"
  local success=true
  local error_message=""
  
  log "INFO" "=== Nightly Bash Backup Orchestrator Started ==="
  log "INFO" "Strategy: $STRATEGY"
  log "INFO" "Dry run: $DRY_RUN"
  log "INFO" "Timestamp: $timestamp"
  
  # Load and validate configuration
  load_config "$DEFAULT_CONFIG"
  validate_config
  
  # Create backup directory
  create_backup_dir "$backup_dir"
  
  # Perform backup based on strategy
  case "$STRATEGY" in
    full)
      perform_full_backup "$backup_dir" "$timestamp" || success=false
      ;;
    incremental)
      perform_incremental_backup "$backup_dir" "$timestamp" || success=false
      ;;
    differential)
      perform_differential_backup "$backup_dir" "$timestamp" || success=false
      ;;
    *)
      log "ERROR" "Invalid backup strategy: $STRATEGY"
      success=false
      ;;
  esac
  
  # Cleanup old backups
  if [[ "$success" == true ]]; then
    cleanup_old_backups "$DESTINATION_DIR"
  fi
  
  local end_time=$(date +%s)
  local duration=$((end_time - start_time))
  
  if [[ "$success" == true ]]; then
    log "SUCCESS" "Backup completed successfully in ${duration}s"
    whimsical_message
    send_email_notification "Backup Success" "Your backup completed successfully in ${duration} seconds.\nStrategy: $STRATEGY\nTimestamp: $timestamp"
  else
    log "ERROR" "Backup failed"
    send_email_notification "Backup Failed" "Your backup failed. Please check the logs for details.\nStrategy: $STRATEGY\nTimestamp: $timestamp"
    exit 1
  fi
  
  log "INFO" "=== Nightly Bash Backup Orchestrator Finished ==="
}

# Script entry point
parse_args "$@"
main
