#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 <stash_name> [OPTIONS]"
    echo "Create a temporary 'ephemeral stash' directory with optional self-destruction or check-in reminders."
    echo ""
    echo "Arguments:"
    echo "  <stash_name>    The name of the ephemeral stash directory to create."
    echo ""
    echo "Options:"
    echo "  -d <duration>   Set a self-destruction timer. Format: 'Xs', 'Xm', 'Xh', 'Xd' (seconds, minutes, hours, days)."
    echo "                  Example: -d 30m for 30 minutes."
    echo "  -r <duration>   Set a check-in reminder. Format: 'Xs', 'Xm', 'Xh', 'Xd'."
    echo "                  Example: -r 1h for a reminder in 1 hour."
    echo "  -h              Display this help message."
    exit 1
}

# Mockable commands (for testing)
# These functions are overridden in tests to capture actions without performing them.
_mkdir() { mkdir "$@"; }
_rm() { rm "$@"; }
_sleep() { sleep "$@"; }
_notify_send() {
    if command -v notify-send &> /dev/null; then
        notify-send "$@"
    else
        # Fallback to logging if notify-send is not available
        echo "$(date +'%Y-%m-%d %H:%M:%S') - Reminder: $2" >> "$HOME/.ephemeral_stash_sentinel_reminders.log"
    fi
}

# Helper function to parse duration string (e.g., "30m" to seconds)
parse_duration() {
    local duration_str="$1"
    local num="${duration_str%[smhd]}"
    local unit="${duration_str##*[0-9]}"
    local seconds=0

    if ! [[ "$num" =~ ^[0-9]+$ ]]; then
        echo 0
        return
    fi

    case "$unit" in
        s) seconds=$num ;;
        m) seconds=$((num * 60)) ;;
        h) seconds=$((num * 3600)) ;;
        d) seconds=$((num * 86400)) ;;
        *) echo 0; return ;;
    esac
    echo "$seconds"
}

# Main logic
main() {
    local stash_name=""
    local delete_duration=""
    local reminder_duration=""

    # Parse arguments
    while getopts ":d:r:h" opt; do
        case ${opt} in
            d ) delete_duration=$OPTARG ;;
            r ) reminder_duration=$OPTARG ;;
            h ) usage ;;
            \? ) echo "Error: Invalid option: -$OPTARG" >&2; usage ;;
            : ) echo "Error: Option -$OPTARG requires an argument." >&2; usage ;;
        esac
    done
    shift $((OPTIND -1))

    stash_name="$1"

    if [ -z "$stash_name" ]; then
        echo "Error: Stash name is required." >&2
        usage
    }

    if [ -d "$stash_name" ]; then
        echo "Error: Directory '$stash_name' already exists. Please choose a different name." >&2
        exit 1
    fi

    echo "Creating ephemeral stash: $stash_name"
    _mkdir "$stash_name" || { echo "Error: Failed to create directory '$stash_name'."; exit 1; }

    local current_dir=$(pwd)

    if [ -n "$delete_duration" ]; then
        local delete_seconds=$(parse_duration "$delete_duration")
        if [ "$delete_seconds" -eq 0 ]; then
            echo "Error: Invalid delete duration format: $delete_duration" >&2
            exit 1
        fi
        echo "Stash '$stash_name' scheduled for self-destruction in $delete_duration."
        (
            _sleep "$delete_seconds"
            if [ -d "$current_dir/$stash_name" ]; then
                echo "Self-destructing '$stash_name' at $(date +'%Y-%m-%d %H:%M:%S')..."
                _rm -rf "$current_dir/$stash_name"
                _notify_send "Ephemeral Stash Sentinel" "Stash '$stash_name' has self-destructed!"
            else
                echo "Stash '$stash_name' already gone, skipping self-destruction at $(date +'%Y-%m-%d %H:%M:%S')."
            fi
        ) & disown # Run in background, detach from shell
    fi

    if [ -n "$reminder_duration" ]; then
        local reminder_seconds=$(parse_duration "$reminder_duration")
        if [ "$reminder_seconds" -eq 0 ]; then
            echo "Error: Invalid reminder duration format: $reminder_duration" >&2
            exit 1
        fi
        echo "Check-in reminder for '$stash_name' scheduled in $reminder_duration."
        (
            _sleep "$reminder_seconds"
            if [ -d "$current_dir/$stash_name" ]; then
                _notify_send "Ephemeral Stash Sentinel" "Time to check your ephemeral stash: '$stash_name' in $current_dir"
            else
                _notify_send "Ephemeral Stash Sentinel" "Reminder: Stash '$stash_name' was scheduled, but it's already gone."
            fi
        ) & disown # Run in background, detach from shell
    fi

    echo "Ephemeral stash '$stash_name' created at $(pwd)/$stash_name"
    echo "Use 'cd $stash_name' to enter."
}

# Call main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    main "$@"
fi
