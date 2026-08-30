import docker
import os
import re

def scan_containers_for_secrets():
    """
    Scans all running Docker containers for environment variables
    that might contain secrets.
    """
    print("Excavation Initiated: Searching for digital artifacts in running containers...\n")

    try:
        client = docker.from_env()
    except Exception as e:
        print(f"Error connecting to Docker daemon: {e}")
        print("Please ensure Docker is running and the Docker socket is accessible (e.g., by mounting /var/run/docker.sock).")
        return

    secret_patterns = [
        re.compile(r".*API_KEY.*", re.IGNORECASE),
        re.compile(r".*SECRET.*", re.IGNORECASE),
        re.compile(r".*PASSWORD.*", re.IGNORECASE),
        re.compile(r".*TOKEN.*", re.IGNORECASE),
        re.compile(r".*CREDENTIAL.*", re.IGNORECASE),
        re.compile(r".*AUTH.*", re.IGNORECASE),
    ]

    found_artifacts_count = 0

    for container in client.containers.list():
        container_id = container.short_id
        container_name = container.name
        image_name = container.image.tags[0] if container.image.tags else "unknown"

        env_vars = container.attrs.get('Config', {}).get('Env', [])
        
        for env_var in env_vars:
            var_name, _ = (env_var.split('=', 1) + [''])[:2] # Split once, handle no value
            for pattern in secret_patterns:
                if pattern.search(var_name):
                    print("--- Artifact Found! ---")
                    print(f"Container ID:   {container_id}")
                    print(f"Container Name: {container_name}")
                    print(f"Image:          {image_name}")
                    print(f"Artifact:       {var_name} (Potential secret)\n")
                    found_artifacts_count += 1
                    break # Found a pattern for this var, move to next env_var

    print(f"Excavation Complete: {found_artifacts_count} digital artifacts unearthed.")

if __name__ == "__main__":
    scan_containers_for_secrets()
