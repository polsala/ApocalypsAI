import argparse
import subprocess
import datetime
from dateutil.relativedelta import relativedelta
import time
import re

def parse_drift_spec(drift_spec):
    """Parses a drift specification string (e.g., '+1d', '-2h') into a relativedelta object."""
    match = re.match(r"^([+-]?)(\d+)([dhms])$", drift_spec)
    if not match:
        raise ValueError(f"Invalid drift specification: {drift_spec}. Expected format like '+1d', '-2h'.")

    sign = -1 if match.group(1) == '-' else 1
    value = int(match.group(2))
    unit = match.group(3)

    if unit == 'd':
        return relativedelta(days=sign * value)
    elif unit == 'h':
        return relativedelta(hours=sign * value)
    elif unit == 'm':
        return relativedelta(minutes=sign * value)
    elif unit == 's':
        return relativedelta(seconds=sign * value)
    else:
        raise ValueError(f"Unknown drift unit: {unit}")

def apply_temporal_drift(env_vars, drift_spec):
    """Applies temporal drift to specific environment variables."""
    if not drift_spec:
        return env_vars

    drift = parse_drift_spec(drift_spec)
    drifted_env_vars = []

    for env_var in env_vars:
        key, value = env_var.split('=', 1)
        if key == 'CAPSULE_DATE':
            try:
                # Convert date string to datetime to apply relativedelta, then format back to date string
                original_datetime = datetime.datetime.strptime(value, '%Y-%m-%d')
                drifted_datetime = original_datetime + drift
                drifted_env_vars.append(f"{key}={drifted_datetime.strftime('%Y-%m-%d')}")
            except ValueError:
                print(f"Warning: Could not parse CAPSULE_DATE '{value}'. Skipping drift for this variable.")
                drifted_env_vars.append(env_var)
        elif key == 'CAPSULE_TIMESTAMP':
            try:
                original_timestamp = int(value)
                original_datetime = datetime.datetime.fromtimestamp(original_timestamp)
                drifted_datetime = original_datetime + drift
                drifted_env_vars.append(f"{key}={int(drifted_datetime.timestamp())}")
            except (ValueError, TypeError):
                print(f"Warning: Could not parse CAPSULE_TIMESTAMP '{value}'. Skipping drift for this variable.")
                drifted_env_vars.append(env_var)
        else:
            drifted_env_vars.append(env_var)
    return drifted_env_vars

def run_capsule(image, command, env_vars, drift_spec=None):
    """Constructs and executes the docker run command."""
    processed_env_vars = apply_temporal_drift(env_vars, drift_spec)

    docker_command = [
        'docker',
        'run',
        '--rm' # Automatically remove the container when it exits
    ]

    for env_var in processed_env_vars:
        docker_command.extend(['-e', env_var])

    docker_command.append(image)
    docker_command.extend(['bash', '-c', command]) # Assuming bash for command execution

    print(f"Executing Docker command: {' '.join(docker_command)}")
    try:
        result = subprocess.run(docker_command, capture_output=True, text=True, check=True)
        print("\n--- Capsule Output ---")
        print(result.stdout)
        if result.stderr:
            print("--- Capsule Errors ---")
            print(result.stderr)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Error executing capsule: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise
    except FileNotFoundError:
        print("Error: 'docker' command not found. Is Docker installed and in your PATH?")
        raise

def main():
    parser = argparse.ArgumentParser(
        description="Run a command in a Docker container with optional temporal drift on environment variables."
    )
    parser.add_argument('--image', required=True, help='The Docker image to use.')
    parser.add_argument('--command', required=True, help='The command to execute inside the container.')
    parser.add_argument('--env', action='append', default=[],
                        help='Environment variables (KEY=VALUE) to pass. Can be specified multiple times.')
    parser.add_argument('--drift', help='Temporal drift to apply (e.g., +1d, -2h, +30m).')

    args = parser.parse_args()

    run_capsule(args.image, args.command, args.env, args.drift)

if __name__ == '__main__':
    main()
