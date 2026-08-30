import docker
import os
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_docker_client():
    """Initializes and returns a Docker client."""
    try:
        client = docker.from_env()
        client.ping() # Verify connection
        return client
    except Exception as e:
        logging.error(f"Could not connect to Docker daemon: {e}")
        raise

def prune_resources(client, dry_run=False):
    """
    Prunes unused Docker resources and returns a summary of cleaned items.
    Returns a dictionary with counts of pruned items.
    """
    cleaned_counts = {
        "images": 0,
        "containers": 0,
        "volumes": 0,
        "networks": 0
    }

    if dry_run:
        logging.info("DRY RUN: No resources will be removed.")

    # Prune images
    logging.info("Fluffernutter is sniffing out unused images...")
    images_pruned = client.images.prune(filters={'dangling': False}) # Prune all unused images, not just dangling
    if images_pruned and 'ImagesDeleted' in images_pruned and images_pruned['ImagesDeleted']:
        cleaned_counts["images"] = len(images_pruned['ImagesDeleted'])
        logging.info(f"DRY RUN: Would delete {cleaned_counts['images']} images." if dry_run else f"Fluffernutter munched {cleaned_counts['images']} unused images!")
    else:
        logging.info("No unused images for Fluffernutter to nibble.")

    # Prune containers (stopped ones)
    logging.info("Fluffernutter is tidying up stopped containers...")
    containers_pruned = client.containers.prune()
    if containers_pruned and 'ContainersDeleted' in containers_pruned and containers_pruned['ContainersDeleted']:
        cleaned_counts["containers"] = len(containers_pruned['ContainersDeleted'])
        logging.info(f"DRY RUN: Would delete {cleaned_counts['containers']} containers." if dry_run else f"Fluffernutter tucked away {cleaned_counts['containers']} stopped containers!")
    else:
        logging.info("No stopped containers for Fluffernutter to nap in.")

    # Prune volumes
    logging.info("Fluffernutter is sweeping up dangling volumes...")
    volumes_pruned = client.volumes.prune()
    if volumes_pruned and 'VolumesDeleted' in volumes_pruned and volumes_pruned['VolumesDeleted']:
        cleaned_counts["volumes"] = len(volumes_pruned['VolumesDeleted'])
        logging.info(f"DRY RUN: Would delete {cleaned_counts['volumes']} volumes." if dry_run else f"Fluffernutter swallowed {cleaned_counts['volumes']} dangling volumes!")
    else:
        logging.info("No dangling volumes for Fluffernutter to roll around in.")

    # Prune networks
    logging.info("Fluffernutter is untangling unused networks...")
    networks_pruned = client.networks.prune()
    if networks_pruned and 'NetworksDeleted' in networks_pruned and networks_pruned['NetworksDeleted']:
        cleaned_counts["networks"] = len(networks_pruned['NetworksDeleted'])
        logging.info(f"DRY RUN: Would delete {cleaned_counts['networks']} networks." if dry_run else f"Fluffernutter untangled {cleaned_counts['networks']} unused networks!")
    else:
        logging.info("No unused networks for Fluffernutter to get lost in.")

    return cleaned_counts

def calculate_satisfaction(cleaned_counts):
    """Calculates Fluffernutter's satisfaction level based on cleaned items."""
    total_cleaned = sum(cleaned_counts.values())
    if total_cleaned == 0:
        return "Content (no dust, but a bit bored)"
    elif total_cleaned < 5:
        return "Mildly Pleased (a few tasty crumbs)"
    elif total_cleaned < 20:
        return "Quite Happy (a decent meal!)"
    elif total_cleaned < 50:
        return "Ecstatic! (a veritable feast of digital dust!)"
    else:
        return "Overjoyed! (a banquet beyond its wildest dreams!)"

def main():
    interval_seconds = int(os.getenv("CLEANUP_INTERVAL_SECONDS", "3600")) # Default to 1 hour
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"

    logging.info(f"Fluffernutter, the Digital Dust Bunny Sweeper, is starting up!")
    logging.info(f"Cleanup interval: {interval_seconds} seconds. Dry run: {dry_run}")

    try:
        client = get_docker_client()
    except Exception:
        logging.error("Failed to initialize Docker client. Exiting.")
        return

    while True:
        logging.info("--- Fluffernutter is beginning its sweep! ---")
        cleaned_items = prune_resources(client, dry_run=dry_run)
        satisfaction = calculate_satisfaction(cleaned_items)

        logging.info(f"--- Fluffernutter's Report ---")
        logging.info(f"Images pruned: {cleaned_items['images']}")
        logging.info(f"Containers pruned: {cleaned_items['containers']}")
        logging.info(f"Volumes pruned: {cleaned_items['volumes']}")
        logging.info(f"Networks pruned: {cleaned_items['networks']}")
        logging.info(f"Fluffernutter's current mood: {satisfaction}")
        logging.info(f"--- Sweep complete. Fluffernutter will rest for {interval_seconds} seconds. ---")

        time.sleep(interval_seconds)

if __name__ == "__main__":
    main()
