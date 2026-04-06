#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# A whimsical Bash script to find and optionally clean up old, forgotten files and empty directories.

set -euo pipefail

# --- Configuration --- #
DEFAULT_TARGET_DIR="."
DEFAULT_AGE_DAYS=30

# --- Global Variables --- #
TARGET_DIR="$DEFAULT_TARGET_DIR"
AGE_DAYS="$DEFAULT_AGE_DAYS"
DRY_RUN=true
AUTO_CONFIRM=false
FIND_FILES=true
FIND_EMPTY_DIRS=true

OLD_FILES=()
EMPTY_DIRS=()

# --- Helper Functions --- #

print_help() {
  echo "Usage: $(basename "$0") [OPTIONS]"
  echo "A whimsical script to find and optionally clean up old files and empty directories."
  echo ""
  echo "Options:"
  echo "  -d, --dir <path>     The target directory to scan. Defaults to '$DEFAULT_TARGET_DIR'."
  echo "  -a, --age <days>     Files older than this many days will be considered 'dust bunnies'. Defaults to $DEFAULT_AGE_DAYS days."
  echo "  -e, --empty-only     Only find and report empty directories (no old files)."
  echo "  -f, --files-only     Only find and report old files (no empty directories)."
  echo "  -s, --sweep          Perform the actual cleanup (delete files/directories). Use with caution!"
  echo "  -y, --yes            Automatically confirm all deletions when using --sweep (non-interactive)."
  echo "  -h, --help           Display this help message."
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") --dir /var/log --age 7"
  echo "  $(basename "$0") --dir ~/ --empty-only --sweep --yes"
  exit 0
}

log_info() {
  echo "[34m[INFO][0m $1"
}

log_warn() {
  echo "[33m[WARN][0m $1"
}

log_error() {
  echo "[31m[ERROR][0m $1" >&2
  exit 1
}

# --- Core Logic --- #

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -d|--dir)
        TARGET_DIR="$2"
        shift # past argument
        shift # past value
        ;;
      -a|--age)
        if ! [[ "$2" =~ ^[0-9]+$ ]] || (( "$2" < 0 )); then
          log_error "Invalid age: '$2'. Must be a non-negative integer."
        fi
        AGE_DAYS="$2"
        shift # past argument
        shift # past value
        ;;
      -e|--empty-only)
        FIND_FILES=false
        FIND_EMPTY_DIRS=true
        shift # past argument
        ;;
      -f|--files-only)
        FIND_FILES=true
        FIND_EMPTY_DIRS=false
        shift # past argument
        ;;
      -s|--sweep)
        DRY_RUN=false
        shift # past argument
        ;;
      -y|--yes)
        AUTO_CONFIRM=true
        shift # past argument
        ;;
      -h|--help)
        print_help
        ;;
      -*)
        log_error "Unknown option: '$1'. Use -h for help."
        ;;
      *)
        log_error "Unexpected argument: '$1'. Use -h for help."
        ;;
    esac
  done

  if [[ ! -d "$TARGET_DIR" ]]; then
    log_error "Target directory '$TARGET_DIR' does not exist or is not a directory."
  fi

  if ! $FIND_FILES && ! $FIND_EMPTY_DIRS; then
    log_error "Cannot use --empty-only and --files-only together. Please choose one or neither."
  fi
}

find_dust_bunnies() {
  if ! $FIND_FILES; then return; fi

  log_info "Searching for digital dust bunnies (files older than $AGE_DAYS days) in '$TARGET_DIR'...
"
  # find -mtime +N means files modified more than N*24 hours ago.
  # So, for files older than AGE_DAYS, we use AGE_DAYS-1.
  # If AGE_DAYS is 1, it means files older than 24 hours (mtime +0).
  local find_age=$((AGE_DAYS - 1))
  if (( find_age < 0 )); then find_age=0; fi # Handle AGE_DAYS=0 or 1 gracefully

  # Mock rationale: In tests, 'find' is not mocked directly. Instead, test files are created
  # with specific modification times, and 'date' is mocked to control the perceived current time,
  # making 'find -mtime' deterministic.
  mapfile -t OLD_FILES < <(find "$TARGET_DIR" -type f -mtime +"$find_age" -print 2>/dev/null || true)
}

find_empty_cobwebs() {
  if ! $FIND_EMPTY_DIRS; then return; fi

  log_info "Searching for cyber cobwebs (empty directories) in '$TARGET_DIR'...
"
  # Mock rationale: Similar to find_dust_bunnies, 'find' is not mocked directly.
  # Test directories are created to be empty or non-empty.
  mapfile -t EMPTY_DIRS < <(find "$TARGET_DIR" -type d -empty -print 2>/dev/null || true)

  # Filter out the TARGET_DIR itself if it's empty and found
  EMPTY_DIRS=( "${EMPTY_DIRS[@]/$TARGET_DIR}" )
}

report_findings() {
  echo "
--- Digital Dust Bunny Sweeper Report ---"
  echo "Target Directory: '$TARGET_DIR'"
  echo "Age Threshold: $AGE_DAYS days"
  echo "Mode: $(if $DRY_RUN; then echo "Dry Run (no changes)"; else echo "Live Sweep (deleting!)"; fi)"
  echo "----------------------------------------"

  if (( ${#OLD_FILES[@]} > 0 )); then
    echo "
[33mFound ${#OLD_FILES[@]} digital dust bunnies (old files):[0m"
    for file in "${OLD_FILES[@]}"; do
      echo "  - $file"
    done
  else
    echo "
[32mNo digital dust bunnies found. Your files are spick and span![0m"
  fi

  if (( ${#EMPTY_DIRS[@]} > 0 )); then
    echo "
[33mFound ${#EMPTY_DIRS[@]} cyber cobwebs (empty directories):[0m"
    for dir in "${EMPTY_DIRS[@]}"; do
      echo "  - $dir"
    done
  else
    echo "
[32mNo cyber cobwebs found. Your directories are bustling with purpose![0m"
  fi

  if (( ${#OLD_FILES[@]} == 0 )) && (( ${#EMPTY_DIRS[@]} == 0 )); then
    echo "
[32mYour digital realm is pristine! No cleanup needed.[0m"
  elif $DRY_RUN; then
    echo "
[34mThis was a dry run. To perform the actual sweep, run with the '--sweep' option.[0m"
  else
    echo "
[32mSweep complete! Your digital space feels lighter.[0m"
  fi
  echo "----------------------------------------"
}

perform_sweep() {
  if $DRY_RUN; then
    log_info "Dry run mode. No files or directories will be deleted."
    return
  fi

  if (( ${#OLD_FILES[@]} == 0 )) && (( ${#EMPTY_DIRS[@]} == 0 )); then
    log_info "Nothing to sweep. Your digital space is already clean."
    return
  fi

  log_warn "
Initiating digital sweep! This will permanently delete files and directories."
  if ! $AUTO_CONFIRM; then
    read -r -p "Are you sure you want to proceed? (y/N) " response
    # Mock rationale: In tests, 'read' is mocked to provide a predetermined response (e.g., 'y' or 'n').
    if ! [[ "$response" =~ ^[yY]$ ]]; then
      log_info "Sweep aborted by user."
      exit 0
    fi
  fi

  log_info "Sweeping digital dust bunnies..."
  for file in "${OLD_FILES[@]}"; do
    if [[ -f "$file" ]]; then
      log_info "Deleting file: '$file'"
      # Mock rationale: In tests, 'rm' is mocked to prevent actual deletion and instead log its calls.
      rm -f "$file" || log_warn "Failed to delete file: '$file'"
    fi
  done

  log_info "Vacuuming cyber cobwebs..."
  # Delete empty directories, starting from deepest to avoid issues with parent directories becoming empty
  # and then being deleted before their children are processed.
  for dir in "$(printf "%s\n" "${EMPTY_DIRS[@]}" | sort -r)"; do
    if [[ -d "$dir" ]]; then
      log_info "Deleting empty directory: '$dir'"
      # Mock rationale: In tests, 'rmdir' (via 'rm -d') is mocked to prevent actual deletion and instead log its calls.
      rmdir "$dir" || log_warn "Failed to delete empty directory: '$dir'"
    fi
  done
}

# --- Main Execution --- #
main() {
  parse_args "$@"

  find_dust_bunnies
  find_empty_cobwebs

  report_findings
  perform_sweep
}

main "$@"
