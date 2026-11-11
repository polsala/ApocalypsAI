#!/bin/bash

set -euo pipefail

# --- Test Setup ---
TEST_DIR=$(mktemp -d)
ECHOES_DIR="${TEST_DIR}/echoes"

# Mock rationale: We need to simulate docker commands without actually running Docker,
# ensuring tests are deterministic and offline. This mock replaces the real 'docker'
# command during testing, capturing its arguments or returning predefined output.

mocked_docker_run_args=""
docker() {
    local cmd="$1"
    shift
    case "${cmd}" in
        "inspect")
            local container_id="$1"
            if [[ "${container_id}" == "test_container" ]]; then
                echo '[
                    {
                        "Config": {
                            "Env": [
                                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                                "MY_VAR=value1",
                                "ANOTHER_VAR=value2"
                            ]
                        },
                        "HostConfig": {
                            "Binds": [
                                "/host/path1:/container/path1:rw",
                                "/host/path2:/container/path2:ro"
                            ]
                        }
                    }
                ]'
            elif [[ "${container_id}" == "container_no_volumes" ]]; then
                 echo '[
                    {
                        "Config": {
                            "Env": [
                                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                                "NO_VOL_VAR=test"
                            ]
                        },
                        "HostConfig": {
                            "Binds": null
                        }
                    }
                ]'
            else
                echo "Error: No such container: ${container_id}" >&2
                return 1
            fi
            ;;
        "run")
            # Capture the arguments passed to docker run
            mocked_docker_run_args="$@"
            echo "MOCKED_DOCKER_RUN_CALLED: $@"
            ;;
        *)
            echo "MOCKED_DOCKER: Unknown command: ${cmd}" >&2
            return 1
            ;;
    esac
}

# Source the script to be tested, overriding its ECHOES_DIR
# Mock rationale: We need to redirect the script's internal ECHOES_DIR to our temporary test directory
# to ensure tests are isolated and don't affect real data.
export ECHOES_DIR="${ECHOES_DIR}"
source src/echo-cli.sh

# --- Test Functions ---

function assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    if [[ "${expected}" != "${actual}" ]]; then
        echo "FAIL: ${message}"
        echo "  Expected: '${expected}'"
        echo "  Actual:   '${actual}'"
        exit 1
    else
        echo "PASS: ${message}"
    fi
}

function assert_file_exists() {
    local file="$1"
    local message="$2"
    if [[ ! -f "${file}" ]]; then
        echo "FAIL: ${message} - File '${file}' does not exist."
        exit 1
    else
        echo "PASS: ${message}"
    fi
}

function assert_file_not_exists() {
    local file="$1"
    local message="$2"
    if [[ -f "${file}" ]]; then
        echo "FAIL: ${message} - File '${file}' unexpectedly exists."
        exit 1
    else
        echo "PASS: ${message}"
    fi
}

function run_test() {
    local test_name="$1"
    local func_name="test_${test_name}"
    echo "\nRunning test: ${test_name}"
    "${func_name}"
}

# --- Actual Tests ---

function test_capture_success() {
    local echo_name="my-test-echo"
    local echo_file="${ECHOES_DIR}/${echo_name}.json"

    capture_echo "test_container" "${echo_name}"

    assert_file_exists "${echo_file}" "Captured echo file should exist"

    local expected_content='{
  "env_vars": {
    "PATH":"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "MY_VAR":"value1",
    "ANOTHER_VAR":"value2"
  },
  "volumes": [
    "/host/path1:/container/path1:rw",
    "/host/path2:/container/path2:ro"
  ]
}'
    local actual_content=$(cat "${echo_file}" | sed 's/^[ \t]*//;s/[ \t]*$//' | tr -d '\n') # Remove leading/trailing spaces and newlines for comparison
    local expected_content_compact=$(echo "${expected_content}" | sed 's/^[ \t]*//;s/[ \t]*$//' | tr -d '\n')

    assert_equals "${expected_content_compact}" "${actual_content}" "Captured echo content should match expected"
}

function test_capture_no_volumes() {
    local echo_name="no-vol-echo"
    local echo_file="${ECHOES_DIR}/${echo_name}.json"

    capture_echo "container_no_volumes" "${echo_name}"

    assert_file_exists "${echo_file}" "Captured echo file for no volumes should exist"

    local expected_content='{
  "env_vars": {
    "PATH":"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "NO_VOL_VAR":"test"
  },
  "volumes": [

  ]
}'
    local actual_content=$(cat "${echo_file}" | sed 's/^[ \t]*//;s/[ \t]*$//' | tr -d '\n')
    local expected_content_compact=$(echo "${expected_content}" | sed 's/^[ \t]*//;s/[ \t]*$//' | tr -d '\n')

    assert_equals "${expected_content_compact}" "${actual_content}" "Captured echo content for no volumes should match expected"
}

function test_list_echoes() {
    local echo_name1="echo1"
    local echo_name2="echo2"
    touch "${ECHOES_DIR}/${echo_name1}.json"
    touch "${ECHOES_DIR}/${echo_name2}.json"

    local output
    output=$(list_echoes)

    echo "List output: ${output}"
    [[ "${output}" == *"- ${echo_name1}"* ]] || { echo "FAIL: List should show ${echo_name1}"; exit 1; }
    [[ "${output}" == *"- ${echo_name2}"* ]] || { echo "FAIL: List should show ${echo_name2}"; exit 1; }
    echo "PASS: List echoes should show created echoes"
}

function test_delete_echo() {
    local echo_name="to-delete-echo"
    local echo_file="${ECHOES_DIR}/${echo_name}.json"
    touch "${echo_file}"

    assert_file_exists "${echo_file}" "File should exist before deletion"

    delete_echo "${echo_name}"

    assert_file_not_exists "${echo_file}" "File should not exist after deletion"
}

function test_replay_echo() {
    local echo_name="replay-test-echo"
    local image_name="my-replay-image:latest"
    local echo_file="${ECHOES_DIR}/${echo_name}.json"

    # Create a dummy echo file for replay
    cat <<EOF > "${echo_file}"
{
  "env_vars": {
    "REPLAY_VAR":"replay_value",
    "ANOTHER_REPLAY_VAR":"another_replay_value"
  },
  "volumes": [
    "/host/replay1:/container/replay1:rw",
    "/host/replay2:/container/replay2:ro"
  ]
}
EOF

    replay_echo "${echo_name}" "${image_name}" "/bin/sh" "-c" "echo Hello"

    local expected_args="run --rm -e REPLAY_VAR=replay_value -e ANOTHER_REPLAY_VAR=another_replay_value -v /host/replay1:/container/replay1:rw -v /host/replay2:/container/replay2:ro ${image_name} /bin/sh -c echo Hello"
    assert_equals "${expected_args}" "${mocked_docker_run_args}" "Replay should construct correct docker run command"
}

function test_replay_echo_no_command() {
    local echo_name="replay-no-cmd-echo"
    local image_name="my-image:1.0"
    local echo_file="${ECHOES_DIR}/${echo_name}.json"

    cat <<EOF > "${echo_file}"
{
  "env_vars": {
    "NO_CMD_VAR":"test_val"
  },
  "volumes": [
  ]
}
EOF

    replay_echo "${echo_name}" "${image_name}"

    local expected_args="run --rm -e NO_CMD_VAR=test_val ${image_name}"
    assert_equals "${expected_args}" "${mocked_docker_run_args}" "Replay without command should construct correct docker run command"
}

# --- Run all tests ---
run_test "capture_success"
run_test "capture_no_volumes"
run_test "list_echoes"
run_test "delete_echo"
run_test "replay_echo"
run_test "replay_echo_no_command"

# --- Cleanup ---
rm -rf "${TEST_DIR}"
echo "\nAll tests passed!"
