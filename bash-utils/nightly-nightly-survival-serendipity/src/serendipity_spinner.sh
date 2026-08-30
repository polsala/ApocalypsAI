#!/bin/bash

# Define tasks with associated energy levels
declare -A TASKS
TASKS["Scavenge for supplies"]="medium high"
TASKS["Fortify shelter defenses"]="high"
TASKS["Repair essential equipment"]="medium"
TASKS["Rest and recuperate"]="low"
TASKS["Organize inventory"]="low medium"
TASKS["Scout immediate perimeter"]="medium"
TASKS["Craft useful tools"]="medium"
TASKS["Tend to garden/crops"]="low medium"
TASKS["Clean and maintain weapons"]="low medium"
TASKS["Study survival guides"]="low"

# Function to get tasks based on mood
# Outputs tasks, one per line, sorted alphabetically for determinism
get_tasks_for_mood() {
    local mood="$1"
    local filtered_tasks=()
    for task in "${!TASKS[@]}"; do
        local energy_levels="${TASKS[$task]}"
        if [[ " ${energy_levels} " =~ " ${mood} " ]]; then
            filtered_tasks+=("$task")
        fi
    done
    # Sort the tasks alphabetically for deterministic output
    printf "%s\n" "${filtered_tasks[@]}" | sort
}

# Function to select a random task from a list
# Expects tasks as separate arguments
select_random_task() {
    local tasks_array=("$@")
    if [ ${#tasks_array[@]} -eq 0 ]; then
        echo "No tasks available for selection."
        return 1
    }
    # Use shuf for random selection. If shuf is not available, fall back to $RANDOM.
    if command -v shuf &> /dev/null; then
        # Correctly pipe array elements as separate lines to shuf
        printf "%s\n" "${tasks_array[@]}" | shuf -n 1
    else
        # Fallback for systems without shuf (less robust randomness but works)
        local num_tasks=${#tasks_array[@]}
        local random_index=$(( RANDOM % num_tasks ))
        echo "${tasks_array[$random_index]}"
    fi
}

main() {
    if [ "$#" -ne 1 ]; then
        echo "Usage: $0 <mood>"
        echo "Available moods: low, medium, high"
        exit 1
    fi

    local mood="$1"
    mood=$(echo "$mood" | tr '[:upper:]' '[:lower:]') # Convert to lowercase

    case "$mood" in
        "low"|"medium"|"high")
            ;;
        *)
            echo "Error: Invalid mood '$mood'. Available moods: low, medium, high."
            exit 1
            ;;
    esac

    # Get tasks, one per line, then read into an array
    local tasks_output=$(get_tasks_for_mood "$mood")
    IFS=$'\n' read -r -d '' -a tasks_array <<< "$tasks_output"

    if [ ${#tasks_array[@]} -eq 0 ]; then
        echo "No tasks found for mood: $mood. Perhaps the task list needs updating?"
        exit 1
    fi

    local chosen_task=$(select_random_task "${tasks_array[@]}")
    echo "Your Serendipity Spinner suggests: $chosen_task"
}

# Call the main function with all arguments if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
