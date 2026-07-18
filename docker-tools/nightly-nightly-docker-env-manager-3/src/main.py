import docker
import sys
import os

CLIENT = docker.from_env()

def start_environment(env_name, dockerfile_path):
    """Starts a new Docker environment from a Dockerfile."""
    if not os.path.isdir(dockerfile_path):
        print(f"Error: Dockerfile path '{dockerfile_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    try:
        # Build the image
        image, build_logs = CLIENT.images.build(path=dockerfile_path, tag=env_name, rm=True)
        print(f"Image '{env_name}' built successfully.")

        # Create and start the container
        container = CLIENT.containers.run(image.tags[0], detach=True, name=env_name, volumes={'/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}})
        print(f"Environment '{env_name}' started with container ID: {container.id[:12]}")
    except docker.errors.BuildError as e:
        print(f"Error building Docker image for '{env_name}': {e}", file=sys.stderr)
        sys.exit(1)
    except docker.errors.APIError as e:
        print(f"Error starting container for '{env_name}': {e}", file=sys.stderr)
        sys.exit(1)

def stop_environment(env_name):
    """Stops and removes a Docker environment."""
    try:
        container = CLIENT.containers.get(env_name)
        container.stop()
        container.remove()
        print(f"Environment '{env_name}' stopped and removed.")
    except docker.errors.NotFound:
        print(f"Error: Environment '{env_name}' not found.", file=sys.stderr)
        sys.exit(1)
    except docker.errors.APIError as e:
        print(f"Error stopping/removing container for '{env_name}': {e}", file=sys.stderr)
        sys.exit(1)

def list_environments():
    """Lists all running managed environments."""
    try:
        containers = CLIENT.containers.list(filters={'label': 'apoc-env-manager=true'})
        if not containers:
            print("No managed environments running.")
            return
        print("Running managed environments:")
        for container in containers:
            print(f"- {container.name} (ID: {container.id[:12]})")
    except docker.errors.APIError as e:
        print(f"Error listing containers: {e}", file=sys.stderr)
        sys.exit(1)

def show_logs(env_name):
    """Shows logs for a specific environment."""
    try:
        container = CLIENT.containers.get(env_name)
        logs = container.logs().decode('utf-8')
        print(f"Logs for '{env_name}':\n{logs}")
    except docker.errors.NotFound:
        print(f"Error: Environment '{env_name}' not found.", file=sys.stderr)
        sys.exit(1)
    except docker.errors.APIError as e:
        print(f"Error fetching logs for '{env_name}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apoc-env-manager <command>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "up":
        if len(sys.argv) != 4:
            print("Usage: up <env_name> <dockerfile_path>", file=sys.stderr)
            sys.exit(1)
        env_name = sys.argv[2]
        dockerfile_path = sys.argv[3]
        # Add a label to easily identify managed containers
        os.environ['APOC_ENV_MANAGER_LABEL'] = 'true'
        start_environment(env_name, dockerfile_path)
    elif command == "down":
        if len(sys.argv) != 3:
            print("Usage: down <env_name>", file=sys.stderr)
            sys.exit(1)
        env_name = sys.argv[2]
        stop_environment(env_name)
    elif command == "list":
        list_environments()
    elif command == "logs":
        if len(sys.argv) != 3:
            print("Usage: logs <env_name>", file=sys.stderr)
            sys.exit(1)
        env_name = sys.argv[2]
        show_logs(env_name)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
