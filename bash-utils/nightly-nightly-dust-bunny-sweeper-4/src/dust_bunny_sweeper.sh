#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# Sweeps away old, forgotten files (digital dust bunnies) from specified directories.

# --- Configuration Defaults ---
CONFIG_FILE="${HOME}/.config/dust_bunny_sweeper.conf"
DEFAULT_SCAN_DIRS=("/tmp" "${HOME}/.cache") # Default directories to scan
DEFAULT_AGE_DAYS=7 # Default age threshold in days
DRY_RUN=true # Default to dry run mode

# --- Whimsical Messages ---
MSG_START="The Digital Dust Bunny Sweeper is revving up its engines! 🧹"
MSG_SCANNING="Scanning for fluffy digital dust bunnies..."
MSG_FOUND="Found some digital dust bunnies! Here's what they look like:"
MSG_NO_BUNNIES="No digital dust bunnies found. Your system is sparkling clean! ✨"
MSG_CONFIRM="Ready to sweep these into the void? (y/N): "
MSG_SWEEPING="Sweeping digital dust bunnies... Poof! They're gone!"
MSG_ABORTED="Sweep aborted. The dust bunnies live to see another day. 🐰"
MSG_DRY_RUN_ONLY="(This was a dry run. No files were actually deleted.)"
MSG_HELP="Usage: $(basename "$0") [OPTIONS]\n\nOptions:\n  -c <config_file>  Specify a custom configuration file path.\n  -d <directory>    Add a directory to scan. Can be used multiple times. Overrides config.\n  -a <days>         Set the age threshold in days. Defaults to ${DEFAULT_AGE_DAYS}.\n  -n                No dry run. Perform the actual sweep (requires confirmation).\n  -h                Display this help message.\n"

# --- Functions ---

# Function to load configuration from file
load_config() {
  if [[ -f "$1" ]]; then
    echo "Loading configuration from $1..."
    # Source the config file to set variables
    # shellcheck disable=SC1090
    source "$1"
  fi
}

# Function to find digital dust bunnies
# Arguments: array of directories, age in days
find_dust_bunnies() {
  local -a dirs=("$@")
  local age_days="${dirs[-1]}"
  unset 'dirs[${#dirs[@]}-1]'

  local found_files=()
  local find_cmd_output

  if [[ ${#dirs[@]} -eq 0 ]]; then
    echo "No directories specified for scanning. Aborting." >&2
    return 1
  fi

  # Use find to locate files older than age_days
  # -type f: only regular files
  # -mtime +N: files whose data was last modified N*24 hours ago. +N means more than N days.
  # -print0: print full file name on standard output, followed by a null character
  # This handles filenames with spaces or special characters correctly.
  find_cmd_output=$(find "${dirs[@]}" -type f -mtime +"$age_days" -print0 2>/dev/null)

  if [[ -n "$find_cmd_output" ]]; then
    # Read null-separated paths into an array
    while IFS= read -r -d '' file; do
      found_files+=("$file")
    done <<< "$find_cmd_output"
  fi

  echo "${found_files[@]}"
  return 0
}

# Function to sweep digital dust bunnies
sweep_dust_bunnies() {
  local -a files_to_sweep=("$@")

  if [[ ${#files_to_sweep[@]} -eq 0 ]]; then
    echo "${MSG_NO_BUNNIES}"
    return 0
  fi

  echo "${MSG_FOUND}"
  for file in "${files_to_sweep[@]}"; do
    echo "  - $file"
  done

  if $DRY_RUN; then
    echo "${MSG_DRY_RUN_ONLY}"
  else
    read -p "${MSG_CONFIRM}" -n 1 -r
    echo # Move to a new line
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      echo "${MSG_SWEEPING}"
      # Use xargs -0 to handle null-separated filenames from find_dust_bunnies
      printf "%s\0" "${files_to_sweep[@]}" | xargs -0 rm -v
    else
      echo "${MSG_ABORTED}"
    fi
  fi
}

# --- Main Logic ---
main() {
  echo "${MSG_START}"

  local scan_dirs=("${DEFAULT_SCAN_DIRS[@]}")
  local age_days="${DEFAULT_AGE_DAYS}"

  # Load config file if it exists
  load_config "$CONFIG_FILE"

  # Override with config file values if set and not overridden by CLI
  if [[ -n "$SCAN_DIRS" && ${#CLI_SCAN_DIRS[@]} -eq 0 ]]; then
    # Convert space-separated string to array
    IFS=' ' read -r -a scan_dirs <<< "$SCAN_DIRS"
  fi
  if [[ -n "$AGE_DAYS" && -z "$CLI_AGE_DAYS" ]]; then
    age_days="$AGE_DAYS"
  fi

  # Override with CLI arguments if provided
  if [[ ${#CLI_SCAN_DIRS[@]} -gt 0 ]]; then
    scan_dirs=("${CLI_SCAN_DIRS[@]}")
  fi
  if [[ -n "$CLI_AGE_DAYS" ]]; then
    age_days="$CLI_AGE_DAYS"
  fi

  echo "${MSG_SCANNING}"
  echo "  Directories: ${scan_dirs[*]}"
  echo "  Age threshold: ${age_days} days"

  local -a bunnies_found
  # Pass directories and age as arguments to find_dust_bunnies
  bunnies_found=($(find_dust_bunnies "${scan_dirs[@]}" "$age_days"))

  sweep_dust_bunnies "${bunnies_found[@]}"
}

# --- Argument Parsing ---
CLI_SCAN_DIRS=()
CLI_AGE_DAYS=""

while getopts "c:d:a:nh" opt; do
  case $opt in
    c) CONFIG_FILE="$OPTARG" ;;
    d) CLI_SCAN_DIRS+=("$OPTARG") ;;
    a) CLI_AGE_DAYS="$OPTARG" ;;
    n) DRY_RUN=false ;;
    h) echo -e "${MSG_HELP}"; exit 0 ;;
    \?) echo "Invalid option: -$OPTARG" >&2; echo -e "${MSG_HELP}"; exit 1 ;;
  esac
done
shift $((OPTIND-1))

main "$@"
