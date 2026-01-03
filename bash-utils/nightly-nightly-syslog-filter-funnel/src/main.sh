#!/bin/bash

# Nightly Syslog Filter Funnel
# A whimsical bash script to filter and funnel syslog messages with fun tags.

# Function to add a whimsical tag to a message
add_tag() {
    local message="$1"
    local tag=""

    # Whimsical tagging logic
    if [[ "$message" == *"error"* ]]; then
        tag="[🚨 ALERT!]";
    elif [[ "$message" == *"warning"* ]]; then
        tag="[⚠️ CAUTION]";
    elif [[ "$message" == *"info"* || "$message" == *"notice"* ]]; then
        tag="[✨ INFO]";
    elif [[ "$message" == *"debug"* ]]; then
        tag="[🔬 DEBUG]";
    elif [[ "$message" == *"critical"* || "$message" == *"emerg"* ]]; then
        tag="[💥 CRITICAL]";
    else
        tag="[❓ UNKNOWN]";
    fi

    echo "$tag $message"
}

# Main processing loop
while IFS= read -r line;
do
    # Add the whimsical tag
    tagged_line=$(add_tag "$line")

    # Simple funneling: output all tagged lines to stdout
    # More complex funneling (e.g., to different files based on tag) would require
    # additional logic here, potentially using grep or case statements on the tag.
    echo "$tagged_line"

    # Example of more advanced funneling (commented out):
    # if [[ "$tagged_line" == *"[🚨 ALERT!]"* ]]; then
    #     echo "$tagged_line" >> errors.log
    # elif [[ "$tagged_line" == *"[⚠️ CAUTION]"* ]]; then
    #     echo "$tagged_line" >> warnings.log
    # else
    #     echo "$tagged_line" >> general.log
    # fi

done
