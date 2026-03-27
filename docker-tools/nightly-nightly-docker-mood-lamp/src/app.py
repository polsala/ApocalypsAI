import os
import time
import docker
from docker.errors import DockerException

# Terminal color codes
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_BLUE = "\033[94m"

def get_stack_health(client, project_name):
    """Determines the overall health of a Docker Compose stack."""
    if not project_name:
        return "blue", "🔵 Just waking up... (COMPOSE_PROJECT_NAME not set)"

    try:
        # Filter containers by the Docker Compose project label
        # The label is typically 'com.docker.compose.project' for Docker Compose V2+
        # or 'com.docker.compose.project' for older versions.
        # We'll check both for robustness.
        containers = client.containers.list(filters={
            "label": [
                f"com.docker.compose.project={project_name}",
                f"com.docker.compose.project.working_dir={project_name}" # Older compose versions might use this
            ]
        })

        if not containers:
            return "blue", f"🔵 Just waking up... (No containers found for project '{project_name}')"

        all_healthy = True
        any_unhealthy = False
        any_restarting = False
        any_exited = False
        any_paused = False

        for container in containers:
            # Check container status
            if container.status == 'exited':
                any_exited = True
                all_healthy = False
            elif container.status == 'restarting':
                any_restarting = True
                all_healthy = False
            elif container.status == 'paused':
                any_paused = True
                all_healthy = False

            # Check healthcheck status if available
            if hasattr(container, 'health') and container.health:
                if container.health.status == 'unhealthy':
                    any_unhealthy = True
                    all_healthy = False
                elif container.health.status == 'starting':
                    any_restarting = True # Treat 'starting' health as 'wobbly'
                    all_healthy = False

        if any_exited or any_unhealthy:
            return "red", f"🔴 Uh Oh, Trouble in Paradise! (Project: '{project_name}')"
        elif any_restarting or any_paused:
            return "yellow", f"🟡 A Bit Wobbly... (Project: '{project_name}')"
        elif all_healthy:
            return "green", f"🟢 All Systems Go! (Project: '{project_name}')"
        else:
            # Fallback for other states not explicitly handled but not 'all_healthy'
            return "blue", f"🔵 Just waking up... (Project: '{project_name}' - unknown state)"

    except DockerException as e:
        return "red", f"🔴 Error connecting to Docker: {e}"
    except Exception as e:
        return "red", f"🔴 An unexpected error occurred: {e}"

def print_mood(color_code, message):
    """Prints the colored mood message to the console."""
    print(f"{color_code}{message}{COLOR_RESET}")

def main():
    project_name = os.getenv("COMPOSE_PROJECT_NAME")
    check_interval = int(os.getenv("CHECK_INTERVAL_SECONDS", "5"))

    if not project_name:
        print_mood(COLOR_RED, "🔴 Error: COMPOSE_PROJECT_NAME environment variable is not set.")
        print_mood(COLOR_RED, "🔴 Please set it to the name of your Docker Compose project.")
        exit(1)

    try:
        client = docker.from_env()
        print_mood(COLOR_BLUE, f"🔵 Starting Docker Mood Lamp for project: '{project_name}'")
        print_mood(COLOR_BLUE, f"🔵 Checking every {check_interval} seconds...")

        while True:
            color, message = get_stack_health(client, project_name)
            if color == "green":
                print_mood(COLOR_GREEN, message)
            elif color == "yellow":
                print_mood(COLOR_YELLOW, message)
            elif color == "red":
                print_mood(COLOR_RED, message)
            else:
                print_mood(COLOR_BLUE, message)
            time.sleep(check_interval)

    except DockerException as e:
        print_mood(COLOR_RED, f"🔴 Failed to connect to Docker daemon: {e}")
        print_mood(COLOR_RED, "🔴 Ensure the Docker socket is mounted and Docker is running.")
        exit(1)
    except KeyboardInterrupt:
        print_mood(COLOR_BLUE, "🔵 Exiting Mood Lamp. Goodbye!")
        exit(0)

if __name__ == "__main__":
    main()
