import docker
import os
import sys
import yaml
import argparse

class DockerEnvManager:
    def __init__(self):
        try:
            self.client = docker.from_env()
            self.client.ping()
        except Exception as e:
            print(f"Error connecting to Docker daemon: {e}", file=sys.stderr)
            sys.exit(1)
        self.envs_dir = os.path.join(os.path.dirname(__file__), '..', 'envs')
        os.makedirs(self.envs_dir, exist_ok=True)

    def _get_compose_file(self, env_name):
        return os.path.join(self.envs_dir, f"{env_name}.yml")

    def _create_default_compose(self, env_name, image):
        compose_content = {
            'version': '3.8',
            'services': {
                'app': {
                    'image': image,
                    'command': 'tail -f /dev/null',
                    'volumes': [
                        f'{os.getcwd()}:/app'
                    ]
                }
            }
        }
        compose_file = self._get_compose_file(env_name)
        with open(compose_file, 'w') as f:
            yaml.dump(compose_content, f)
        print(f"Created default compose file for '{env_name}' at {compose_file}")

    def start(self, env_name, image="ubuntu:latest"):
        compose_file = self._get_compose_file(env_name)
        if not os.path.exists(compose_file):
            print(f"Compose file for '{env_name}' not found. Creating a default one.")
            self._create_default_compose(env_name, image)

        try:
            # Use docker-compose command for more robust management
            # This assumes docker-compose is available in the PATH
            # For a pure Python solution, one would need to parse compose files and use client.containers.run
            # However, for simplicity and robustness, we delegate to the docker-compose CLI
            print(f"Starting environment '{env_name}'...")
            os.system(f"docker-compose -f {compose_file} up -d --build")
            print(f"Environment '{env_name}' started successfully.")
        except Exception as e:
            print(f"Error starting environment '{env_name}': {e}", file=sys.stderr)

    def stop(self, env_name):
        compose_file = self._get_compose_file(env_name)
        if not os.path.exists(compose_file):
            print(f"Compose file for '{env_name}' not found.", file=sys.stderr)
            return

        try:
            print(f"Stopping environment '{env_name}'...")
            os.system(f"docker-compose -f {compose_file} down")
            print(f"Environment '{env_name}' stopped successfully.")
        except Exception as e:
            print(f"Error stopping environment '{env_name}': {e}", file=sys.stderr)

    def list_envs(self):
        running_containers = self.client.containers.list()
        if not running_containers:
            print("No development environments are currently running.")
            return

        print("Running development environments:")
        for container in running_containers:
            # Attempt to infer environment name from container labels or names
            # This is a heuristic and might need refinement based on actual docker-compose naming conventions
            env_name = container.name.split('_')[0] if '_' in container.name else container.name
            print(f"- {env_name} (Container ID: {container.short_id})")

    def status(self, env_name):
        compose_file = self._get_compose_file(env_name)
        if not os.path.exists(compose_file):
            print(f"Compose file for '{env_name}' not found.", file=sys.stderr)
            return

        try:
            print(f"Checking status for environment '{env_name}'...")
            # Use docker-compose ps to get status
            os.system(f"docker-compose -f {compose_file} ps")
        except Exception as e:
            print(f"Error checking status for environment '{env_name}': {e}", file=sys.stderr)

    def logs(self, env_name):
        compose_file = self._get_compose_file(env_name)
        if not os.path.exists(compose_file):
            print(f"Compose file for '{env_name}' not found.", file=sys.stderr)
            return

        try:
            print(f"Fetching logs for environment '{env_name}'...")
            # Use docker-compose logs
            os.system(f"docker-compose -f {compose_file} logs")
        except Exception as e:
            print(f"Error fetching logs for environment '{env_name}': {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="ApocalypsAI Docker Environment Manager")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start a new development environment")
    start_parser.add_argument("env_name", help="Name of the environment to start")
    start_parser.add_argument("--image", default="ubuntu:latest", help="Docker image to use for the environment")

    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Stop a development environment")
    stop_parser.add_argument("env_name", help="Name of the environment to stop")

    # List command
    list_parser = subparsers.add_parser("list", help="List all running development environments")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show the status of a development environment")
    status_parser.add_argument("env_name", help="Name of the environment to check status for")

    # Logs command
    logs_parser = subparsers.add_parser("logs", help="Display logs for a development environment")
    logs_parser.add_argument("env_name", help="Name of the environment to get logs from")

    args = parser.parse_args()

    manager = DockerEnvManager()

    if args.command == "start":
        manager.start(args.env_name, args.image)
    elif args.command == "stop":
        manager.stop(args.env_name)
    elif args.command == "list":
        manager.list_envs()
    elif args.command == "status":
        manager.status(args.env_name)
    elif args.command == "logs":
        manager.logs(args.env_name)

if __name__ == "__main__":
    main()
