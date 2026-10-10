#!/bin/bash

# Nightly Doom List Prioritizer
# Prioritizes a given list of tasks based on keywords, assigning a "Doom Factor" and a whimsical comment.

# --- Configuration ---
# Keywords and their associated doom levels
declare -A HIGH_DOOM_KEYWORDS=(
    ["rift"]="5" ["temporal"]="5" ["anomaly"]="5" ["collapse"]="5" ["mutant"]="4"
    ["radiation"]="4" ["shelter"]="4" ["scavenge"]="3" ["critical"]="3" ["urgent"]="3"
)
declare -A MEDIUM_DOOM_KEYWORDS=(
    ["water"]="2" ["food"]="2" ["repair"]="2" ["signal"]="2" ["defense"]="2"
    ["secure"]="2" ["fortify"]="2" ["investigate"]="2"
)
declare -A LOW_DOOM_KEYWORDS=(
    ["clean"]="1" ["organize"]="1" ["inventory"]="1" ["recharge"]="1" ["meditate"]="1"
    ["tidy"]="1" ["sort"]="1"
)

# Whimsical comments based on doom level
HIGH_DOOM_COMMENTS=(
    "The fabric of reality is fraying. This cannot wait."
    "A whisper from the void suggests this is paramount."
    "The cosmic clock is ticking. Act now!"
    "Impending doom detected. Prioritize immediately."
    "The void hungers for your procrastination."
)
MEDIUM_DOOM_COMMENTS=(
    "Don't let the temporal distortions distract you."
    "Moderately important. The future is watching (and judging)."
    "This task radiates a faint glow of impending doom. Attend to it."
    "A solid step towards not becoming mutant chow."
    "The cosmic winds whisper of moderate urgency."
)
LOW_DOOM_COMMENTS=(
    "Even in the apocalypse, some things can wait... probably."
    "The cosmic dust bunnies can wait. Or can they?"
    "A moment of calm before the next storm. Or after."
    "Essential for morale, if not immediate survival."
    "The universe appreciates your tidiness, even if it's ending."
)

# --- Functions ---

# Function to get a random comment based on doom level
get_random_comment() {
    local doom_level_for_comment=$1 # This is the highest individual keyword score, not the sum
    local comments_array_name

    if (( doom_level_for_comment >= 4 )); then
        comments_array_name="HIGH_DOOM_COMMENTS"
    elif (( doom_level_for_comment >= 2 )); then
        comments_array_name="MEDIUM_DOOM_COMMENTS"
    else
        comments_array_name="LOW_DOOM_COMMENTS"
    fi

    # Mock rationale: In a real scenario, this would use shuf or RANDOM. For deterministic testing,
    # the test script will override this function to always return the first comment.
    local num_comments=${#${comments_array_name}[@]}
    local index=$(( RANDOM % num_comments ))
    
    echo "${!comments_array_name:$index:1}"
}

# Function to calculate doom factor for a task
calculate_doom_factor() {
    local task_description="$1"
    local doom_factor=0
    local highest_doom_level=0 # To help select comment category

    # Convert task to lowercase for case-insensitive matching
    local lower_task="${task_description,,}"

    # Check High Doom Keywords
    for keyword in "${!HIGH_DOOM_KEYWORDS[@]}"; do
        if [[ "$lower_task" =~ "$keyword" ]]; then
            doom_factor=$(( doom_factor + HIGH_DOOM_KEYWORDS[$keyword] ))
            if (( HIGH_DOOM_KEYWORDS[$keyword] > highest_doom_level )); then
                highest_doom_level=${HIGH_DOOM_KEYWORDS[$keyword]}
            fi
        fi
    done

    # Check Medium Doom Keywords
    for keyword in "${!MEDIUM_DOOM_KEYWORDS[@]}"; do
        if [[ "$lower_task" =~ "$keyword" ]]; then
            doom_factor=$(( doom_factor + MEDIUM_DOOM_KEYWORDS[$keyword] ))
            if (( MEDIUM_DOOM_KEYWORDS[$keyword] > highest_doom_level )); then
                highest_doom_level=${MEDIUM_DOOM_KEYWORDS[$keyword]}
            fi
        fi
    done

    # Check Low Doom Keywords
    for keyword in "${!LOW_DOOM_KEYWORDS[@]}"; do
        if [[ "$lower_task" =~ "$keyword" ]]; then
            doom_factor=$(( doom_factor + LOW_DOOM_KEYWORDS[$keyword] ))
            if (( LOW_DOOM_KEYWORDS[$keyword] > highest_doom_level )); then
                highest_doom_level=${LOW_DOOM_KEYWORDS[$keyword]}
            fi
        fi
    done

    # If no keywords matched, assign a default low doom factor
    if (( doom_factor == 0 )); then
        doom_factor=1
        highest_doom_level=1
    fi

    echo "$doom_factor $highest_doom_level"
}

# Function to determine urgency label
get_urgency_label() {
    local total_doom_factor=$1 # This is the sum of all keyword scores
    if (( total_doom_factor >= 4 )); then
        echo "CRITICAL"
    elif (( total_doom_factor >= 2 )); then
        echo "HIGH"
    else
        echo "LOW"
    fi
}

# --- Main Logic ---

# Read tasks from stdin or file
if [[ -t 0 ]]; then # Check if stdin is a terminal (no pipe)
    if [[ -n "$1" && -f "$1" ]]; then
        input_source="$1"
    else
        echo "Usage: $0 [task_file.txt]" >&2
        echo "       Pipe tasks to stdin: echo \"Task\" | $0" >&2
        exit 1
    fi
else
    input_source="/dev/stdin"
fi

declare -a tasks_with_doom

while IFS= read -r task; do
    if [[ -z "$task" ]]; then
        continue # Skip empty lines
    fi
    read -r doom_factor highest_doom_level <<< "$(calculate_doom_factor "$task")"
    comment="$(get_random_comment "$highest_doom_level")"
    urgency_label="$(get_urgency_label "$doom_factor")"
    tasks_with_doom+=("$doom_factor|$urgency_label|$comment|$task")
done < "$input_source"

# Sort tasks by doom factor (descending)
IFS=$'\n' sorted_tasks=($(sort -t '|' -k1,1nr <<<"${tasks_with_doom[*]}"))
unset IFS

echo "--- Doom List Prioritization Report ---"
for entry in "${sorted_tasks[@]}"; do
    IFS='|' read -r doom_factor urgency_label comment task <<< "$entry"
    printf "Doom Factor: %-2s | Urgency: %-8s | Comment: %s | Task: %s\n" "$doom_factor" "$urgency_label" "$comment" "$task"
done
