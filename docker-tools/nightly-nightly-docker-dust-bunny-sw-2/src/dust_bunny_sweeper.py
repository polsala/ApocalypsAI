import subprocess
import sys

def run_docker_command(command):
    """Helper to run a docker command and return its stdout."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("Error: 'docker' command not found. Is Docker installed and in PATH?", file=sys.stderr)
        return []

def get_dangling_images():
    """Get a list of dangling image IDs and their sizes."""
    # Get detailed info for dangling images
    details_output = run_docker_command(['docker', 'images', '-f', 'dangling=true', '--format', '{{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedSince}}\t{{.Size}}'])
    
    images = []
    for line in details_output:
        parts = line.split('\t')
        if len(parts) == 5:
            images.append({
                'repo': parts[0],
                'tag': parts[1],
                'id': parts[2],
                'created_since': parts[3],
                'size': parts[4]
            })
    return images

def get_unused_volumes():
    """Get a list of unused volume names."""
    return run_docker_command(['docker', 'volume', 'ls', '-f', 'dangling=true', '--format', '{{.Name}}'])

def get_exited_containers():
    """Get a list of exited container names and their exit status."""
    container_info = run_docker_command(['docker', 'ps', '-a', '-f', 'status=exited', '--format', '{{.Names}}\t{{.Status}}'])
    containers = []
    for line in container_info:
        parts = line.split('\t')
        if len(parts) == 2:
            containers.append({'name': parts[0], 'status': parts[1]})
    return containers

def generate_report(dangling_images, unused_volumes, exited_containers):
    """Generates a whimsical report of Docker dust bunnies."""
    report = []
    report.append("✨ Initiating the Nightly Docker Dust Bunny Sweep! ✨\n")
    report.append("Oh dear, it seems some digital dust bunnies have accumulated in your Docker realm!\n")
    report.append("Let's see what we've found...\n")

    if not dangling_images and not unused_volumes and not exited_containers:
        report.append("\n--- 🎉 All Clear! (No Dust Bunnies Found) 🎉 ---")
        report.append("Your Docker environment is sparkling clean! Keep up the good work.\n")
        return "\n".join(report)

    report.append("\n--- 🧹 Dangling Images (Forgotten Phantoms) 🧹 ---")
    if dangling_images:
        report.append("These images are like old blueprints for projects long finished, taking up space.\n")
        for img in dangling_images:
            report.append(f"  {img['repo']:<18} {img['tag']:<18} {img['id']:<12} {img['created_since']:<18} {img['size']}")
        report.append("\nTo banish these forgotten phantoms, consider running:")
        image_ids_to_remove = ' '.join([img['id'] for img in dangling_images])
        report.append(f"  docker rmi {image_ids_to_remove}")
        report.append("  # Or, for a general sweep of all dangling images:\n  docker image prune")
    else:
        report.append("No dangling images found. Your image registry is tidy!")

    report.append("\n--- 🗑️ Unused Volumes (Lost Luggage) 🗑️ ---")
    if unused_volumes:
        report.append("Volumes that aren't attached to any container, like lost luggage at a forgotten terminal.\n")
        for vol in unused_volumes:
            report.append(f"  {vol}")
        report.append("\nTo reclaim this lost luggage, consider running:")
        volumes_to_remove = ' '.join(unused_volumes)
        report.append(f"  docker volume rm {volumes_to_remove}")
        report.append("  # Or, for a general sweep of all unused volumes:\n  docker volume prune")
    else:
        report.append("No unused volumes found. All your data has a home!")

    report.append("\n--- 👻 Exited Containers (Lingering Spirits) 👻 ---")
    if exited_containers:
        report.append("Containers that have finished their work but are still hanging around, taking up minimal space but adding to the clutter.\n")
        for container in exited_containers:
            report.append(f"  {container['name']} ({container['status']})")
        report.append("\nTo bid farewell to these lingering spirits, consider running:")
        container_names_to_remove = ' '.join([c['name'] for c in exited_containers])
        report.append(f"  docker rm {container_names_to_remove}")
        report.append("  # Or, for a general sweep of all exited containers:\n  docker container prune")
    else:
        report.append("No exited containers found. All your processes are either running or gracefully departed!")

    if dangling_images or unused_volumes or exited_containers:
        report.append("\n--- ✨ Grand Cleanup Suggestion ✨ ---")
        report.append("For a comprehensive sweep of all dangling images, unused volumes, and exited containers, you can use the mighty:\n")
        report.append("  docker system prune\n")
        report.append("Remember to review the items before pruning! Happy sweeping!")

    return "\n".join(report)

if __name__ == '__main__':
    dangling_images = get_dangling_images()
    unused_volumes = get_unused_volumes()
    exited_containers = get_exited_containers()
    print(generate_report(dangling_images, unused_volumes, exited_containers))
