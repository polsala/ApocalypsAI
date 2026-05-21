import docker
import sys

def get_container_status(container):
    """
    Determines the whimsical status of a container based on its Docker state.
    """
    state = container.attrs['State']
    status = state['Status']
    health = state.get('Health', {}).get('Status')

    if status == 'running':
        if health == 'healthy':
            return "purring happily", "healthy"
        elif health == 'unhealthy':
            return "looking a bit green", "unhealthy"
        else: # running but no healthcheck or unknown health status
            return "idling contentedly", "running"
    elif status == 'exited':
        return "wandered off", "exited"
    elif status == 'created':
        return "just hatched", "created"
    elif status == 'paused':
        return "taking a nap", "paused"
    else:
        return f"in an unusual state ({status})", "unknown"

def get_care_instructions(container_name, whimsical_status, actual_status):
    """
    Generates whimsical care instructions and a suggested command based on the container's status.
    """
    instructions = ""
    command = ""

    if actual_status == "healthy":
        instructions = f"Your {container_name} critter is {whimsical_status}! Keep an eye on its joyful antics."
        command = f"docker logs {container_name}"
    elif actual_status == "unhealthy":
        instructions = f"Oh dear, your {container_name} critter is {whimsical_status}. It might need a vet visit!"
        command = f"docker inspect {container_name} --format '{{{{json .State.Health}}}}'"
    elif actual_status == "exited":
        instructions = f"Your {container_name} critter has {whimsical_status}. Time to coax it back into action!"
        command = f"docker start {container_name}"
    elif actual_status == "paused":
        instructions = f"Your {container_name} critter is {whimsical_status}. Gently wake it up for some playtime!"
        command = f"docker unpause {container_name}"
    elif actual_status == "created":
        instructions = f"Your {container_name} critter has {whimsical_status}. It's eager to explore!"
        command = f"docker start {container_name}"
    else: # running, unknown, or other
        instructions = f"Your {container_name} critter is {whimsical_status}. A gentle nudge might help understand its mood."
        command = f"docker inspect {container_name}"

    return instructions, command

def main():
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True) # Get all containers, not just running ones
        
        if not containers:
            print("No container critters found to care for! Perhaps it's time to adopt some?")
            return

        print("--- Container Critter Care Report ---")
        for container in containers:
            name = container.name
            whimsical_status, actual_status = get_container_status(container)
            instructions, command = get_care_instructions(name, whimsical_status, actual_status)
            
            print(f"\nCritter: {name}")
            print(f"  Status: {whimsical_status.capitalize()}")
            print(f"  Care Tip: {instructions}")
            print(f"  Suggested Action: {command}")
        print("\n--- End of Report ---")

    except docker.errors.DockerException as e:
        print(f"Error connecting to Docker daemon: {e}", file=sys.stderr)
        print("Please ensure Docker is running and the Docker socket is accessible.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
