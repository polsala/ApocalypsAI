import yaml
import os
import subprocess

def create_dockerfile(env_config):
    """Generates a Dockerfile content based on the environment configuration."""
    base_image = env_config.get('base_image', 'ubuntu:latest')
    packages = env_config.get('packages', [])
    commands = env_config.get('commands', [])

    dockerfile_content = f"FROM {base_image}\n\n"

    if packages:
        # Basic package installation logic, can be extended for different package managers
        if 'apt-get' in base_image or 'debian' in base_image or 'ubuntu' in base_image:
            dockerfile_content += "RUN apt-get update && apt-get install -y --no-install-recommends \
" \
                                  + " \
".join([f"    {pkg}\
" for pkg in packages]) \
                                  + "&& rm -rf /var/lib/apt/lists/*\n\n"
        elif 'alpine' in base_image:
            dockerfile_content += "RUN apk update && apk add \
" \
                                  + " \
".join([f"    {pkg}\
" for pkg in packages]) \
                                  + "&& rm -rf /var/cache/apk/*\n\n"
        elif 'fedora' in base_image or 'centos' in base_image or 'rhel' in base_image:
            dockerfile_content += "RUN dnf update -y && dnf install -y \
" \
                                  + " \
".join([f"    {pkg}\
" for pkg in packages]) \
                                  + "&& dnf clean all\n\n"
        elif 'python:' in base_image and 'slim' not in base_image and 'alpine' not in base_image:
            # For standard Python images, assume pip is available or install it
            dockerfile_content += "RUN pip install --no-cache-dir \
" \
                                  + " \
".join([f"    {pkg}\
" for pkg in packages]) \
                                  + "\n\n"

    if commands:
        for cmd in commands:
            dockerfile_content += f"RUN {cmd}\n"

    return dockerfile_content

def create_docker_compose_file(env_config):
    """Generates a docker-compose.yml content for the environment."""
    env_name = env_config.get('environment_name', 'my-dev-env')
    image_name = env_name.lower().replace(' ', '-') # Use env_name as image name

    compose_content = f"version: '3.8'\n\nservices:\n  {env_name}:\n    build:\n      context: .\n      dockerfile: Dockerfile\n    image: {image_name}\n    volumes:\n      - ..:/workspace # Mount current directory to workspace
    # Add any other common configurations like ports, environment variables, etc.
    # For simplicity, we'll keep it minimal here.
"
    return compose_content

def main():
    config_path = "/app/env_config.yaml"
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at {config_path}")
        return

    with open(config_path, 'r') as f:
        env_config = yaml.safe_load(f)

    environment_name = env_config.get('environment_name', 'default-env')
    output_dir = environment_name.lower().replace(' ', '-')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create Dockerfile
    dockerfile_content = create_dockerfile(env_config)
    with open(os.path.join(output_dir, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)
    print(f"Generated Dockerfile in {output_dir}/")

    # Create docker-compose.yml
    docker_compose_content = create_docker_compose_file(env_config)
    with open(os.path.join(output_dir, 'docker-compose.yml'), 'w') as f:
        f.write(docker_compose_content)
    print(f"Generated docker-compose.yml in {output_dir}/")

    print(f"\nTo start your environment, navigate to the '{output_dir}' directory and run:")
    print(f"  docker-compose up -d")
    print(f"To enter your environment:")
    print(f"  docker-compose exec {environment_name} bash")

if __name__ == "__main__":
    main()
