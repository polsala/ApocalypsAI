import json
import argparse
import os

def parse_docker_inspect(file_path):
    """Parses a Docker inspect JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)[0] # inspect returns a list
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing inspect file {file_path}: {e}")
        return None

def parse_env_vars(env_list):
    """Parses a list of 'KEY=VALUE' strings into a dictionary."""
    return {item.split('=', 1)[0]: item.split('=', 1)[1] for item in env_list if '=' in item}

def compare_env_vars(image_env, container_env):
    """Compares environment variables between image and container."""
    drift = {
        "added": [],
        "changed": []
    }
    image_env_dict = parse_env_vars(image_env)
    container_env_dict = parse_env_vars(container_env)

    for key, value in container_env_dict.items():
        if key not in image_env_dict:
            drift["added"].append(f"{key}={value}")
        elif image_env_dict[key] != value:
            drift["changed"].append(f"{key}={value} (was: {image_env_dict[key]})")
    return drift

def compare_exposed_ports(image_ports, container_ports):
    """Compares exposed ports between image and container."""
    drift = {
        "new": []
    }
    image_exposed = set(image_ports.keys() if image_ports else [])
    container_exposed = set(container_ports.keys() if container_ports else [])

    for port in container_exposed:
        if port not in image_exposed:
            drift["new"].append(port)
    return drift

def check_temporal_marker(ls_output_file, marker_file_path="/tmp/chrono_drift_marker.txt"):
    """Checks for the presence of a specific marker file in the container's filesystem listing."""
    try:
        with open(ls_output_file, 'r') as f:
            content = f.read()
            if marker_file_path in content:
                return True
            # Also check for just the filename if ls -R /tmp was used
            if os.path.basename(marker_file_path) in content and marker_file_path.startswith('/tmp'):
                return True
    except FileNotFoundError:
        print(f"Warning: Filesystem listing file {ls_output_file} not found. Cannot check for marker.")
    return False

def main():
    parser = argparse.ArgumentParser(description="Nightly Docker Chrono-Drift Detector")
    parser.add_argument("--container-id", required=True, help="ID or name of the container to scan.")
    parser.add_argument("--image-inspect-file", required=True, help="Path to the mock or live image inspect JSON file.")
    parser.add_argument("--container-inspect-file", required=True, help="Path to the mock or live container inspect JSON file.")
    parser.add_argument("--container-ls-file", required=True, help="Path to the mock or live container ls -R / output file.")
    args = parser.parse_args()

    container_id = args.container_id

    image_data = parse_docker_inspect(args.image_inspect_file)
    container_data = parse_docker_inspect(args.container_inspect_file)

    if not image_data or not container_data:
        print("Error: Could not load necessary inspect data. Exiting.")
        exit(1)

    print(f"Scanning container: {container_id} (ID: {container_data['Id'][:12]})")
    print("\n--- Chrono-Drift Report ---\n")

    drift_detected = False

    # 1. Environment Variable Drift
    image_env = image_data.get('Config', {}).get('Env', [])
    container_env = container_data.get('Config', {}).get('Env', [])
    env_drift = compare_env_vars(image_env, container_env)
    if env_drift["added"] or env_drift["changed"]:
        drift_detected = True
        print("Environment Variable Drift:")
        for item in env_drift["added"]:
            print(f"  - Added: {item}")
        for item in env_drift["changed"]:
            print(f"  - Changed: {item}")
        print()

    # 2. Exposed Port Anomalies
    image_exposed_ports = image_data.get('Config', {}).get('ExposedPorts', {})
    container_network_ports = container_data.get('NetworkSettings', {}).get('Ports', {})
    exposed_port_drift = compare_exposed_ports(image_exposed_ports, container_network_ports)
    if exposed_port_drift["new"]:
        drift_detected = True
        print("Exposed Port Anomalies:")
        for port in exposed_port_drift["new"]:
            print(f"  - New Port Exposed: {port}")
        print()

    # 3. Temporal Marker File Check
    marker_found = check_temporal_marker(args.container_ls_file)
    if marker_found:
        drift_detected = True
        print("Temporal Marker File Detected:")
        print(f"  - Found /tmp/chrono_drift_marker.txt. This indicates an unexpected filesystem alteration.")
        print()

    if not drift_detected:
        print("[NO DRIFT DETECTED]")
        print(f"Container '{container_id}' appears stable across monitored parameters.")
    else:
        print("[DRIFT DETECTED]")
        print(f"Container '{container_id}' shows signs of temporal instability!")

if __name__ == "__main__":
    main()
