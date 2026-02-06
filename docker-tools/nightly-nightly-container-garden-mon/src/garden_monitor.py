import docker
import sys
import json
import time

def get_container_garden_status():
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
    except Exception as e:
        return {"error": f"Failed to connect to Docker daemon: {e}. Is Docker running?"}

    garden_report = []
    for container in containers:
        plant_status = {
            "name": container.name,
            "id": container.short_id,
            "status": container.status,
            "health": "Unknown",
            "cpu_usage_percent": "N/A",
            "memory_usage_mb": "N/A",
            "foliage_condition": "N/A"
        }

        # Determine health status
        if container.status == 'running':
            try:
                # Docker SDK doesn't directly expose health status from `container.health_status`
                # We need to inspect the container for healthcheck results
                inspect_data = client.api.inspect_container(container.id)
                health_status = inspect_data.get('State', {}).get('Health', {}).get('Status')
                if health_status:
                    plant_status["health"] = health_status
                else:
                    plant_status["health"] = "No Healthcheck"
            except Exception:
                plant_status["health"] = "Error checking health"

            # Get stats (CPU, Memory)
            try:
                # Get a single stats snapshot, not a stream
                stats_stream = container.stats(stream=False)
                if stats_stream:
                    # CPU calculation (simplified for a single snapshot)
                    cpu_delta = stats_stream['cpu_stats']['cpu_usage']['total_usage'] - \
                                stats_stream['precpu_stats']['cpu_usage']['total_usage']
                    system_cpu_delta = stats_stream['cpu_stats']['system_cpu_usage'] - \
                                       stats_stream['precpu_stats']['system_cpu_usage']
                    number_cpus = stats_stream['cpu_stats']['online_cpus'] if 'online_cpus' in stats_stream['cpu_stats'] else len(stats_stream['cpu_stats']['cpu_usage']['percpu_usage'])

                    if system_cpu_delta > 0 and number_cpus > 0:
                        cpu_percent = (cpu_delta / system_cpu_delta) * number_cpus * 100.0
                        plant_status["cpu_usage_percent"] = f"{cpu_percent:.2f}%"
                    else:
                        plant_status["cpu_usage_percent"] = "0.00%"

                    # Memory calculation
                    mem_usage = stats_stream['memory_stats']['usage']
                    mem_limit = stats_stream['memory_stats']['limit']
                    plant_status["memory_usage_mb"] = f"{mem_usage / (1024 * 1024):.2f} MB / {mem_limit / (1024 * 1024):.2f} MB"

                    # Whimsical foliage condition based on stats
                    if cpu_percent > 80 or (mem_usage / mem_limit) > 0.8:
                        plant_status["foliage_condition"] = "Thirsty Roots & Overgrown Foliage"
                    elif cpu_percent > 50 or (mem_usage / mem_limit) > 0.5:
                        plant_status["foliage_condition"] = "Vigorous Growth"
                    else:
                        plant_status["foliage_condition"] = "Lush & Green"

            except Exception as stats_e:
                plant_status["cpu_usage_percent"] = f"Stats Error: {stats_e}"
                plant_status["memory_usage_mb"] = f"Stats Error: {stats_e}"
                plant_status["foliage_condition"] = "Withered"

        # Whimsical status mapping
        if container.status == 'running' and plant_status["health"] == 'healthy':
            plant_status["garden_status"] = "Thriving Bloom"
        elif container.status == 'running' and plant_status["health"] == 'unhealthy':
            plant_status["garden_status"] = "Wilting Petal"
        elif container.status == 'running':
            plant_status["garden_status"] = "Budding Sprout (Running)"
        elif container.status == 'exited':
            plant_status["garden_status"] = "Dormant Seed (Exited)"
        elif container.status == 'paused':
            plant_status["garden_status"] = "Hibernating Bulb (Paused)"
        else:
            plant_status["garden_status"] = f"Mysterious Growth ({container.status})"

        garden_report.append(plant_status)

    return garden_report

def format_report(report_data):
    if "error" in report_data:
        return f"Garden Report Error: {report_data['error']}"

    output = ["\n--- ApocalypsAI Container Garden Report ---"]
    if not report_data:
        output.append("The garden is empty. No containers found. Perhaps plant some seeds?")
        return "\n".join(output)

    for plant in report_data:
        output.append(f"\nPlant Name: {plant['name']} (ID: {plant['id']})")
        output.append(f"  Garden Status: {plant['garden_status']}")
        output.append(f"  Current State: {plant['status'].capitalize()}")
        output.append(f"  Health Check: {plant['health'].capitalize()}")
        if plant['status'] == 'running':
            output.append(f"  Foliage Condition: {plant['foliage_condition']}")
            output.append(f"  Soil Nutrients (CPU): {plant['cpu_usage_percent']}")
            output.append(f"  Water Level (Memory): {plant['memory_usage_mb']}")
        else:
            output.append("  (Plant is not active, no live stats available)")
    output.append("\n--- End of Garden Report ---")
    return "\n".join(output)

if __name__ == "__main__":
    report = get_container_garden_status()
    print(format_report(report))
