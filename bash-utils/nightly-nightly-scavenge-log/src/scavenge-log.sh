#!/bin/bash

# Nightly Scavenge Log - A utility for tracking wasteland finds.

# Configuration
LOG_DIR="${HOME}/.apocalypsai_scavenge_logs"
CURRENT_DATE="${_TEST_DATE:-$(date +%Y-%m-%d)}" # Mock rationale: Allows deterministic testing by overriding the date.
LOG_FILE="${LOG_DIR}/${CURRENT_DATE}.log"

# --- Helper Functions ---

# Ensures the log directory exists
_ensure_log_dir() {
    mkdir -p "$LOG_DIR" || { echo "Error: Could not create log directory $LOG_DIR" >&2; exit 1; }
}

# Logs an item
# Args: item_name, category, quantity
add_item() {
    local item_name="$1"
    local category="$2"
    local quantity="$3"

    if [[ -z "$item_name" || -z "$category" || -z "$quantity" ]]; then
        echo "Usage: scavenge-log.sh add \"<item_name>\" \"<category>\" <quantity>" >&2
        return 1
    fi

    if ! [[ "$quantity" =~ ^[1-9][0-9]*$ ]]; then
        echo "Error: Quantity must be a positive integer." >&2
        return 1
    fi

    _ensure_log_dir

    local timestamp=$(date +%H:%M:%S) # Mock rationale: Timestamp is real-time, but date is mocked.
    echo "${timestamp} | ${item_name} | ${category} | ${quantity}" >> "$LOG_FILE"
    echo "Logged: ${item_name} (${quantity}) in category '${category}' for ${CURRENT_DATE}."
    return 0
}

# Views today's log
view_log() {
    echo "--- Scavenge Log for ${CURRENT_DATE} ---"
    if [[ -f "$LOG_FILE" ]]; then
        cat "$LOG_FILE"
    else
        echo "No scavenged items logged for today."
    fi
    echo "-------------------------------------"
    return 0
}

# Generates a manifest for a specific date
# Args: target_date (YYYY-MM-DD)
generate_manifest() {
    local target_date="$1"
    local target_log_file="${LOG_DIR}/${target_date}.log"

    if [[ -z "$target_date" ]]; then
        echo "Usage: scavenge-log.sh manifest <YYYY-MM-DD>" >&2
        return 1
    fi

    if ! [[ "$target_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo "Error: Invalid date format. Please use YYYY-MM-DD." >&2
        return 1
    fi

    echo "--- Scavenge Manifest for ${target_date} ---"
    if [[ -f "$target_log_file" ]]; then
        cat "$target_log_file"
    else
        echo "No scavenged items logged for ${target_date}."
    fi
    echo "------------------------------------------"
    return 0
}

# --- Main Logic ---

case "$1" in
    add)
        shift # Remove 'add' from arguments
        add_item "$@"
        ;;
    view)
        view_log
        ;;
    manifest)
        shift # Remove 'manifest' from arguments
        generate_manifest "$@"
        ;;
    *)
        echo "Usage: scavenge-log.sh {add|view|manifest}" >&2
        echo "  add \"<item_name>\" \"<category>\" <quantity>" >&2
        echo "  view" >&2
        echo "  manifest <YYYY-MM-DD>" >&2
        exit 1
        ;;
esac

exit $?
