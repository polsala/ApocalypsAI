import docker
import sys
import time

def get_container_metrics(container):
    """
    Fetches CPU and memory usage for a given container.
    Returns (cpu_percent, mem_percent) or (0, 0) if stats are unavailable.
    """
    try:
        stats = container.stats(stream=False)
        if not stats:
            return 0.0, 0.0

        # CPU calculation
        cpu_percent = 0.0
        if 'cpu_stats' in stats and 'system_cpu_usage' in stats['cpu_stats'] and \
           'online_cpus' in stats['cpu_stats'] and 'total_usage' in stats['cpu_stats']['cpu_usage'] and \
           'precpu_stats' in stats and 'system_cpu_usage' in stats['precpu_stats'] and \
           'total_usage' in stats['precpu_stats']['cpu_usage']:
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
            if system_delta > 0 and stats['cpu_stats']['online_cpus'] > 0:
                cpu_percent = (cpu_delta / system_delta) * stats['cpu_stats']['online_cpus'] * 100.0

        # Memory calculation
        mem_percent = 0.0
        if 'memory_stats' in stats and 'usage' in stats['memory_stats'] and 'limit' in stats['memory_stats']:
            mem_usage = stats['memory_stats']['usage']
            mem_limit = stats['memory_stats']['limit']
            if mem_limit > 0:
                mem_percent = (mem_usage / mem_limit) * 100.0

        return cpu_percent, mem_percent
    except Exception as e:
        print(f"Warning: Could not get stats for container {container.name}: {e}", file=sys.stderr)
        return 0.0, 0.0

def assign_mood(cpu_percent, mem_percent, status):
    """
    Assigns a whimsical mood based on container metrics and status.
    """
    if status not in ['running', 'restarting']:
        return "Lost in the Void 👻"
    if cpu_percent > 85 or mem_percent > 85:
        return "Overwhelmed 🥵"
    if cpu_percent > 50 or mem_percent > 50:
        return "Anxious 😬"
    if cpu_percent < 5 and mem_percent < 5:
        return "Snoozing 😴"
    if cpu_percent > 10 or mem_percent > 10:
        return "Busy Bee 🐝"
    return "Zen 🙏"

def main():
    try:
        client = docker.from_env()
        print("--- Docker Container Mood Ring ---")
        print(f"Scan Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        containers = client.containers.list(all=True) # Get all containers to check status properly

        if not containers:
            print("No Docker containers found. The universe is eerily calm.")
            return

        print(f"{'Container Name':<30} {'ID (short)':<15} {'Status':<15} {'CPU %':<10} {'Mem %':<10} {'Mood':<20}")
        print(f"{'-'*30:<30} {'-'*15:<15} {'-'*15:<15} {'-'*10:<10} {'-'*10:<10} {'-'*20:<20}")

        for container in containers:
            cpu, mem = get_container_metrics(container)
            mood = assign_mood(cpu, mem, container.status)
            print(f"{container.name:<30} {container.short_id:<15} {container.status:<15} {cpu: <9.2f}% {mem: <9.2f}% {mood:<20}")

    except docker.errors.DockerException as e:
        print(f"Error connecting to Docker daemon: {e}", file=sys.stderr)
        print("Please ensure Docker is running and the Docker socket is accessible (e.g., mount /var/run/docker.sock).", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
