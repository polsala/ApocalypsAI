#!/bin/bash

# ApocalypsAI Nightly Integrator - Apocalypse Task Prioritizer

TASK_FILE="${APOCALYPSE_TASK_FILE:-$HOME/.apocalypse_tasks}"
declare -a APOCALYPSE_TIPS=(
    "Always check your six, even when sorting irradiated socks."
    "A well-maintained Geiger counter is a survivor's best friend."
    "Barter wisely. A can of beans today is worth two tomorrow."
    "Never trust a smiling stranger in the wasteland. Or a frowning one."
    "Keep your water purifier clean. Hydration is key to survival."
    "Temporal anomalies are tricky. Document everything, even if it vanishes."
    "Remember the old world. It helps you appreciate the new."
    "Sharpen your wits as often as your blade."
    "The best defense is a good offense... or a really fast escape route."
    "Don't forget to laugh. Even the void has a sense of humor."
)

# Ensure the task file exists
_init_task_file() {
    if [[ ! -f "$TASK_FILE" ]]; then
        echo "# Apocalypse Task Log - Created $(date +%Y-%m-%d)" > "$TASK_FILE"
        echo "# Format: ID | Status | Category | Priority | Task Description" >> "$TASK_FILE"
        echo "# Status: [ ] = Pending, [X] = Completed" >> "$TASK_FILE"
        echo "# Categories: CRITICAL, SCAVENGE, MORALE, TEMPORAL, MISC" >> "$TASK_FILE"
        echo "# Priorities: 1 (Highest) to 5 (Lowest)" >> "$TASK_FILE"
    fi
}

# Get a random apocalypse tip
_get_random_tip() {
    local num_tips=${#APOCALYPSE_TIPS[@]}
    local random_index=$(( RANDOM % num_tips ))
    echo "${APOCALYPSE_TIPS[$random_index]}"
}

# Add a new task
add_task() {
    local category="$1"
    local priority="$2"
    local description="$3"

    if [[ -z "$category" || -z "$priority" || -z "$description" ]]; then
        echo "Usage: add <CATEGORY> <PRIORITY> <DESCRIPTION>"
        echo "Categories: CRITICAL, SCAVENGE, MORALE, TEMPORAL, MISC"
        echo "Priorities: 1 (Highest) to 5 (Lowest)"
        return 1
    fi

    category=$(echo "$category" | tr '[:lower:]' '[:upper:]')
    if ! [[ "$category" =~ ^(CRITICAL|SCAVENGE|MORALE|TEMPORAL|MISC)$ ]]; then
        echo "Error: Invalid category. Choose from CRITICAL, SCAVENGE, MORALE, TEMPORAL, MISC."
        return 1
    fi

    if ! [[ "$priority" =~ ^[1-5]$ ]]; then
        echo "Error: Priority must be a number between 1 and 5."
        return 1
    fi

    _init_task_file

    local last_id=$(grep -E '^[0-9]+ \|' "$TASK_FILE" | awk -F ' \| ' '{print $1}' | sort -nr | head -n 1)
    local new_id=$((last_id + 1))
    if [[ -z "$last_id" ]]; then
        new_id=1
    fi

    echo "$new_id | [ ] | $category | $priority | $description" >> "$TASK_FILE"
    echo "Task added: \"$description\" (ID: $new_id, Category: $category, Priority: $priority)"
}

# List tasks
list_tasks() {
    local filter_category="$1"
    _init_task_file

    echo "--- Apocalypse Task Log ---"
    echo "Wasteland Wisdom: $(_get_random_tip)"
    echo "--------------------------"

    local tasks_found=0
    grep -E '^[0-9]+ \|' "$TASK_FILE" | while IFS=' | ' read -r id status category priority description; do
        if [[ -z "$filter_category" || "$(echo "$category" | tr '[:lower:]' '[:upper:]')" == "$(echo "$filter_category" | tr '[:lower:]' '[:upper:]')" ]]; then
            echo "ID: $id | Status: $status | Cat: $category | Prio: $priority | Task: $description"
            tasks_found=$((tasks_found + 1))
        fi
    done | sort -t '|' -k 4,4n -k 3,3
    
    if [[ "$tasks_found" -eq 0 ]]; then
        if [[ -n "$filter_category" ]]; then
            echo "No tasks found for category '$filter_category'."
        else
            echo "No tasks found. Time to scavenge for new objectives!"
        fi
    fi
    echo "--------------------------"
}

# Mark a task as complete
complete_task() {
    local task_id="$1"
    if [[ -z "$task_id" ]]; then
        echo "Usage: complete <TASK_ID>"
        return 1
    }

    _init_task_file
    
    local temp_file=$(mktemp)
    local task_found=0
    while IFS= read -r line; do
        if [[ "$line" =~ ^([0-9]+) \| \[ \] \| (.*) ]]; then
            local current_id="${BASH_REMATCH[1]}"
            if [[ "$current_id" -eq "$task_id" ]]; then
                echo "${line/[ ]/[X]}" >> "$temp_file"
                echo "Task ID $task_id marked as completed."
                task_found=1
            else
                echo "$line" >> "$temp_file"
            fi
        else
            echo "$line" >> "$temp_file"
        fi
    done < "$TASK_FILE"
    mv "$temp_file" "$TASK_FILE"

    if [[ "$task_found" -eq 0 ]]; then
        echo "Error: Task ID $task_id not found or already completed."
        return 1
    }
}

# Clear all completed tasks
clear_completed_tasks() {
    _init_task_file
    local temp_file=$(mktemp)
    grep -v '\[X\]' "$TASK_FILE" > "$temp_file"
    mv "$temp_file" "$TASK_FILE"
    echo "All completed tasks cleared from the log."
}

# Main script logic
case "$1" in
    add)
        shift
        add_task "$@"
        ;;
    list)
        shift
        list_tasks "$@"
        ;;
    complete)
        shift
        complete_task "$@"
        ;;
    clear)
        clear_completed_tasks
        ;;
    *)
        echo "Apocalypse Task Prioritizer"
        echo "Usage: $0 <command> [arguments]"
        echo ""
        echo "Commands:"
        echo "  add <CATEGORY> <PRIORITY> <DESCRIPTION>  - Add a new task"
        echo "  list [CATEGORY]                          - List tasks (optional filter by category)"
        echo "  complete <TASK_ID>                       - Mark a task as completed"
        echo "  clear                                    - Clear all completed tasks"
        echo ""
        echo "Categories: CRITICAL, SCAVENGE, MORALE, TEMPORAL, MISC"
        echo "Priorities: 1 (Highest) to 5 (Lowest)"
        exit 1
        ;;
esac
