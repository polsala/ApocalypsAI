import os
import sys
import random
import subprocess
import yaml

WHIMSICAL_NAMES = [
    "wasteland-workbench", "bunker-builder", "scavenger-station", "radiation-ranch",
    "dusty-digs", "fortress-forge", "nomad-nest", "survival-shelter",
    "apocalypse-arcade", "ruin-refinery", "ghost-grotto", "iron-haven",
    "mutant-mansion", "outpost-omega", "phantom-post", "quarantine-quarters",
    "relic-residence", "shattered-shack", "tombstone-tavern", "underground-unit"
]

def get_random_name():
    return random.choice(WHIMSICAL_NAMES)

def run_command(command, check=True):
    print(f"Executing: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}", file=sys.stderr)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        if check:
            sys.exit(1)
        return None

def start_environment(compose_file):
    if not os.path.exists(compose_file):
        print(f"Error: Compose file '{compose_file}' not found.", file=sys.stderr)
        sys.exit(1)

    env_name = get_random_name()
    print(f"Starting environment '{env_name}' using '{compose_file}'...")

    # Check if a project with this name already exists and is running
    try:
        running_projects = run_command(['docker-compose', '-f', compose_file, 'ps', '-q'], check=False)
        if running_projects:
            print(f"Environment '{env_name}' might already be running or a previous instance failed to clean up.", file=sys.stderr)
            # Attempt to stop it first if it seems to exist
            stop_environment_by_file(compose_file)
    except Exception as e:
        print(f"Could not check existing projects: {e}", file=sys.stderr)

    # Use a unique project name to avoid conflicts if multiple instances are run from the same dir
    # This is a simplified approach; a more robust solution might involve unique IDs.
    project_name_arg = f"-p {env_name}"
    command = ["docker-compose", "-f", compose_file, project_name_arg, "up", "-d"]
    run_command(command)
    print(f"Environment '{env_name}' started successfully.")

def list_environments():
    print("Listing running Docker Compose environments...")
    # This is a heuristic. It lists all containers that are part of a docker-compose project.
    # A more robust solution would involve tracking project names explicitly.
    command = ["docker", "ps", "--format", "{{.Names}}"]
    container_names = run_command(command, check=False)
    if not container_names:
        print("No Docker Compose environments found running.")
        return

    # Try to infer project names from container names
    # Docker Compose typically prefixes container names with the project name and a hyphen.
    project_names = set()
    for name in container_names.split('\n'):
        if '-' in name:
            project_name = name.split('-')[0]
            project_names.add(project_name)

    if not project_names:
        print("Could not infer project names. Displaying raw container names:")
        print(container_names)
    else:
        print("Running environments (inferred project names):")
        for p_name in sorted(list(project_names)):
            print(f"- {p_name}")

def stop_environment_by_file(compose_file):
    print(f"Stopping environment defined in '{compose_file}'...")
    command = ["docker-compose", "-f", compose_file, "down"]
    run_command(command, check=False) # Don't fail if it's not running

def stop_environment_by_name(env_name):
    print(f"Stopping environment named '{env_name}'...")
    # This is tricky. We need to find the compose file associated with this env_name.
    # For simplicity, we'll assume the env_name is the project name and try to find a compose file
    # in the current directory that might correspond to it.
    # A more robust solution would store mappings or use docker labels.
    
    # Heuristic: look for a compose file and try to stop it with the given project name.
    # This is not foolproof and might stop the wrong environment if multiple compose files exist.
    compose_files = [f for f in os.listdir('.') if f.endswith('.yml') or f.endswith('.yaml')]
    found_compose_file = None
    for cf in compose_files:
        try:
            with open(cf, 'r') as f:
                data = yaml.safe_load(f)
                if 'services' in data:
                    # This is a very weak check, but better than nothing.
                    # A real check would involve inspecting docker labels or container names.
                    # For this whimsical tool, we'll proceed with a best effort.
                    found_compose_file = cf
                    break
        except Exception:
            pass

    if found_compose_file:
        command = ["docker-compose", "-f", found_compose_file, f"-p {env_name}", "down"]
        run_command(command, check=False)
        print(f"Attempted to stop environment '{env_name}'. Check 'docker ps' for status.")
    else:
        print(f"Could not find a suitable compose file to stop environment '{env_name}'.", file=sys.stderr)

def stop_all_environments():
    print("Stopping all running Docker Compose environments...")
    # This is a broad stroke. It stops all containers managed by docker-compose.
    # It might be too aggressive if you have multiple unrelated compose projects running.
    # A more targeted approach would iterate through known project names.
    command = ["docker-compose", "down"]
    run_command(command, check=False)
    print("Attempted to stop all environments.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <start|list|stop|stop-all> [compose_file] [env_name]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) != 3:
            print("Usage: python main.py start <compose_file>")
            sys.exit(1)
        compose_file = sys.argv[2]
        start_environment(compose_file)
    elif command == "list":
        list_environments()
    elif command == "stop":
        if len(sys.argv) != 3:
            print("Usage: python main.py stop <env_name>")
            sys.exit(1)
        env_name = sys.argv[2]
        stop_environment_by_name(env_name)
    elif command == "stop-all":
        stop_all_environments()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
