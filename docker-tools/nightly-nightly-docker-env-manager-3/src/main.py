import subprocess
import sys
import os

def run_command(command):
    """Executes a shell command and returns its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Error output:\n{result.stderr}", file=sys.stderr)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}", file=sys.stderr)
        print(f"Stderr:\n{e.stderr}", file=sys.stderr)
        sys.exit(1)

def build_docker_image(env_name):
    """Builds the Docker image for a given environment."""
    env_dir = os.path.abspath(env_name)
    if not os.path.isdir(env_dir):
        print(f"Error: Environment directory '{env_name}' not found.", file=sys.stderr)
        sys.exit(1)
    
    dockerfile_path = os.path.join(env_dir, 'Dockerfile')
    if not os.path.exists(dockerfile_path):
        print(f"Error: Dockerfile not found in '{env_dir}'.", file=sys.stderr)
        sys.exit(1)

    print(f"Building Docker image for environment: {env_name}...")
    run_command(f"docker build -t apoc-{env_name}-env {env_dir}")

def start_environment(env_name):
    """Starts a Docker container for the specified environment."""
    env_dir = os.path.abspath(env_name)
    compose_file = os.path.join(env_dir, 'docker-compose.yml')

    if os.path.exists(compose_file):
        print(f"Starting environment '{env_name}' using docker-compose...")
        # Change directory to ensure docker-compose uses the correct context
        original_dir = os.getcwd()
        os.chdir(env_dir)
        run_command("docker-compose up -d")
        os.chdir(original_dir)
    else:
        print(f"Starting environment '{env_name}' using direct docker run...")
        # Mount current directory into the container for development
        run_command(f"docker run --rm -it -v $(pwd):/app apoc-{env_name}-env")

def stop_environment(env_name):
    """Stops a Docker environment managed by docker-compose."""
    env_dir = os.path.abspath(env_name)
    compose_file = os.path.join(env_dir, 'docker-compose.yml')

    if os.path.exists(compose_file):
        print(f"Stopping environment '{env_name}'...")
        original_dir = os.getcwd()
        os.chdir(env_dir)
        run_command("docker-compose down")
        os.chdir(original_dir)
    else:
        print(f"Environment '{env_name}' does not use docker-compose. Use 'docker stop <container_id>' or 'docker rm <container_id>'.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python src/main.py <command> <environment_name>")
        print("Commands: start, stop, build")
        sys.exit(1)

    command = sys.argv[1]
    env_name = sys.argv[2]

    if command == "start":
        start_environment(env_name)
    elif command == "stop":
        stop_environment(env_name)
    elif command == "build":
        build_docker_image(env_name)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
