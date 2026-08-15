import docker
import time
import os

def get_container_mood(container):
    """Determines a whimsical mood based on container status."""
    status = container.status
    health_status = None
    if 'Health' in container.attrs.get('State', {}):
        health_status = container.attrs['State']['Health']['Status']

    if status == 'running':
        if health_status == 'healthy':
            return "Joyful"
        elif health_status == 'unhealthy':
            return "Grumpy"
        else: # running but no healthcheck or unknown health
            return "Content"
    elif status == 'exited':
        return "Sleepy"
    elif status == 'restarting':
        return "Anxious"
    elif status == 'paused':
        return "Pensive"
    elif status == 'dead':
        return "At Peace (Exited Permanently)"
    else:
        return "Mysterious"

def monitor_containers(interval=5, target_names=None):
    """Monitors Docker containers and prints their moods."""
    try:
        client = docker.from_env()
    except Exception as e:
        print(f"Error connecting to Docker daemon: {e}")
        print("Ensure Docker is running and /var/run/docker.sock is mounted.")
        return

    print("ApocalypsAI Docker Mood Ring activated!")
    print(f"Monitoring containers every {interval} seconds. Press Ctrl+C to stop.")

    while True:
        try:
            containers = client.containers.list(all=True)
            for container in containers:
                if target_names and container.name not in target_names:
                    continue
                mood = get_container_mood(container)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Container '{container.name}' (ID: {container.short_id}): {mood}")
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nDocker Mood Ring deactivated. Farewell!")
            break
        except Exception as e:
            print(f"An error occurred during monitoring: {e}")
            time.sleep(interval) # Wait before retrying

if __name__ == "__main__":
    # Allow specifying target container names via environment variable
    target_containers_str = os.getenv("DOCKER_MOOD_RING_TARGETS")
    target_container_names = [name.strip() for name in target_containers_str.split(',')] if target_containers_str else None

    # Allow specifying interval via environment variable
    monitor_interval = int(os.getenv("DOCKER_MOOD_RING_INTERVAL", 5))

    monitor_containers(interval=monitor_interval, target_names=target_container_names)
