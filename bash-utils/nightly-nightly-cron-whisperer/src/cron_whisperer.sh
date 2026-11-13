#!/bin/bash

# Function to interpret cron job commands
interpret_command() {
    local cmd="$1"
    local whisper="Mysterious Routine"

    if [[ "$cmd" =~ "backup" || "$cmd" =~ "sync" || "$cmd" =~ "archive" ]]; then
        whisper="Guardian of the Archives"
    elif [[ "$cmd" =~ "cleanup" || "$cmd" =~ "rm" || "$cmd" =~ "delete" ]]; then
        whisper="Wasteland Scavenger"
    elif [[ "$cmd" =~ "update" || "$cmd" =~ "upgrade" || "$cmd" =~ "apt" || "$cmd" =~ "yum" ]]; then
        whisper="Temporal Harmonizer"
    elif [[ "$cmd" =~ "reboot" || "$cmd" =~ "shutdown" ]]; then
        whisper="System's Slumber"
    elif [[ "$cmd" =~ "monitor" || "$cmd" =~ "log" ]]; then
        whisper="Silent Observer"
    fi
    echo "$whisper"
}

# Main script logic
main() {
    echo "--- Nightly Cron Whisperer ---"
    echo "Listening to the temporal echoes of your scheduled tasks..."
    echo ""

    # Use 'crontab -l' to get current user's cron jobs
    # Mock rationale: In a real scenario, this would call the system's crontab.
    # For testing, we will override the 'crontab' command or feed it mocked input.
    local cron_output
    if command -v crontab &> /dev/null; then
        cron_output=$(crontab -l 2>/dev/null)
    else
        echo "Warning: 'crontab' command not found. Cannot retrieve cron jobs."
        echo "Assuming no cron jobs for analysis."
        cron_output=""
    fi

    if [ -z "$cron_output" ]; then
        echo "No cron jobs detected. The temporal fabric is calm."
        return 0
    fi

    local job_count=0
    echo "$cron_output" | while IFS= read -r line; do
        # Skip comments and empty lines
        if [[ "$line" =~ ^# ]] || [[ -z "$line" ]]; then
            continue
        fi

        # Extract schedule and command
        # This regex is a simplification and might not cover all cron formats
        # but it's good enough for a whimsical utility.
        if [[ "$line" =~ ^([^\ ]+\ [^\ ]+\ [^\ ]+\ [^\ ]+\ [^\ ]+)\ (.*)$ ]]; then
            local schedule="${BASH_REMATCH[1]}"
            local command="${BASH_REMATCH[2]}"
            local whisper=$(interpret_command "$command")

            # Check for hyper-frequent jobs
            if [[ "$schedule" == "* * * * *" ]]; then
                whisper="Hyper-Vigilant Sentinel ($whisper)"
            fi

            echo "  - Schedule: $schedule"
            echo "    Command:  $command"
            echo "    Whisper:  $whisper"
            echo ""
            job_count=$((job_count + 1))
        fi
    done

    if [ "$job_count" -eq 0 ]; then
        echo "No active cron jobs found after filtering. The temporal fabric is calm."
    else
        echo "--- End of Whispers ---"
        echo "Total active cron jobs analyzed: $job_count"
    fi
}

# Execute main function
main "$@"
