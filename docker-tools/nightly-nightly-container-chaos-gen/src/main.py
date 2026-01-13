import random
import subprocess
import time
import yaml
import os
import sys
import argparse

from docker import DockerClient
from docker.errors import APIError

# Mock rationale: Using a mock Docker client for deterministic testing without requiring a running Docker daemon.
# In a real scenario, this would be a live DockerClient instance.
class MockDockerClient:
    def __init__(self):
        self.containers = MockContainerManager()
        self.networks = MockNetworkManager()

    def containers(self):
        return self.containers

    def networks(self):
        return self.networks

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class MockContainerManager:
    def run(self, image, detach=True, network=None, command=None, volumes=None, name=None, **kwargs):
        print(f"Mock: Running container {name} from image {image} on network {network} with command {command}")
        return MockContainer(name, image, network)

    def list(self, filters=None):
        print(f"Mock: Listing containers with filters {filters}")
        return []

class MockContainer:
    def __init__(self, name, image, network):
        self.name = name
        self.image = image
        self.network = network
        self.id = f"mock_id_{name}"

    def stop(self):
        print(f"Mock: Stopping container {self.name}")

    def remove(self, force=True):
        print(f"Mock: Removing container {self.name}")

class MockNetworkManager:
    def create(self, name):
        print(f"Mock: Creating network {name}")
        return MockNetwork(name)

    def get(self, name):
        print(f"Mock: Getting network {name}")
        return MockNetwork(name)

class MockNetwork:
    def __init__(self, name):
        self.name = name
        self.id = f"mock_net_id_{name}"

    def remove(self):
        print(f"Mock: Removing network {self.name}")


SERVICE_TEMPLATES = {
    "web": {
        "image": "nginx:latest",
        "ports": ["80:80"],
        "depends_on": [],
        "command": "nginx -g 'daemon off;'",
        "environment": {},
        "volumes": []
    },
    "db": {
        "image": "postgres:13",
        "ports": ["5432:5432"],
        "depends_on": [],
        "environment": {
            "POSTGRES_USER": "user",
            "POSTGRES_PASSWORD": "password",
            "POSTGRES_DB": "database"
        },
        "volumes": ["db_data:/var/lib/postgresql/data"]
    },
    "redis": {
        "image": "redis:alpine",
        "ports": ["6379:6379"],
        "depends_on": [],
        "command": "redis-server --appendonly yes",
        "environment": {},
        "volumes": ["redis_data:/data"]
    },
    "worker": {
        "image": "python:3.9-slim",
        "depends_on": [],
        "command": "sleep infinity",
        "environment": {},
        "volumes": []
    }
}

CHAOS_LEVELS = {
    "low": {
        "network_delay_ms": (50, 200),
        "service_restart_chance": 0.1,
        "resource_limit_chance": 0.05
    },
    "medium": {
        "network_delay_ms": (200, 1000),
        "service_restart_chance": 0.2,
        "resource_limit_chance": 0.1
    },
    "high": {
        "network_delay_ms": (1000, 5000),
        "service_restart_chance": 0.4,
        "resource_limit_chance": 0.2
    }
}

def generate_random_compose_file(num_services=5):
    """Generates a random docker-compose.yml content."""
    services = {}
    service_names = []
    available_service_types = list(SERVICE_TEMPLATES.keys())

    for i in range(num_services):
        service_type = random.choice(available_service_types)
        service_config = SERVICE_TEMPLATES[service_type].copy()
        service_name = f"{service_type}-{i+1}"
        service_names.append(service_name)
        services[service_name] = service_config

    # Add dependencies randomly
    for name, config in services.items():
        if random.random() < 0.5 and len(service_names) > 1:
            dependency = random.choice([s for s in service_names if s != name])
            if dependency not in config["depends_on"]:
                config["depends_on"].append(dependency)

    # Add volumes
    volumes = {}
    for service_name, config in services.items():
        if "volumes" in config:
            for vol_mapping in config["volumes"]:
                vol_name = vol_mapping.split(":")[0]
                if vol_name not in volumes:
                    volumes[vol_name] = None # Docker Compose syntax for named volumes

    compose_content = {
        "version": "3.8",
        "services": services,
        "volumes": volumes
    }
    return yaml.dump(compose_content)

def apply_chaos(docker_client, compose_file_content, chaos_level="medium"):
    """Applies random chaos to the running containers."""
    chaos_params = CHAOS_LEVELS.get(chaos_level, CHAOS_LEVELS["medium"])
    network_name = f"chaos_net_{int(time.time())}"
    created_network = None

    try:
        # Create a dedicated network for this chaos run
        created_network = docker_client.networks.create(network_name)
        print(f"Created network: {network_name}")

        # Parse compose file to get service names
        compose_data = yaml.safe_load(compose_file_content)
        service_names = list(compose_data.get("services", {}).keys())

        # Apply network delay
        if chaos_params["network_delay_ms"]:
            delay_ms = random.randint(*chaos_params["network_delay_ms"])
            print(f"Applying network delay of {delay_ms}ms to services...")
            for service_name in service_names:
                # This is a simplified representation. Real implementation would involve execing into containers.
                # For this example, we'll just print the intent.
                print(f"  - Simulating delay for {service_name}")
                # In a real scenario, you'd use `docker exec {service_name} tc qdisc add dev eth0 root netem delay {delay_ms}ms"

        # Apply service restarts
        if chaos_params["service_restart_chance"] > 0:
            print(f"Applying random service restarts (chance: {chaos_params['service_restart_chance']:.1f})...")
            for service_name in service_names:
                if random.random() < chaos_params["service_restart_chance"]:
                    print(f"  - Restarting {service_name}")
                    # In a real scenario, you'd find the container and stop/start it.
                    # For mock, we just print.
                    pass

        # Apply resource limits (simplified)
        if chaos_params["resource_limit_chance"] > 0:
            print(f"Applying random resource limits (chance: {chaos_params['resource_limit_chance']:.1f})...")
            for service_name in service_names:
                if random.random() < chaos_params["resource_limit_chance"]:
                    print(f"  - Limiting resources for {service_name}")
                    # In a real scenario, you'd pass --cpus, --memory etc. to docker run or update existing container config.
                    pass

        # Simulate a brief period of chaos
        chaos_duration = random.randint(5, 15)
        print(f"Simulating chaos for {chaos_duration} seconds...")
        time.sleep(chaos_duration)

    except APIError as e:
        print(f"Docker API error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during chaos application: {e}", file=sys.stderr)
    finally:
        # Cleanup
        if created_network:
            print(f"Cleaning up network: {network_name}")
            try:
                created_network.remove()
            except APIError as e:
                print(f"Error removing network {network_name}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Generate and run chaotic Docker Compose configurations.")
    parser.add_argument("--num-services", type=int, default=random.randint(3, 7), help="Number of services to generate.")
    parser.add_argument("--chaos-level", type=str, default="medium", choices=CHAOS_LEVELS.keys(), help="Level of chaos to introduce.")
    args = parser.parse_args()

    compose_content = generate_random_compose_file(args.num_services)
    print("-- Generated Docker Compose File --")
    print(compose_content)
    print("-----------------------------------")

    # Use MockDockerClient for testing, real DockerClient otherwise
    if os.environ.get("USE_MOCK_DOCKER") == "true":
        docker_client = MockDockerClient()
        print("Using Mock Docker Client.")
    else:
        try:
            docker_client = DockerClient(base_url='unix://var/run/docker.sock')
            # Test connection
            docker_client.ping()
            print("Using real Docker Client.")
        except APIError as e:
            print(f"Error connecting to Docker daemon: {e}", file=sys.stderr)
            print("Please ensure Docker is running and accessible.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred connecting to Docker: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        # This part is tricky to mock fully without a full Docker Compose implementation.
        # For this example, we'll simulate the process.
        print("Starting simulated Docker Compose up...")
        # In a real scenario, you'd use `docker compose up -d` or the SDK to create services.
        # For simplicity, we'll just pass the content to apply_chaos which simulates the effects.
        apply_chaos(docker_client, compose_content, args.chaos_level)

        print("Chaos simulation complete.")

    except Exception as e:
        print(f"An error occurred during chaos simulation: {e}", file=sys.stderr)
    finally:
        # Cleanup is handled within apply_chaos for the network.
        # For a full docker-compose up, you'd need `docker compose down`.
        print("Cleanup of generated resources initiated.")

if __name__ == "__main__":
    main()
