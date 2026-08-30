#!/bin/bash

# Default values
WAYPOINTS_FILE=""
LOOKBACK_DAYS=1 # Last 24 hours
TARGET_DIR=""

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS] <directory>"
    echo "A whimsical Chrono-Compass to guide you through temporal currents."
    echo ""
    echo "Options:"
    echo "  --waypoints <file>  Specify a file containing temporal waypoints (deadlines)."
    echo "                      Format: 'Task Name|YYYY-MM-DD' per line."
    echo "  --lookback <days>   Number of days to look back for recently modified files (default: 1)."
    echo "  -h, --help          Display this help message."
    echo ""
    echo "Example:"
    echo "  $0 --waypoints my_deadlines.txt --lookback 3 /path/to/project"
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --waypoints)
            WAYPOINTS_FILE="$2"
            shift
            ;;
        --lookback)
            LOOKBACK_DAYS="$2"
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then
                TARGET_DIR="$1"
            else
                echo "Error: Unknown option or too many directories: $1" >&2
                usage
                exit 1
            fi
            ;;
    esac
    shift
done

# Validate TARGET_DIR
if [[ -z "$TARGET_DIR" ]]; then
    echo "Error: No target directory specified." >&2
    usage
    exit 1
elif [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist." >&2
    exit 1
fi

echo "🧭 Chrono-Compass Report 🧭"
echo ""
echo "Scanning temporal currents in $TARGET_DIR..."
echo ""

# --- Recent Temporal Disturbances ---
echo "Recent Temporal Disturbances (Modified in last $LOOKBACK_DAYS day(s)):";
RECENT_FILES=$(find "$TARGET_DIR" -maxdepth 2 -type f -mtime -"$LOOKBACK_DAYS" -print0 2>/dev/null | xargs -0 stat -c "%y %n" 2>/dev/null | sort -r)

if [[ -z "$RECENT_FILES" ]]; then
    echo "  No recent disturbances detected."
else
    echo "$RECENT_FILES" | while IFS= read -r line; do
        MOD_DATE=$(echo "$line" | awk '{print $1 " " $2}')
        FILE_PATH=$(echo "$line" | awk '{$1=$2=""; print $0}' | sed 's/^ *//')
        echo "  - $FILE_PATH (Modified: $MOD_DATE)"
    done
fi
echo ""

# --- Upcoming Temporal Waypoints ---
echo "Upcoming Temporal Waypoints:"
if [[ -z "$WAYPOINTS_FILE" ]]; then
    echo "  No waypoint file specified. Use --waypoints to set your course."
elif [[ ! -f "$WAYPOINTS_FILE" ]]; then
    echo "  Waypoint file '$WAYPOINTS_FILE' not found. The temporal map is blank."
else
    CURRENT_DATE_SECONDS=$(date +%s)
    WAYPOINTS_FOUND=false
    while IFS='|' read -r task_name deadline_date; do
        # Skip empty lines or lines without a pipe
        if [[ -z "$task_name" && -z "$deadline_date" ]]; then
            continue
        fi

        # Validate date format (YYYY-MM-DD)
        if ! [[ "$deadline_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            echo "  Warning: Invalid date format for task '$task_name'. Expected YYYY-MM-DD." >&2
            continue
        fi

        DEADLINE_DATE_SECONDS=$(date -d "$deadline_date" +%s 2>/dev/null)
        if [[ $? -ne 0 ]]; then
            echo "  Warning: Could not parse deadline date '$deadline_date' for task '$task_name'." >&2
            continue
        fi

        # Calculate days left
        DAYS_LEFT=$(( (DEADLINE_DATE_SECONDS - CURRENT_DATE_SECONDS) / 86400 )) # 86400 seconds in a day

        if [[ "$DAYS_LEFT" -ge 0 ]]; then
            WAYPOINTS_FOUND=true
            if [[ "$DAYS_LEFT" -eq 0 ]]; then
                echo "  - [TODAY!] $task_name (Deadline: $deadline_date)"
            elif [[ "$DAYS_LEFT" -eq 1 ]]; then
                echo "  - [URGENT - 1 day left] $task_name (Deadline: $deadline_date)"
            elif [[ "$DAYS_LEFT" -lt 7 ]]; then
                echo "  - [$DAYS_LEFT days left] $task_name (Deadline: $deadline_date)"
            else
                echo "  - $task_name (Deadline: $deadline_date)"
            fi
        fi
    done < "$WAYPOINTS_FILE"

    if ! $WAYPOINTS_FOUND; then
        echo "  No upcoming waypoints on the temporal map."
    fi
fi
echo ""
echo "All clear on the temporal horizon for now. Keep an eye on the currents!"
