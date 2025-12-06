#!/bin/bash

# Nightly Bash Backup Buddy
# A whimsical utility for creating timestamped backups

set -euo pipefail

# Configuration defaults
COMPRESS=false
RETENTION=5
DRY_RUN=false
SCRIPT_NAME="$(basename "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ASCII art for the backup buddy
print_buddy() {
  cat << 'EOF'
  🎒  _
     (\(\
    ( ._.)
    o_('')(')
  EOF
}

# Print colored output
print_info() {
  echo -e "${BLUE}[INFO]${NC} $*"
}

print_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $*"
}

print_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $*"
}

print_error() {
  echo -e "${RED}[ERROR]${NC} $*"
}

# Print help
print_help() {
  cat << EOF
${SCRIPT_NAME} - A whimsical backup utility

USAGE:
    ${SCRIPT_NAME} [OPTIONS] <source_dir> <backup_dir>

DESCRIPTION:
    Creates timestamped backups of directories with optional compression
    and automatic cleanup of old backups.

OPTIONS:
    --compress          Create compressed tar.gz backups
    --retention N       Keep only the last N backups (default: 5)
    --dry-run           Show what would be done without actually doing it
    --help              Display this help message

EXAMPLES:
    # Basic backup
    ${SCRIPT_NAME} /path/to/source /path/to/backup

    # Compressed backup with 7-day retention
    ${SCRIPT_NAME} --compress --retention 7 /path/to/source /path/to/backup

    # Dry run
    ${SCRIPT_NAME} --dry-run /path/to/source /path/to/backup

EOF
}

# Parse command line arguments
parse_args() {
  local args=()
  
  while [[ $# -gt 0 ]]; do
    case $1 in
      --compress)
        COMPRESS=true
        shift
        ;;
      --retention)
        if [[ -n "${2:-}" ]] && [[ $2 != --* ]]; then
          RETENTION="$2"
          shift 2
        else
          print_error "--retention requires a number"
          exit 1
        fi
        ;;
      --dry-run)
        DRY_RUN=true
        shift
        ;;
      --help)
        print_help
        exit 0
        ;;
      *)
        args+=("$1")
        shift
        ;;
    esac
  done
  
  if [[ ${#args[@]} -ne 2 ]]; then
    print_error "Usage: ${SCRIPT_NAME} [OPTIONS] <source_dir> <backup_dir>"
    exit 1
  fi
  
  SOURCE_DIR="${args[0]}"
  BACKUP_DIR="${args[1]}"
}

# Validate inputs
validate_inputs() {
  # Check if source directory exists
  if [[ ! -d "$SOURCE_DIR" ]]; then
    print_error "Source directory does not exist: $SOURCE_DIR"
    exit 1
  fi
  
  # Check if source is readable
  if [[ ! -r "$SOURCE_DIR" ]]; then
    print_error "Source directory is not readable: $SOURCE_DIR"
    exit 1
  fi
  
  # Create backup directory if it doesn't exist
  if [[ ! -d "$BACKUP_DIR" ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then
      print_info "Would create backup directory: $BACKUP_DIR"
    else
      print_info "Creating backup directory: $BACKUP_DIR"
      mkdir -p "$BACKUP_DIR"
    fi
  fi
  
  # Check if backup directory is writable
  if [[ ! -w "$BACKUP_DIR" ]]; then
    print_error "Backup directory is not writable: $BACKUP_DIR"
    exit 1
  fi
  
  # Validate retention number
  if ! [[ "$RETENTION" =~ ^[0-9]+$ ]] || [[ "$RETENTION" -lt 1 ]]; then
    print_error "Retention must be a positive integer"
    exit 1
  fi
  
  # Check compression tools if compression is enabled
  if [[ "$COMPRESS" == "true" ]]; then
    if ! command -v tar &> /dev/null; then
      print_error "tar command not found. Please install tar for compression."
      exit 1
    fi
  fi
}

# Generate timestamp for backup name
get_timestamp() {
  date '+%Y%m%d_%H%M%S'
}

# Create backup
create_backup() {
  local timestamp
  timestamp=$(get_timestamp)
  local backup_name="backup_${timestamp}"
  local backup_path="$BACKUP_DIR/$backup_name"
  
  print_info "Starting backup..."
  print_buddy
  
  if [[ "$COMPRESS" == "true" ]]; then
    backup_name="${backup_name}.tar.gz"
    backup_path="$BACKUP_DIR/$backup_name"
    
    if [[ "$DRY_RUN" == "true" ]]; then
      print_info "Would create compressed backup: $backup_path"
      print_info "Would backup source: $SOURCE_DIR"
    else
      print_info "Creating compressed backup: $backup_path"
      if tar -czf "$backup_path" -C "$(dirname \"$SOURCE_DIR\")" "$(basename \"$SOURCE_DIR\")"; then
        print_success "Compressed backup created successfully!"
      else
        print_error "Failed to create compressed backup"
        exit 1
      fi
    fi
  else
    if [[ "$DRY_RUN" == "true" ]]; then
      print_info "Would create directory backup: $backup_path"
      print_info "Would backup source: $SOURCE_DIR"
    else
      print_info "Creating directory backup: $backup_path"
      if cp -r "$SOURCE_DIR" "$backup_path"; then
        print_success "Directory backup created successfully!"
      else
        print_error "Failed to create directory backup"
        exit 1
      fi
    fi
  fi
  
  return 0
}

# Cleanup old backups
cleanup_old_backups() {
  print_info "Cleaning up old backups (keeping last $RETENTION)..."
  
  local backup_files=()
  
  if [[ "$COMPRESS" == "true" ]]; then
    # Find compressed backups
    while IFS= read -r -d '' file; do
      backup_files+=("$file")
    done < <(find "$BACKUP_DIR" -name "backup_*.tar.gz" -type f -print0 2>/dev/null | sort -rz)
  else
    # Find directory backups
    while IFS= read -r -d '' dir; do
      backup_files+=("$dir")
    done < <(find "$BACKUP_DIR" -name "backup_*" -type d -print0 2>/dev/null | sort -rz)
  fi
  
  local total_backups=${#backup_files[@]}
  
  if [[ $total_backups -le $RETENTION ]]; then
    print_info "No old backups to clean up (have $total_backups, keeping $RETENTION)"
    return 0
  fi
  
  local to_remove=$((total_backups - RETENTION))
  print_info "Found $total_backups backups, removing $to_remove old ones"
  
  # Remove old backups
  for ((i=RETENTION; i<total_backups; i++)); do
    local backup_to_remove="${backup_files[i]}"
    if [[ "$DRY_RUN" == "true" ]]; then
      print_info "Would remove: $backup_to_remove"
    else
      print_info "Removing old backup: $(basename \"$backup_to_remove\")"
      if rm -rf "$backup_to_remove"; then
        print_success "Removed: $(basename \"$backup_to_remove\")"
      else
        print_warning "Failed to remove: $backup_to_remove"
      fi
    fi
  done
}

# Main execution
main() {
  print_info "Welcome to Nightly Bash Backup Buddy! 🎒"
  
  parse_args "$@"
  validate_inputs
  create_backup
  cleanup_old_backups
  
  print_success "Backup operation completed successfully!"
  print_buddy
}

# Run main with all arguments
main "$@"
