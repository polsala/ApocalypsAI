#!/bin/bash

COMMAND_LOG_FILE="/app/vault/commands.log"

touch "$COMMAND_LOG_FILE"

case "$1" in
    record)
        if [ -z "$2" ]; then
            echo "Usage: scribe.sh record \"<command_to_record>\""
            exit 1
        fi
        TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
        echo "[$TIMESTAMP] $2" >> "$COMMAND_LOG_FILE"
        echo "Scribed: \"$2\""
        ;;
    replay)
        if [ ! -s "$COMMAND_LOG_FILE" ]; then
            echo "The temporal vault is empty. No echoes to replay."
            exit 0
        fi
        echo "--- Temporal Echoes from the Vault ---"
        while IFS= read -r line; do
            echo "[Temporal Echo]: $line"
        done < "$COMMAND_LOG_FILE"
        echo "--------------------------------------"
        ;;
    clear)
        > "$COMMAND_LOG_FILE"
        echo "Temporal vault cleared. Memories dispersed into the void."
        ;;
    *)
        echo "Usage: scribe.sh [record \"<command>\" | replay | clear]"
        exit 1
        ;;
esac
