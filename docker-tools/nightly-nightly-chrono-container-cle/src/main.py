import os
import argparse
import yaml
import requests
import datetime
import docker # type: ignore # Docker SDK is not always type-hinted

def find_docker_files(root_path):
    """Recursively finds Dockerfiles and docker-compose.yml files."""
    docker_files = []
    docker_compose_files = []
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename == "Dockerfile":
                docker_files.append(os.path.join(dirpath, filename))
            elif filename == "docker-compose.yml" or filename == "docker-compose.yaml":
                docker_compose_files.append(os.path.join(dirpath, filename))
    return docker_files, docker_compose_files

def extract_images_from_dockerfile(filepath):
    """Extracts image names from a Dockerfile."""
    images = set()
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line.upper().startswith("FROM"):
                    parts = line.split()
                    if len(parts) > 1:
                        image_name = parts[1]
                        # Remove any build arguments or aliases
                        if ' AS ' in image_name.upper():
                            image_name = image_name.upper().split(' AS ')[0]
                        images.add(image_name)
    except Exception as e:
        print(f"Warning: Could not read or parse Dockerfile '{filepath}': {e}")
    return list(images)

def extract_images_from_docker_compose(filepath):
    """Extracts image names from a docker-compose.yml file."""
    images = set()
    try:
        with open(filepath, 'r') as f:
            compose_config = yaml.safe_load(f)
            if compose_config and 'services' in compose_config:
                for service_name, service_config in compose_config['services'].items():
                    if isinstance(service_config, dict) and 'image' in service_config:
                        images.add(service_config['image'])
    except yaml.YAMLError as e:
        print(f"Warning: Could not parse docker-compose.yml '{filepath}': {e}")
    except Exception as e:
        print(f"Warning: Could not read docker-compose.yml '{filepath}': {e}")
    return list(images)

def get_image_age(image_name):
    """
    Attempts to get the creation/push date of a Docker image.
    Prioritizes local image info, then falls back to Docker Hub API.
    Returns a datetime object or None.
    """
    # 1. Try local Docker daemon
    try:
        client = docker.from_env()
        image = client.images.get(image_name)
        # 'Created' field is a Unix timestamp
        created_timestamp = image.attrs['Created']
        return datetime.datetime.fromtimestamp(created_timestamp, tz=datetime.timezone.utc)
    except (docker.errors.ImageNotFound, docker.errors.APIError):
        pass # Image not found locally, or Docker daemon not accessible
    except Exception as e:
        print(f"Warning: Error inspecting local image '{image_name}': {e}")

    # 2. Fallback to Docker Hub API (for public images)
    # This is a simplified approach; real-world might need authentication for rate limits
    repo, tag = (image_name.split(':', 1) + ['latest'])[:2]
    if '/' not in repo: # Assume official library image if no '/'
        repo = f"library/{repo}"

    docker_hub_url = f"https://hub.docker.com/v2/repositories/{repo}/tags/{tag}/"
    try:
        response = requests.get(docker_hub_url, timeout=5)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        if 'last_updated' in data and data['last_updated']:
            # Docker Hub returns ISO 8601 format
            return datetime.datetime.fromisoformat(data['last_updated'].replace('Z', '+00:00'))
    except requests.exceptions.RequestException as e:
        # print(f"Debug: Could not fetch Docker Hub info for '{image_name}': {e}")
        pass # Could not reach Docker Hub or image not found there
    except Exception as e:
        print(f"Warning: Error fetching Docker Hub info for '{image_name}': {e}")

    return None

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chrono-Container Cleaner: Detects 'dusty' (old) Docker images."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The root directory to scan for Dockerfiles and docker-compose files."
    )
    parser.add_argument(
        "--threshold-days",
        type=int,
        default=365,
        help="Images older than this many days will be flagged as 'dusty'. Default: 365."
    )
    args = parser.parse_args()

    root_path = args.path
    threshold_days = args.threshold_days
    threshold_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=threshold_days)

    print(f"--- Nightly Chrono-Container Cleaner Report ---")
    print(f"Scanning '{root_path}' for images older than {threshold_days} days (pre-{threshold_date.strftime('%Y-%m-%d')}).\n")

    docker_files, docker_compose_files = find_docker_files(root_path)
    all_images = set()

    for df in docker_files:
        images = extract_images_from_dockerfile(df)
        all_images.update(images)
        # print(f"Found images in {df}: {images}") # Debug

    for dcf in docker_compose_files:
        images = extract_images_from_docker_compose(dcf)
        all_images.update(images)
        # print(f"Found images in {dcf}: {images}") # Debug

    if not all_images:
        print("No Docker images found in any Dockerfile or docker-compose.yml. Your container garden is pristine (or empty)!")
        return

    dusty_images = []
    for image_name in sorted(list(all_images)):
        print(f"Inspecting image: {image_name}...")
        age_date = get_image_age(image_name)
        if age_date:
            if age_date < threshold_date:
                dusty_images.append((image_name, age_date))
                print(f"  -> Detected as DUSTY! Last updated: {age_date.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            else:
                print(f"  -> Fresh as a daisy! Last updated: {age_date.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        else:
            print(f"  -> Age unknown. Perhaps a relic from a forgotten era? (Could not determine age)")

    print("\n--- Chrono-Container Cleaner Summary ---")
    if dusty_images:
        print(f"🚨 {len(dusty_images)} DUSTY IMAGES DETECTED! Time for a 'freshening' ritual:")
        for image, age in dusty_images:
            print(f"  - '{image}' (Last updated: {age.strftime('%Y-%m-%d')})")
        print("\nSuggestions for a 'freshening' ritual:")
        print("  *   Update your Dockerfiles: Change `FROM old_image:tag` to `FROM new_image:latest` or a more recent stable tag.")
        print("  *   Rebuild your images: `docker build --no-cache .` to ensure fresh base layers.")
        print("  *   Pull newer versions: `docker pull <image_name>` for images used directly in docker-compose.")
        print("  *   Consider multi-stage builds to reduce final image size and dependency on base image updates.")
    else:
        print("✨ All detected container images are sparkling fresh! Your temporal container garden is in excellent order.")

if __name__ == "__main__":
    main()
