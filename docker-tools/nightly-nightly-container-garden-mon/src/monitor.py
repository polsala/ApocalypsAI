import docker
import sys
import json
import time

def get_container_stats(container):
    """Fetches stats for a single container."""
    try:
        # stream=False gets a single snapshot of stats
        stats = container.stats(stream=False)
        return stats
    except docker.errors.APIError as e:
        sys.stderr.write(f"Error fetching stats for {container.name}: {e}\n")
        return None

def analyze_plant_health(container_name, stats):
    """Analyzes container stats and returns whimsical plant health metrics."""
    if not stats:
        return {
            "name": container_name,
            "status": "Wilted (No Data)",
            "emoji": "🥀",
            "sunlight": "N/A",
            "water": "N/A",
            "soil_nutrients": "N/A",
            "pollination": "N/A"
        }

    # Extract relevant metrics
    cpu_usage = 0
    if 'cpu_stats' in stats and 'system_cpu_usage' in stats['cpu_stats'] and 'online_cpus' in stats['cpu_stats']:
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
        system_cpu_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
        if system_cpu_delta > 0:
            cpu_usage = (cpu_delta / system_cpu_delta) * stats['cpu_stats']['online_cpus'] * 100

    mem_usage = 0
    mem_limit = 0
    if 'memory_stats' in stats:
        mem_usage = stats['memory_stats'].get('usage', 0)
        mem_limit = stats['memory_stats'].get('limit', 0)
    mem_percent = (mem_usage / mem_limit) * 100 if mem_limit > 0 else 0

    net_rx = 0
    net_tx = 0
    if 'networks' in stats:
        for net_name, net_stats in stats['networks'].items():
            net_rx += net_stats.get('rx_bytes', 0)
            net_tx += net_stats.get('tx_bytes', 0)

    block_read = 0
    block_write = 0
    if 'blkio_stats' in stats and 'io_service_bytes_recursive' in stats['blkio_stats']:
        for entry in stats['blkio_stats']['io_service_bytes_recursive']:
            if entry['op'] == 'Read':
                block_read += entry['value']
            elif entry['op'] == 'Write':
                block_write += entry['value']

    # Whimsical interpretation
    status = "Thriving"
    emoji = "🌱"

    if cpu_usage > 80:
        status = "Sun-scorched"
        emoji = "☀️"
    elif cpu_usage > 50:
        status = "Basking"
        emoji = "🌞"

    if mem_percent > 90:
        status = "Parched"
        emoji = "💧"
    elif mem_percent > 70:
        status = "Thirsty"
        emoji = "💦"

    if block_read + block_write > 100 * 1024 * 1024: # > 100MB I/O
        status = "Soil-churning"
        emoji = "🪱"
    elif block_read + block_write > 50 * 1024 * 1024: # > 50MB I/O
        status = "Root-deep"
        emoji = "🌿"

    if net_rx + net_tx > 10 * 1024 * 1024: # > 10MB network
        status = "Buzzing with Pollinators"
        emoji = "🐝"

    return {
        "name": container_name,
        "status": status,
        "emoji": emoji,
        "sunlight": f"{cpu_usage:.2f}% CPU",
        "water": f"{mem_percent:.2f}% MEM ({mem_usage / (1024*1024):.2f}MB)",
        "soil_nutrients": f"R:{block_read / (1024*1024):.2f}MB W:{block_write / (1024*1024):.2f}MB",
        "pollination": f"RX:{net_rx / (1024*1024):.2f}MB TX:{net_tx / (1024*1024):.2f}MB"
    }

def main():
    try:
        client = docker.from_env()
        running_containers = client.containers.list()

        if not running_containers:
            sys.stdout.write("The container garden is empty. No plants to monitor! 🌻\n")
            return

        sys.stdout.write("--- ApocalypsAI Container Garden Report ---\n")
        sys.stdout.write(f"Report generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for container in running_containers:
            stats = get_container_stats(container)
            health_report = analyze_plant_health(container.name, stats)
            sys.stdout.write(f"{health_report['emoji']} {health_report['name']} ({health_report['status']})\n")
            sys.stdout.write(f"  Sunlight: {health_report['sunlight']}\n")
            sys.stdout.write(f"  Water: {health_report['water']}\n")
            sys.stdout.write(f"  Soil Nutrients: {health_report['soil_nutrients']}\n")
            sys.stdout.write(f"  Pollination: {health_report['pollination']}\n\n")

        sys.stdout.write("-------------------------------------------\n")

    except docker.errors.DockerException as e:
        sys.stderr.write(f"Error connecting to Docker daemon: {e}\n")
        sys.stderr.write("Please ensure Docker is running and the Docker socket is accessible.\n")
        sys.stderr.write("You might need to run with '-v /var/run/docker.sock:/var/run/docker.sock'\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
