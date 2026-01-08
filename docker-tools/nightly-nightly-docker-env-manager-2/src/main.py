import yaml
import subprocess
import sys
import os

class DockerEnvManager:
    def __init__(self, env_dir="environments", dockerfile_dir="dockerfiles"):
        self.env_dir = env_dir
        self.dockerfile_dir = dockerfile_dir
        self.environments = {}
        self.load_environments()

    def load_environments(self):
        if not os.path.exists(self.env_dir):
            return
        for filename in os.listdir(self.env_dir):
            if filename.endswith(".yaml"):
                filepath = os.path.join(self.env_dir, filename)
                with open(filepath, 'r') as f:
                    try:
                        env_config = yaml.safe_load(f)
                        if env_config and 'name' in env_config:
                            self.environments[env_config['name']] = env_config
                    except yaml.YAMLError as e:
                        print(f"Error loading {filename}: {e}", file=sys.stderr)

    def get_env_config(self, env_name):
        return self.environments.get(env_name)

    def run_command(self, cmd_list):
        try:
            result = subprocess.run(cmd_list, capture_output=True, text=True, check=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}", file=sys.stderr)
            print(f"Stderr: {e.stderr}", file=sys.stderr)
            return False
        except FileNotFoundError:
            print(f"Error: Docker command not found. Is Docker installed and in your PATH?", file=sys.stderr)
            return False

    def up(self, env_name):
        config = self.get_env_config(env_name)
        if not config:
            print(f"Environment '{env_name}' not found.", file=sys.stderr)
            return

        container_name = f"apoc-env-{env_name}"
        docker_cmd = ["docker", "run", "-d", "--name", container_name]

        if "image" in config:
            docker_cmd.extend(["-i", config["image"]])
        elif "dockerfile" in config:
            dockerfile_path = os.path.join(self.dockerfile_dir, config["dockerfile"])
            if not os.path.exists(dockerfile_path):
                print(f"Dockerfile '{config['dockerfile']}' not found in {self.dockerfile_dir}", file=sys.stderr)
                return
            build_context = self.dockerfile_dir
            image_tag = f"apoc-env-{env_name}-custom"
            build_cmd = ["docker", "build", "-t", image_tag, "-f", dockerfile_path, build_context]
            print(f"Building custom image for '{env_name}'...")
            if not self.run_command(build_cmd):
                return
            docker_cmd.extend(["-i", image_tag])
        else:
            print(f"Environment '{env_name}' must specify either 'image' or 'dockerfile'.", file=sys.stderr)
            return

        if "ports" in config:
            for port in config["ports"]:
                docker_cmd.extend(["-p", port])
        if "volumes" in config:
            for volume in config["volumes"]:
                docker_cmd.extend(["-v", volume])
        if "environment" in config:
            for env_var in config["environment"]:
                docker_cmd.extend(["-e", env_var])

        print(f"Starting environment '{env_name}'...")
        if self.run_command(docker_cmd):
            if "commands" in config:
                print(f"Executing post-start commands for '{env_name}'...")
                for cmd in config["commands"]:
                    exec_cmd = ["docker", "exec", container_name] + cmd.split()
                    if not self.run_command(exec_cmd):
                        print(f"Warning: Command '{cmd}' failed.", file=sys.stderr)

    def down(self, env_name):
        container_name = f"apoc-env-{env_name}"
        print(f"Stopping and removing environment '{env_name}'...")
        self.run_command(["docker", "stop", container_name])
        self.run_command(["docker", "rm", container_name])

    def logs(self, env_name):
        container_name = f"apoc-env-{env_name}"
        print(f"Logs for environment '{env_name}':")
        self.run_command(["docker", "logs", container_name])

    def exec(self, env_name, command):
        container_name = f"apoc-env-{env_name}"
        print(f"Executing command in '{env_name}': {command}")
        exec_cmd = ["docker", "exec", container_name] + command.split()
        self.run_command(exec_cmd)

def main():
    if len(sys.argv) < 3:
        print("Usage: python src/main.py <command> <environment_name> [command_args...]", file=sys.stderr)
        print("Commands: up, down, logs, exec", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    env_name = sys.argv[2]
    manager = DockerEnvManager()

    if command == "up":
        manager.up(env_name)
    elif command == "down":
        manager.down(env_name)
    elif command == "logs":
        manager.logs(env_name)
    elif command == "exec":
        if len(sys.argv) < 4:
            print("Usage: python src/main.py exec <environment_name> <command>", file=sys.stderr)
            sys.exit(1)
        command_args = sys.argv[3:]
        manager.exec(env_name, " ".join(command_args))
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
