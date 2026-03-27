import subprocess
import json
import argparse
import sys

def run_docker_command(command, check=True, capture_output=True):
    """Runs a docker command and returns its stdout."""
    try:
        result = subprocess.run(
            command,
            check=check,
            capture_output=capture_output,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'docker' command not found. Is Docker installed and in your PATH?", file=sys.stderr)
        sys.exit(1)

def get_dangling_images():
    """Returns a list of dangling image IDs."""
    output = run_docker_command(["docker", "images", "-f", "dangling=true", "-q"])
    return output.splitlines() if output else []

def get_exited_containers():
    """Returns a list of exited container IDs."""
    output = run_docker_command(["docker", "ps", "-a", "-f", "status=exited", "-q"])
    return output.splitlines() if output else []

def get_unused_volumes():
    """Returns a list of unused volume names."""
    output = run_docker_command(["docker", "volume", "ls", "-f", "dangling=true", "-q"])
    return output.splitlines() if output else []

def get_system_df():
    """Returns a dictionary of Docker system disk usage."""
    output = run_docker_command(["docker", "system", "df", "--format", "{{json .}}"])
    lines = output.splitlines()
    df_data = {}
    for line in lines:
        try:
            data = json.loads(line)
            df_data[data['Type']] = data
        except json.JSONDecodeError:
            # Handle cases where a line might not be valid JSON
            pass
    return df_data

def generate_report(dangling_images, exited_containers, unused_volumes, system_df):
    """Generates a whimsical garden report."""
    report = []
    report.append("🌿 Your Container Garden Report 🌿\n")
    report.append("-----------------------------------\n")

    if dangling_images:
        report.append(f"🌱 Dangling Images ({len(dangling_images)} found):")
        report.append("   These are like forgotten seedlings, taking up space but not growing into anything useful.")
        for img_id in dangling_images:
            report.append(f"   - Image ID: {img_id}")
        report.append("\n")

    if exited_containers:
        report.append(f"🥀 Exited Containers ({len(exited_containers)} found):")
        report.append("   These are withered blooms, their season passed. They can be composted.")
        for container_id in exited_containers:
            report.append(f"   - Container ID: {container_id}")
        report.append("\n")

    if unused_volumes:
        report.append(f"🏺 Unused Volumes ({len(unused_volumes)} found):")
        report.append("   These are empty pots, ready to be reclaimed.")
        for vol_name in unused_volumes:
            report.append(f"   - Volume Name: {vol_name}")
        report.append("\n")

    if not (dangling_images or exited_containers or unused_volumes):
        report.append("✨ Your garden is pristine! No digital weeds found. Keep up the good work! ✨\n")

    report.append("--- Disk Usage Overview ---\n")
    for item_type, data in system_df.items():
        report.append(f"🌳 {item_type}: {data.get('Size', 'N/A')} (Reclaimable: {data.get('Reclaimable', 'N/A')})")
    report.append("\n")

    return "\n".join(report)

def generate_prune_suggestions(dangling_images, exited_containers, unused_volumes):
    """Generates suggested pruning commands."""
    suggestions = []
    suggestions.append("✂️ Suggested Pruning Tools ✂️\n")
    suggestions.append("-------------------------------\n")

    if dangling_images or exited_containers or unused_volumes:
        suggestions.append("For a general tidy-up (removes stopped containers, dangling images, and unused networks/build cache):")
        suggestions.append("   docker system prune")
        suggestions.append("\n")

        if dangling_images:
            suggestions.append("To specifically remove dangling images:")
            suggestions.append(f"   docker rmi {' '.join(dangling_images)}")
            suggestions.append("\n")

        if exited_containers:
            suggestions.append("To specifically remove exited containers:")
            suggestions.append(f"   docker rm {' '.join(exited_containers)}")
            suggestions.append("\n")

        if unused_volumes:
            suggestions.append("To specifically remove unused volumes:")
            suggestions.append(f"   docker volume rm {' '.join(unused_volumes)}")
            suggestions.append("\n")
    else:
        suggestions.append("No pruning needed! Your garden is perfectly manicured.")

    return "\n".join(suggestions)

def main():
    parser = argparse.ArgumentParser(
        description="A whimsical Docker-based utility to scan for and report on unused Docker resources."
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Actually prune the identified resources using 'docker system prune'. Use with caution!"
    )
    args = parser.parse_args()

    print("Scanning your container garden for digital weeds...\n")

    dangling_images = get_dangling_images()
    exited_containers = get_exited_containers()
    unused_volumes = get_unused_volumes()
    system_df = get_system_df()

    report = generate_report(dangling_images, exited_containers, unused_volumes, system_df)
    print(report)

    if args.prune:
        print("Initiating garden pruning...\n")
        try:
            # docker system prune removes stopped containers, dangling images, unused networks, and build cache
            # It asks for confirmation, so we need to pass -f
            prune_output = run_docker_command(["docker", "system", "prune", "-f"], capture_output=False)
            print("\nGarden pruned successfully! 🌱")
            print(prune_output)
        except Exception as e:
            print(f"Error during pruning: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        prune_suggestions = generate_prune_suggestions(dangling_images, exited_containers, unused_volumes)
        print(prune_suggestions)

if __name__ == "__main__":
    main()
