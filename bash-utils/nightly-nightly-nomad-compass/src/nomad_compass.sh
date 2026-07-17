#!/bin/bash

# --- Configuration ---
COLOR_RESET='\033[0m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_BLUE='\033[0;34m'
COLOR_CYAN='\033[0;36m'
COLOR_MAGENTA='\033[0;35m'

# --- Utility Functions ---

get_uptime() {
    echo -e "${COLOR_GREEN}Uptime:${COLOR_RESET} $(uptime -p 2>/dev/null || echo 'N/A')"
}

get_ip_address() {
    local ip=$(hostname -I 2>/dev/null | awk '{print $1}')
    if [[ -z "$ip" ]]; then
        ip="N/A"
    fi
    echo -e "${COLOR_YELLOW}IP Address:${COLOR_RESET} $ip"
}

get_disk_usage() {
    local disk_info=$(df -h . 2>/dev/null | awk 'NR==2 {print $5 " used of " $2}')
    if [[ -z "$disk_info" ]]; then
        disk_info="N/A"
    fi
    echo -e "${COLOR_BLUE}Disk Usage:${COLOR_RESET} $disk_info"
}

get_memory_usage() {
    local mem_info=$(free -h 2>/dev/null | awk 'NR==2 {print $3 " used of " $2}')
    if [[ -z "$mem_info" ]]; then
        mem_info="N/A"
    fi
    echo -e "${COLOR_MAGENTA}Memory Usage:${COLOR_RESET} $mem_info"
}

get_current_dir() {
    echo -e "${COLOR_CYAN}Current Path:${COLOR_RESET} $(pwd)"
}

get_git_status() {
    if command -v git &>/dev/null && git rev-parse --is-inside-work-tree &>/dev/null; then
        local status=$(git status --short --branch 2>/dev/null)
        if [[ -n "$status" ]]; then
            echo -e "${COLOR_GREEN}Git Status:${COLOR_RESET}\n$(echo "$status" | sed 's/^/  /')"
        else
            echo -e "${COLOR_GREEN}Git Status:${COLOR_RESET} Clean"
        fi
    else
        echo -e "${COLOR_GREEN}Git Status:${COLOR_RESET} Not a Git repository"
    fi
}

# --- Main Execution ---
echo -e "\n${COLOR_CYAN}--- Nightly Digital Nomad's Compass ---${COLOR_RESET}"
get_uptime
get_ip_address
get_disk_usage
get_memory_usage
get_current_dir
get_git_status
echo -e "${COLOR_CYAN}---------------------------------------${COLOR_RESET}\n"
