import docker
import sys

def get_container_aura(container):
    """Assigns a whimsical aura based on container status and health."""
    status = container.status
    health_status = None
    if hasattr(container, 'health') and container.health:
        health_status = container.health.status

    if status == 'running':
        if health_status == 'healthy':
            return "Vibrant"
        elif health_status == 'unhealthy':
            return "Anxious"
        elif health_status == 'starting':
            return "Pondering"
        else: # running but no healthcheck or unknown health
            return "Mysterious"
    elif status == 'exited':
        # Check exit code if possible, though `container.status` usually implies this
        # For simplicity, we'll assume 'exited' implies a graceful exit unless health was bad
        if container.attrs.get('State', {}).get('ExitCode') == 0:
            return "Serene"
        else:
            return "Grumpy"
    elif status == 'created' or status == 'restarting':
        return "Pondering"
    elif status == 'dead':
        return "Grumpy"
    else:
        return "Mysterious"

def main():
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True) # Get all containers, not just running ones

        if not containers:
            print("No Docker containers found.", file=sys.stderr)
            return

        for container in containers:
            aura = get_container_aura(container)
            print(f"Container '{container.name}' is {aura}.")

    except docker.errors.DockerException as e:
        print(f"Error connecting to Docker daemon: {e}", file=sys.stderr)
        print("Please ensure Docker is running and you have permission to access /var/run/docker.sock.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
