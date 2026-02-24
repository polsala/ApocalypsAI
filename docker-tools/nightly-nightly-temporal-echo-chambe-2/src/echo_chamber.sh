#!/bin/bash

set -euo pipefail

# Function to display usage
usage() {
    echo "Usage: echo_chamber.sh <command>"
    echo "Commands:"
    echo "  record <output_file.json> <command...>"
    echo "    Records the stdout, stderr, exit code, and duration of a command."
    echo "  replay <input_file.json> [--delay-factor <factor>]"
    echo "    Replays the recorded stdout and stderr, and exits with the recorded code."
    echo "    --delay-factor: Multiplies the recorded duration for replay delay (default: 1)."
    exit 1
}

# Function to record a command's output
record_command() {
    local output_file="$1"
    shift
    local cmd_array=("$@")
    local cmd_string=$(printf "%q " "${cmd_array[@]}")

    echo "Recording command: $cmd_string"

    local start_time=$(date +%s.%N)
    local stdout_output=""
    local stderr_output=""
    local exit_code=0

    # Execute command, capture stdout/stderr, and exit code
    # Using a temporary file for stdout/stderr to avoid pipe issues with complex commands
    local tmp_stdout=$(mktemp)
    local tmp_stderr=$(mktemp)

    # Run the command, redirecting stdout and stderr to temporary files
    # and capturing its exit code.
    if ! "${cmd_array[@]}" > "$tmp_stdout" 2> "$tmp_stderr"; then
        exit_code=$?
    fi

    local end_time=$(date +%s.%N)
    local duration=$(echo "$end_time - $start_time" | bc -l)

    stdout_output=$(cat "$tmp_stdout")
    stderr_output=$(cat "$tmp_stderr")

    rm "$tmp_stdout" "$tmp_stderr"

    # Create JSON output
    local cmd_json_array=$(printf '%s\n' "${cmd_array[@]}" | jq -R . | jq -s .)

    jq -n \
        --argjson cmd "$cmd_json_array" \
        --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
        --arg duration "$duration" \
        --arg stdout "$stdout_output" \
        --arg stderr "$stderr_output" \
        --arg exit_code "$exit_code" \
        '{
            "command": $cmd,
            "timestamp": $timestamp,
            "duration_seconds": ($duration | tonumber),
            "stdout": $stdout,
            "stderr": $stderr,
            "exit_code": ($exit_code | tonumber)
        }' > "$output_file"

    echo "Recorded echo saved to $output_file"
}

# Function to replay a recorded output
replay_command() {
    local input_file="$1"
    local delay_factor=1
    shift

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --delay-factor)
                delay_factor="$2"
                shift 2
                ;;
            *)
                echo "Unknown option: $1"
                usage
                ;;
        esac
    done

    if [[ ! -f "$input_file" ]]; then
        echo "Error: Input file '$input_file' not found."
        exit 1
    fi

    echo "Replaying echo from $input_file"

    local json_content=$(cat "$input_file")

    local stdout_to_print=$(echo "$json_content" | jq -r '.stdout')
    local stderr_to_print=$(echo "$json_content" | jq -r '.stderr')
    local exit_code_to_use=$(echo "$json_content" | jq -r '.exit_code')
    local recorded_duration=$(echo "$json_content" | jq -r '.duration_seconds')

    # Introduce delay
    local actual_delay=$(echo "$recorded_duration * $delay_factor" | bc -l)
    if (( $(echo "$actual_delay > 0" | bc -l) )); then
        echo "Simulating temporal distortion: waiting for ${actual_delay} seconds..." >&2
        sleep "$actual_delay"
    fi

    # Print stdout
    if [[ -n "$stdout_to_print" ]]; then
        printf "%s" "$stdout_to_print"
    fi

    # Print stderr
    if [[ -n "$stderr_to_print" ]]; then
        printf "%s" "$stderr_to_print" >&2
    fi

    echo "Replay complete. Exiting with code $exit_code_to_use." >&2
    exit "$exit_code_to_use"
}

# Main logic
if [[ $# -eq 0 ]]; then
    usage
fi

case "$1" in
    record)
        if [[ $# -lt 3 ]]; then
            echo "Error: 'record' command requires an output file and a command."
            usage
        fi
        shift
        record_command "$@"
        ;;
    replay)
        if [[ $# -lt 2 ]]; then
            echo "Error: 'replay' command requires an input file."
            usage
        fi
        shift
        replay_command "$@"
        ;;
    *)
        usage
        ;;
esac
