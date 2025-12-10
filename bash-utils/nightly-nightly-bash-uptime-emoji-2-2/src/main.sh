#!/bin/bash

# Nightly Bash Uptime Emoji 2
# A whimsical utility to display system uptime with emoji and ASCII art

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to get uptime in seconds
get_uptime_seconds() {
    if [[ $(uname -s) == "Darwin" ]]; then
        # macOS
        sysctl -n kern.boottime | awk -F'[=,]' '{print $2}'
    else
        # Linux
        cat /proc/uptime | awk '{print int($1)}'
    fi
}

# Function to format uptime
format_uptime() {
    local uptime_seconds=$1
    local days=$((uptime_seconds / 86400))
    local hours=$(((uptime_seconds % 86400) / 3600))
    local minutes=$(((uptime_seconds % 3600) / 60))
    
    if [[ $days -gt 0 ]]; then
        echo "${days} day(s), ${hours} hour(s), ${minutes} minute(s)"
    elif [[ $hours -gt 0 ]]; then
        echo "${hours} hour(s), ${minutes} minute(s)"
    else
        echo "${minutes} minute(s)"
    fi
}

# Function to create progress bar
create_progress_bar() {
    local percentage=$1
    local width=20
    local filled=$((percentage * width / 100))
    local empty=$((width - filled))
    
    printf "${GREEN}"
    for ((i=0; i<filled; i++)); do printf "█"; done
    printf "${NC}"
    printf "${RED}"
    for ((i=0; i<empty; i++)); do printf "░"; done
    printf "${NC}"
}

# Function to display ASCII art
show_ascii_art() {
    local uptime_seconds=$1
    local days=$((uptime_seconds / 86400))
    
    if [[ $days -ge 7 ]]; then
        # Week+ uptime - trophy
        cat << 'EOF'

   .-"""""-.
  /         \
 /           \
|             |
|     🏆     |
|             |
 \           /
  \         /
   '-.....-'

EOF
    elif [[ $days -ge 1 ]]; then
        # Day+ uptime - rocket
        cat << 'EOF'

    🚀
   / \ 
  /   \ 
 /_____\ 
   | |
   | |

EOF
    else
        # Less than a day - coffee cup
        cat << 'EOF'

   ☕
  ┌───┐
  │   │
  └───┘
   ~~~
   ~~~

EOF
    fi
}

# Function to get encouraging message
get_encouragement() {
    local uptime_seconds=$1
    local messages=(
        "Keep going! You're doing great! 💪"
        "Staying powered on like a champ! 🏆"
        "Uptime goals achieved! 🎯"
        "System's feeling fresh! 🌟"
        "You've got this! 🔥"
    )
    
    # Select message based on uptime
    if [[ $uptime_seconds -gt 604800 ]]; then
        echo "${messages[0]}" # Week+
    elif [[ $uptime_seconds -gt 86400 ]]; then
        echo "${messages[1]}" # Day+
    elif [[ $uptime_seconds -gt 3600 ]]; then
        echo "${messages[2]}" # Hour+
    elif [[ $uptime_seconds -gt 600 ]]; then
        echo "${messages[3]}" # 10+ minutes
    else
        echo "${messages[4]}" # Less than 10 minutes
    fi
}

# Function to calculate uptime percentage (mock for demo)
# In a real system, you might compare to a target uptime
get_uptime_percentage() {
    local uptime_seconds=$1
    # Mock calculation - for demo purposes
    # Assume target uptime is 30 days (2592000 seconds)
    local target=2592000
    local percentage=$((uptime_seconds * 100 / target))
    
    # Cap at 100%
    if [[ $percentage -gt 100 ]]; then
        percentage=100
    fi
    
    echo $percentage
}

# Main function
main() {
    echo -e "${CYAN}=== Nightly Bash Uptime Emoji 2 ===${NC}\n"
    
    # Get uptime
    uptime_seconds=$(get_uptime_seconds)
    uptime_formatted=$(format_uptime $uptime_seconds)
    
    # Display uptime
    echo -e "${BLUE}🚀 System Uptime:${NC} ${uptime_formatted}"
    
    # Calculate and display progress
    percentage=$(get_uptime_percentage $uptime_seconds)
    echo -e "\n${YELLOW}Progress:${NC} $(create_progress_bar $percentage) ${percentage}% ${get_encouragement $uptime_seconds}"
    
    # Show ASCII art
    show_ascii_art $uptime_seconds
    
    # Display current time
    echo -e "${PURPLE}Current time:${NC} $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${GREEN}Boot time:${NC} $(date -d '@'$(($(date +%s) - uptime_seconds)) '+%Y-%m-%d %H:%M:%S')"
}

# Run main function
main
