import docker
import argparse
from datetime import datetime, timedelta, timezone

def get_stale_containers(client, threshold_hours):
    """
    Identifies stopped containers older than a given threshold.
    """
    stale_containers = []
    now = datetime.now(timezone.utc)
    for container in client.containers.list(all=True, filters={"status": "exited"}):
        # Docker's 'Created' timestamp is in seconds since epoch
        created_timestamp = container.attrs['Created']
        created_dt = datetime.fromtimestamp(created_timestamp, timezone.utc)
        if (now - created_dt) > timedelta(hours=threshold_hours):
            stale_containers.append(container)
    return stale_containers

def get_dangling_images(client):
    """
    Identifies dangling images (images not associated with any container).
    """
    dangling_images = []
    for image in client.images.list(filters={"dangling": True}):
        dangling_images.append(image)
    return dangling_images

def perform_cleanup(client, containers_to_remove, images_to_remove, dry_run):
    """
    Performs the actual removal or reports what would be removed.
    """
    if dry_run:
        print("\n--- Temporal Defragmentation Dry Run ---")
        print("The following entities would be chronologically re-aligned (removed):")
    else:
        print("\n--- Initiating Temporal Defragmentation ---")

    if containers_to_remove:
        print(f"\nContainers ({len(containers_to_remove)}):")
        for container in containers_to_remove:
            print(f"  - Container ID: {container.short_id}, Name: {container.name} (created {datetime.fromtimestamp(container.attrs['Created'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')})")
            if not dry_run:
                try:
                    container.remove()
                    print(f"    [SUCCESS] Re-aligned container {container.short_id}")
                except docker.errors.APIError as e:
                    print(f"    [ERROR] Failed to re-align container {container.short_id}: {e}")
    else:
        print("\nNo stale containers detected for temporal re-alignment.")

    if images_to_remove:
        print(f"\nImages ({len(images_to_remove)}):")
        for image in images_to_remove:
            tags = image.tags if image.tags else ["<none>"]
            print(f"  - Image ID: {image.short_id}, Tags: {', '.join(tags)}")
            if not dry_run:
                try:
                    client.images.remove(image.id)
                    print(f"    [SUCCESS] Re-aligned image {image.short_id}")
                except docker.errors.APIError as e:
                    print(f"    [ERROR] Failed to re-align image {image.short_id}: {e}")
    else:
        print("\nNo dangling images detected for temporal re-alignment.")

    if not dry_run:
        print("\n--- Temporal Defragmentation Complete ---")
    else:
        print("\n--- Temporal Defragmentation Dry Run Complete ---")
        print("Run with --force-clean to apply changes.")

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Integrator's Temporal Container Tidy: "
                    "Chronologically defragments and tidies up Docker images and containers."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the cleanup without actually removing anything."
    )
    parser.add_argument(
        "--force-clean",
        action="store_true",
        help="Execute the cleanup. WARNING: This will remove resources."
    )
    parser.add_argument(
        "--container-age-threshold",
        type=int,
        default=24,
        help="Remove stopped containers older than this many hours (default: 24)."
    )
    args = parser.parse_args()

    if not args.dry_run and not args.force_clean:
        print("Please specify either --dry-run to see what would be removed, or --force-clean to proceed with removal.")
        return

    try:
        client = docker.from_env()
        client.ping() # Test connection
    except Exception as e:
        print(f"ERROR: Could not connect to Docker daemon. Is Docker running? {e}")
        return

    print("Scanning for temporal anomalies in your Docker realm...")

    stale_containers = get_stale_containers(client, args.container_age_threshold)
    dangling_images = get_dangling_images(client)

    perform_cleanup(client, stale_containers, dangling_images, args.dry_run)

if __name__ == "__main__":
    main()
