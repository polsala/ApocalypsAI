#!/bin/bash

CACHE_DIR="/cache/notes"
RETENTION_HOURS=${CHRONO_RETENTION_HOURS:-24} # Default retention: 24 hours

# Ensure cache directory exists
mkdir -p "$CACHE_DIR"

function help_message {
    echo "Chrono-Cache Courier - Ephemeral Note System"
    echo ""
    echo "Usage: chrono-cache-courier <command> [args]"
    echo ""
    echo "Commands:"
    echo "  add <key> <value>   - Store a new ephemeral note."
    echo "  get <key>           - Retrieve an ephemeral note by its key."
    echo "  list                - List all active ephemeral note keys."
    echo "  clean               - Remove notes older than ${RETENTION_HOURS} hours."
    echo "  help                - Display this help message."
    echo ""
    echo "Environment Variables:"
    echo "  CHRONO_RETENTION_HOURS - Override default retention (default: 24 hours)."
}

function add_note {
    local key="$1"
    local value="$2"
    if [[ -z "$key" || -z "$value" ]]; then
        echo "Error: 'add' requires a key and a value." >&2
        help_message
        return 1
    fi
    echo "$value" > "${CACHE_DIR}/${key}"
    echo "Note '${key}' added to Chrono-Cache."
}

function get_note {
    local key="$1"
    if [[ -z "$key" ]]; then
        echo "Error: 'get' requires a key." >&2
        help_message
        return 1
    fi
    if [[ -f "${CACHE_DIR}/${key}" ]]; then
        cat "${CACHE_DIR}/${key}"
    else
        echo "Error: Note '${key}' not found." >&2
        return 1
    fi
}

function list_notes {
    if ls -1q "$CACHE_DIR" | grep -q .; then # Check if directory is not empty
        echo "Active Chrono-Cache Notes:"
        ls -1 "$CACHE_DIR"
    else
        echo "No active Chrono-Cache notes."
    fi
}

function clean_notes {
    local retention_minutes=$((RETENTION_HOURS * 60))
    local cleaned_count=0
    # Find files older than retention_minutes and delete them
    # -mmin +N: file's data was last modified N minutes ago.
    # +N means more than N minutes.
    while IFS= read -r -d $'\0' file; do
        rm "$file"
        echo "Cleaned: $(basename "$file") (older than ${RETENTION_HOURS} hours)"
        cleaned_count=$((cleaned_count + 1))
    done < <(find "$CACHE_DIR" -type f -mmin "+$retention_minutes" -print0)

    if [[ "$cleaned_count" -eq 0 ]]; then
        echo "No notes older than ${RETENTION_HOURS} hours found for cleaning."
    else
        echo "Chrono-Cache cleaned. Removed ${cleaned_count} old notes."
    fi
}

case "$1" in
    add)
        add_note "$2" "$3"
        ;;
    get)
        get_note "$2"
        ;;
    list)
        list_notes
        ;;
    clean)
        clean_notes
        ;;
    help|*)
        help_message
        ;;
esac
