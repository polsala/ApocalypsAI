import docker
import os
import sys
import time

def get_container_mood(container_name_or_id, client):
    """Determines the 'mood' of a Docker container."""
    try:
        container = client.containers.get(container_name_or_id)
        status = container.status
        health_status = None

        if 'Health' in container.attrs.get('State', {}):
            health_status = container.attrs['State']['Health']['Status']

        if status == 'running':
            if health_status == 'healthy':
                return "Serene 😌"
            elif health_status == 'unhealthy' or health_status == 'starting':
                return "Anxious 😨"
            else: # running but no health check or unknown health
                return "Pensive 🧠"
        elif status == 'exited':
            return "Grumpy 😠"
        elif status == 'restarting':
            return "Anxious 😨"
        else:
            return f"Mysterious 👻 (Status: {status})"
    except docker.errors.NotFound:
        return "Invisible 👻 (Not Found)"
    except docker.errors.APIError as e:
        return f"Troubled ⛈️ (API Error: {e})"
    except Exception as e:
        return f"Confused 😵 (Error: {e})"

def main():
    container_names_str = os.getenv("CONTAINER_NAMES", "")
    if not container_names_str:
        print("Error: CONTAINER_NAMES environment variable not set. Please specify container names/IDs separated by commas.")
        sys.exit(1)

    container_names = [name.strip() for name in container_names_str.split(',') if name.strip()]

    if not container_names:
        print("Error: No valid container names provided in CONTAINER_NAMES.")
        sys.exit(1)

    try:
        client = docker.from_env()
    except Exception as e:
        print(f"Error connecting to Docker daemon: {e}")
        print("Ensure the Docker daemon is running and the Docker socket is accessible (e.g., mount /var/run/docker.sock).")
        sys.exit(1)

    print(f"--- Docker Mood Ring Report ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---")
    for name in container_names:
        mood = get_container_mood(name, client)
        print(f"Container '{name}': {mood}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()
