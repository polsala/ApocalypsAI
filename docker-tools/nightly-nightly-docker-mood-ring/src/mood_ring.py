import docker
import sys
import os

def get_container_stats(container):
    try:
        # Get a single stat snapshot, not a stream
        stats_generator = container.stats(stream=False)
        return next(stats_generator) if stats_generator else None
    except Exception:
        # Handle cases where stats might not be available immediately
        # or if the container is in a transient state.
        return None

def calculate_cpu_percent(stats):
    if not stats or 'cpu_stats' not in stats or 'precpu_stats' not in stats:
        return 0.0

    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    number_cpus = stats['cpu_stats']['online_cpus'] if 'online_cpus' in stats['cpu_stats'] else len(stats['cpu_stats']['cpu_usage']['percpu_usage'])

    if system_delta > 0 and cpu_delta > 0:
        return (cpu_delta / system_delta) * number_cpus * 100.0
    return 0.0

def calculate_mem_percent(stats):
    if not stats or 'memory_stats' not in stats or 'limit' not in stats['memory_stats'] or stats['memory_stats']['limit'] == 0:
        return 0.0

    usage = stats['memory_stats']['usage']
    limit = stats['memory_stats']['limit']
    return (usage / limit) * 100.0

def get_container_mood(container_name_or_id):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name_or_id)
    except docker.errors.NotFound:
        return "Vanished 👻"
    except docker.errors.APIError as e:
        return f"Error connecting to Docker: {e}"

    status = container.status

    if status == 'running':
        health_status = 'unknown'
        try:
            # Docker SDK v6.x changed how healthcheck status is accessed
            # It's now typically in container.attrs['State']['Health']['Status']
            if 'Health' in container.attrs.get('State', {}):
                health_status = container.attrs['State']['Health']['Status']
        except (KeyError, AttributeError):
            pass # No healthcheck defined or not available

        stats = get_container_stats(container)

        if health_status == 'unhealthy':
            return "Grumpy 😠"

        if not stats:
            return "Confused 🤔" # Running but no stats available

        cpu_percent = calculate_cpu_percent(stats)
        mem_percent = calculate_mem_percent(stats)

        cpu_anxious_threshold = float(os.getenv('CPU_ANXIOUS_THRESHOLD', '50'))
        mem_anxious_threshold = float(os.getenv('MEM_ANXIOUS_THRESHOLD', '50'))

        if cpu_percent >= cpu_anxious_threshold or mem_percent >= mem_anxious_threshold:
            return "Anxious 😟"
        elif cpu_percent >= 20 or mem_percent >= 20:
            return "Content 😊"
        else:
            return "Serene 😌"
    elif status == 'exited':
        # Check exit code for 'Furious'
        if container.attrs['State']['ExitCode'] != 0:
            return "Furious 😡"
        return "Asleep 😴"
    elif status == 'restarting':
        return "Furious 😡"
    elif status == 'paused':
        return "Asleep 😴" # Paused is similar to stopped for mood purposes
    else:
        return f"Asleep 😴" # Other non-running states

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python mood_ring.py <container_name_or_id>", file=sys.stderr)
        sys.exit(1)

    container_id = sys.argv[1]
    mood = get_container_mood(container_id)
    print(mood)
