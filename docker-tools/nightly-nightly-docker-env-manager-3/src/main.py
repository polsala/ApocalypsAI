import docker
import yaml
import os
import sys
import subprocess

class DockerEnvManager:
    def __init__(self, env_config_path='env.yaml'):
        self.client = docker.from_env()
        self.env_config_path = env_config_path
        self.config = self._load_config()
        self.container_name = f"apoc-{self.config.get('name', 'default')}"

    def _load_config(self):
        if not os.path.exists(self.env_config_path):
            print(f"Error: Environment configuration file '{self.env_config_path}' not found.", file=sys.stderr)
            sys.exit(1)
        with open(self.env_config_path, 'r') as f:
            return yaml.safe_load(f)

    def _get_container(self):
        try:
            return self.client.containers.get(self.container_name)
        except docker.errors.NotFound:
            return None

    def up(self):
        container = self._get_container()
        if container:
            print(f"Environment '{self.container_name}' is already running.")
            return

        image_name = self.config.get('image', 'ubuntu:latest')
        ports = self.config.get('ports', {})
        volumes = self.config.get('volumes', {})
        commands = self.config.get('commands', [])

        # Ensure volumes are correctly formatted for docker-py
        volume_bindings = {}
        for vol_str in volumes:
            host_path, container_path = vol_str.split(':', 1)
            volume_bindings[os.path.abspath(host_path)] = {'bind': container_path, 'mode': 'rw'}

        # Ensure ports are correctly formatted for docker-py
        port_bindings = {}
        for port_str in ports:
            host_port, container_port = port_str.split(':', 1)
            port_bindings[container_port] = host_port

        try:
            print(f"Starting environment '{self.container_name}' with image '{image_name}'...")
            container = self.client.containers.run(
                image_name,
                detach=True,
                name=self.container_name,
                ports=port_bindings,
                volumes=volume_bindings,
                tty=True, # Keep container running
                stdin_open=True # Allow interaction
            )
            print(f"Environment '{self.container_name}' started successfully.")

            # Execute initial commands if any
            if commands:
                print("Executing initial commands...")
                for cmd in commands:
                    exec_result = container.exec_run(cmd)
                    if exec_result.exit_code != 0:
                        print(f"Warning: Command '{cmd}' failed with exit code {exec_result.exit_code}", file=sys.stderr)
                        print(exec_result.output.decode(), file=sys.stderr)
                    else:
                        print(f"Command '{cmd}' executed successfully.")

        except docker.errors.ImageNotFound:
            print(f"Error: Docker image '{image_name}' not found. Please build it first.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred while starting the container: {e}", file=sys.stderr)
            sys.exit(1)

    def down(self):
        container = self._get_container()
        if not container:
            print(f"Environment '{self.container_name}' is not running.")
            return

        try:
            print(f"Stopping and removing environment '{self.container_name}'...")
            container.stop()
            container.remove()
            print(f"Environment '{self.container_name}' stopped and removed.")
        except Exception as e:
            print(f"An error occurred while stopping/removing the container: {e}", file=sys.stderr)
            sys.exit(1)

    def logs(self):
        container = self._get_container()
        if not container:
            print(f"Environment '{self.container_name}' is not running.")
            return

        try:
            print(f"Logs for environment '{self.container_name}':")
            print(container.logs().decode('utf-8'))
        except Exception as e:
            print(f"An error occurred while fetching logs: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: docker-env-manager <up|down|logs>")
        sys.exit(1)

    command = sys.argv[1]
    manager = DockerEnvManager()

    if command == 'up':
        manager.up()
    elif command == 'down':
        manager.down()
    elif command == 'logs':
        manager.logs()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
