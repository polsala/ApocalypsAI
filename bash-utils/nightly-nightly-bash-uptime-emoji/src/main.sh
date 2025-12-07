#!/usr/bin/env bash
# nightly-bash-uptime-emoji
# Prints system uptime together with a whimsical emoji.

# -------------------------------------------------------------------
# Helper: Convert a "uptime -p" string (e.g. "up 2 hours, 15 minutes")
# into total minutes.
# -------------------------------------------------------------------
parse_uptime_minutes() {
    local uptime_str="$1"
    # Strip leading "up " if present
    uptime_str="${uptime_str#up }"
    # Replace commas with spaces for easier tokenisation
    uptime_str="${uptime_str//,/ }"
    local total_minutes=0
    for token in $uptime_str; do
        case "$token" in
            *day*)
                # Remove the trailing "day" or "days"
                local days="${token%%day*}"
                (( total_minutes+=days*1440 ))
                ;;
            *hour*)
                local hours="${token%%hour*}"
                (( total_minutes+=hours*60 ))
                ;;
            *minute*)
                local minutes="${token%%minute*}"
                (( total_minutes+=minutes ))
                ;;
        esac
    done
    echo "$total_minutes"
}

# -------------------------------------------------------------------
# Determine which emoji to show based on total minutes.
# -------------------------------------------------------------------
select_emoji() {
    local minutes="$1"
    if (( minutes < 360 )); then   # < 6 hours
        echo "🌅"
    elif (( minutes < 720 )); then # < 12 hours
        echo "☀️"
    elif (( minutes < 1080 )); then # < 18 hours
        echo "🌇"
    else
        echo "🌙"
    fi
}

# -------------------------------------------------------------------
# Main logic
# -------------------------------------------------------------------
main() {
    local uptime_input="$1"
    if [[ -z "$uptime_input" ]]; then
        # No argument supplied – query the real system
        if ! command -v uptime >/dev/null 2>&1; then
            echo "Error: 'uptime' command not found." >&2
            exit 1
        fi
        uptime_input=$(uptime -p)
    fi

    # Parse minutes
    local total_minutes
    total_minutes=$(parse_uptime_minutes "$uptime_input")

    # Derive hours and remaining minutes for pretty printing
    local hours=$(( total_minutes / 60 ))
    local minutes=$(( total_minutes % 60 ))

    # Choose emoji
    local emoji
    emoji=$(select_emoji "$total_minutes")

    echo "System has been up for ${hours} hours ${minutes} minutes. ${emoji}"
}

# Execute
main "$1"
