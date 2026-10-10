import docker
import sys

def get_container_garden_data(client):
    """
    Retrieves container data and maps it to garden plant states.
    # Mock rationale: This function interacts with the Docker daemon.
    # In tests, a mock client will be passed to simulate Docker API responses.
    """
    plants = []
    try:
        containers = client.containers.list(all=True)
        for container in containers:
            plant_type = "🌿"  # Vigorous Vine (default running)
            status_detail = container.status

            # Check health status if available
            health_status = None
            if hasattr(container, 'health') and container.health:
                health_status = container.health.get('Status')
                if health_status == 'healthy':
                    plant_type = "🌱" # Thriving Sprout
                elif health_status == 'unhealthy':
                    plant_type = "🥀" # Wilting Blossom
                elif health_status == 'starting':
                    plant_type = "🐛" # Pest Infestation (starting/problematic)

            if container.status == 'exited':
                plant_type = "💀"  # Withered Root
            elif container.status == 'restarting':
                plant_type = "🐛"  # Pest Infestation

            plants.append({
                "name": container.name,
                "status": status_detail,
                "health": health_status if health_status else "N/A",
                "plant_type": plant_type
            })
    except docker.errors.APIError as e:
        print(f"Error connecting to Docker daemon: {e}", file=sys.stderr)
        print("Please ensure the Docker daemon is running and accessible.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    return plants

def render_garden(plants):
    """
    Renders the ASCII art garden based on plant data.
    """
    if not plants:
        return "Your container garden is currently empty. Time to plant some services!\n"

    garden_rows = []
    # Header
    garden_rows.append("=" * 60)
    garden_rows.append("🌱 Nightly Container Garden Monitor 🌿")
    garden_rows.append("=" * 60)
    garden_rows.append(f"{'Plant':<8} {'Container Name':<30} {'Status':<12} {'Health':<8}")
    garden_rows.append("-" * 60)

    for plant in plants:
        garden_rows.append(
            f"{plant['plant_type']:<8} {plant['name']:<30} {plant['status']:<12} {plant['health']:<8}"
        )

    garden_rows.append("-" * 60)
    garden_rows.append("\nGarden Legend:")
    garden_rows.append("  🌱 Thriving Sprout: Running & Healthy")
    garden_rows.append("  🌿 Vigorous Vine: Running (no health check or healthy)")
    garden_rows.append("  🥀 Wilting Blossom: Running but Unhealthy")
    garden_rows.append("  💀 Withered Root: Exited or Dead")
    garden_rows.append("  🐛 Pest Infestation: Restarting or Problematic")
    garden_rows.append("\n")

    return "\n".join(garden_rows)

def main():
    """
    Main function to initialize Docker client, get data, and render.
    """
    try:
        client = docker.from_env()
    except docker.errors.DockerException as e:
        print(f"Could not connect to Docker daemon: {e}", file=sys.stderr)
        print("Ensure Docker is running and accessible (e.g., via /var/run/docker.sock).", file=sys.stderr)
        sys.exit(1)

    plants_data = get_container_garden_data(client)
    print(render_garden(plants_data))

if __name__ == "__main__":
    main()
