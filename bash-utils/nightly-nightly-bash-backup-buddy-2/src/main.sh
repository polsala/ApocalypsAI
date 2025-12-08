#!/bin/bash

# Nightly Bash Backup Buddy
# A whimsical utility for creating timestamped backups

set -euo pipefail

# Configuration
SCRIPT_NAME="$(basename "$0")"
DEFAULT_COMPRESS=6
MAX_COMPRESS=9

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Whimsical messages
declare -a SUCCESS_MESSAGES=(
  "Backup completed successfully! The data is safe and sound."
  "Archive created! Your files are now cozy in their compressed home."
  "Backup finished! Even a squirrel would be proud of this hoard."
  "All done! Your data is now immortalized in digital amber."
  "Success! The backup fairies have done their work."
)

declare -a ERROR_MESSAGES=(
  "Uh oh! Something went wrong. The backup goblins are at it again."
  "Error! Your files escaped the archive. Try again!"
  "Oops! The backup wizard lost his spellbook."
  "Failed! Even the cloud is crying about this one."
  "Nope! The backup gremlins struck at midnight."
)

declare -a VALIDATION_MESSAGES=(
  "Archive validated! Your backup is as solid as a rock."
  "Checksum verified! The data integrity police give it a thumbs up."
  "All good! Your backup passed the digital Turing test."
  "Confirmed! Your files survived the compression journey."
  "Validated! The backup is ready for the apocalypse."
)

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

# Get random message from array
get_random_message() {
  local messages=("$@")
  local count=${#messages[@]}
  local random_index=$((RANDOM % count))
  echo "${messages[$random_index]}"
}

# Show help
show_help() {
  cat << EOF
${SCRIPT_NAME} - A whimsical backup utility

USAGE:
    ${SCRIPT_NAME} [OPTIONS] SOURCE_DIR BACKUP_DIR

ARGUMENTS:
    SOURCE_DIR    Directory to backup
    BACKUP_DIR    Directory where backup archives will be stored

OPTIONS:
    -c, --compress LEVEL    Compression level (1-9, default: ${DEFAULT_COMPRESS})
    -d, --dry-run          Show what would be done without actually doing it
    -h, --help             Show this help message

EXAMPLES:
    # Basic backup
    ${SCRIPT_NAME} /home/user/Documents /backups

    # High compression backup
    ${SCRIPT_NAME} --compress 9 /home/user/Documents /backups

    # Dry run to see what would happen
    ${SCRIPT_NAME} --dry-run /home/user/Documents /backups

EOF
}

# Validate compression level
validate_compress_level() {
  local level="$1"
  
  if ! [[ "$level" =~ ^[0-9]+$ ]]; then
    log_error "Compression level must be a number"
    return 1
  fi
  
  if (( level < 1 || level > MAX_COMPRESS )); then
    log_error "Compression level must be between 1 and ${MAX_COMPRESS}"
    return 1
  fi
  
  return 0
}

# Check if directory exists and is readable
validate_source_dir() {
  local dir="$1"
  
  if [[ ! -d "$dir" ]]; then
    log_error "Source directory does not exist: $dir"
    return 1
  fi
  
  if [[ ! -r "$dir" ]]; then
    log_error "Source directory is not readable: $dir"
    return 1
  fi
  
  return 0
}

# Ensure backup directory exists
ensure_backup_dir() {
  local dir="$1"
  local dry_run="$2"
  
  if [[ ! -d "$dir" ]]; then
    if [[ "$dry_run" == "true" ]]; then
      log_info "[DRY RUN] Would create backup directory: $dir"
    else
      log_info "Creating backup directory: $dir"
      mkdir -p "$dir"
    fi
  fi
  
  if [[ ! -w "$dir" ]]; then
    log_error "Backup directory is not writable: $dir"
    return 1
  fi
  
  return 0
}

# Create backup archive
create_backup() {
  local source_dir="$1"
  local backup_dir="$2"
  local compress_level="$3"
  local dry_run="$4"
  
  # Generate timestamp and filename
  local timestamp="$(date '+%Y%m%d_%H%M%S')"
  local source_basename="$(basename "$source_dir")"
  local archive_name="${source_basename}_${timestamp}.tar.gz"
  local archive_path="${backup_dir}/${archive_name}"
  local checksum_path="${archive_path}.sha256"
  
  log_info "Creating backup of '$source_dir'"
  log_info "Archive will be: $archive_name"
  
  if [[ "$dry_run" == "true" ]]; then
    log_info "[DRY RUN] Would create archive: $archive_path"
    log_info "[DRY RUN] Would use compression level: $compress_level"
    log_success "[DRY RUN] $ (get_random_message "${SUCCESS_MESSAGES[@]}")"
    return 0
  fi
  
  # Create the archive
  log_info "Compressing with level $compress_level..."
  if tar -czf "$archive_path" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"; then
    log_success "$(get_random_message "${SUCCESS_MESSAGES[@]}")"
  else
    log_error "$(get_random_message "${ERROR_MESSAGES[@]}")"
    return 1
  fi
  
  # Generate checksum
  log_info "Generating checksum..."
  if sha256sum "$archive_path" | awk '{print $1}' > "$checksum_path"; then
    log_info "Checksum saved to: $(basename "$checksum_path")"
  else
    log_warning "Failed to generate checksum"
  fi
  
  # Validate the archive
  validate_archive "$archive_path"
  
  return 0
}

# Validate backup archive
validate_archive() {
  local archive_path="$1"
  
  log_info "Validating archive..."
  
  if tar -tzf "$archive_path" > /dev/null 2>&1; then
    log_success "$(get_random_message "${VALIDATION_MESSAGES[@]}")"
  else
    log_error "Archive validation failed! The backup may be corrupted."
    return 1
  fi
  
  return 0
}

# Main function
main() {
  local compress_level="$DEFAULT_COMPRESS"
  local dry_run="false"
  local source_dir=""
  local backup_dir=""
  
  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case $1 in
      -c|--compress)
        if [[ -n "${2:-}" ]] && [[ ! $2 =~ ^- ]]; then
          compress_level="$2"
          shift 2
        else
          log_error "--compress requires a value"
          exit 1
        fi
        ;;
      -d|--dry-run)
        dry_run="true"
        shift
        ;;
      -h|--help)
        show_help
        exit 0
        ;;
      *)
        if [[ -z "$source_dir" ]]; then
          source_dir="$1"
        elif [[ -z "$backup_dir" ]]; then
          backup_dir="$1"
        else
          log_error "Unexpected argument: $1"
          exit 1
        fi
        shift
        ;;
    esac
  done
  
  # Validate arguments
  if [[ -z "$source_dir" ]] || [[ -z "$backup_dir" ]]; then
    log_error "Source and backup directories are required"
    echo
    show_help
    exit 1
  fi
  
  if ! validate_compress_level "$compress_level"; then
    exit 1
  fi
  
  if ! validate_source_dir "$source_dir"; then
    exit 1
  fi
  
  if ! ensure_backup_dir "$backup_dir" "$dry_run"; then
    exit 1
  fi
  
  # Create backup
  if create_backup "$source_dir" "$backup_dir" "$compress_level" "$dry_run"; then
    log_info "Backup process completed successfully!"
    exit 0
  else
    log_error "Backup process failed!"
    exit 1
  fi
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
