import sys
import os
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table
from docker import from_env
from docker.errors import NotFound

console = Console()

# Mock rationale: Using a fixed path for environments within the container.
ENV_DIR = Path("/app/environments")

def get_environments():
    """Finds all valid docker-compose files in the environment directory."""
    return [f.stem for f in ENV_DIR.glob("*.yaml") if f.is_file()]

def get_docker_client():
    """Returns a Docker client instance."""
    try:
        return from_env()
    except Exception as e:
        console.print(f"[bold red]Error connecting to Docker daemon: {e}[/bold red]")
        sys.exit(1)

def start_environment(env_name):
    """Starts a Docker Compose environment."""
    env_file = ENV_DIR / f"{env_name}.yaml"
    if not env_file.exists():
        console.print(f"[bold red]Environment file not found: {env_file}[/bold red]")
        return

    console.print(f"[bold green]Starting environment: {env_name}...[/bold green]")
    try:
        # Mock rationale: Using subprocess to call docker-compose for simplicity in this example.
        # In a real-world scenario, a dedicated Docker SDK for Compose might be preferred.
        import subprocess
        result = subprocess.run(
            ["docker-compose", "-f", str(env_file), "up", "-d"],
            capture_output=True,
            text=True,
            check=True
        )
        console.print(f"[green]Successfully started {env_name}.[/green]")
        if result.stdout:
            console.print(result.stdout)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error starting {env_name}:[/bold red]")
        console.print(e.stderr)
    except FileNotFoundError:
        console.print("[bold red]docker-compose command not found. Please ensure it is installed and in your PATH.[/bold red]")

def stop_environment(env_name):
    """Stops and removes a Docker Compose environment."""
    env_file = ENV_DIR / f"{env_name}.yaml"
    if not env_file.exists():
        console.print(f"[bold red]Environment file not found: {env_file}[/bold red]")
        return

    console.print(f"[bold yellow]Stopping environment: {env_name}...[/bold yellow]")
    try:
        import subprocess
        result = subprocess.run(
            ["docker-compose", "-f", str(env_file), "down"],
            capture_output=True,
            text=True,
            check=True
        )
        console.print(f"[yellow]Successfully stopped and removed {env_name}.[/yellow]")
        if result.stdout:
            console.print(result.stdout)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error stopping {env_name}:[/bold red]")
        console.print(e.stderr)
    except FileNotFoundError:
        console.print("[bold red]docker-compose command not found. Please ensure it is installed and in your PATH.[/bold red]")

def list_environments():
    """Lists all available environments."""
    envs = get_environments()
    if not envs:
        console.print("[italic]No environments found. Create .yaml files in the environments/ directory.[/italic]")
        return

    table = Table(title="Available Environments")
    table.add_column("Name", style="dim", width=12)
    table.add_column("Status", justify="right")

    client = get_docker_client()
    for env_name in envs:
        status = "Unknown"
        try:
            # Mock rationale: Checking container status to infer environment status.
            # This is a simplification; a more robust check would involve inspecting docker-compose project names.
            containers = client.containers.list(all=True, filters={"label": f"com.docker.compose.project={env_name}"})
            if containers:
                # Check if any container is running
                if any(c.status == 'running' for c in containers):
                    status = "[bold green]Running[/bold green]"
                else:
                    status = "[bold red]Stopped[/bold red]"
            else:
                status = "[bold red]Stopped[/bold red]"
        except Exception as e:
            status = f"[bold yellow]Error: {e}[/bold yellow]"
        table.add_row(env_name, status)
    console.print(table)

def get_environment_status(env_name):
    """Shows the status of a specific environment."""
    env_file = ENV_DIR / f"{env_name}.yaml"
    if not env_file.exists():
        console.print(f"[bold red]Environment file not found: {env_file}[/bold red]")
        return

    console.print(f"[bold cyan]Status for environment: {env_name}...[/bold cyan]")
    client = get_docker_client()
    try:
        containers = client.containers.list(all=True, filters={"label": f"com.docker.compose.project={env_name}"})
        if not containers:
            console.print(f"[bold red]Environment '{env_name}' is not running.[/bold red]")
            return

        table = Table(title=f"Environment: {env_name}")
        table.add_column("Container Name", style="dim")
        table.add_column("Image")
        table.add_column("Status")
        table.add_column("Ports")

        for container in containers:
            ports_str = ", ".join([f"{p['HostPort']}:{p['ContainerPort']}" for p in container.ports.values()]) if container.ports else "N/A"
            status_color = "green" if container.status == 'running' else "red"
            table.add_row(
                container.name,
                container.image.tags[0] if container.image.tags else "<none>",
                f"[bold {status_color}]{container.status}[/bold {status_color}]",
                ports_str
            )
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error getting status for {env_name}: {e}[/bold red]")

def main():
    if len(sys.argv) < 2:
        console.print("[bold red]Usage: python main.py <command> [environment_name][/bold red]")
        console.print("Commands: up, down, list, status")
        sys.exit(1)

    command = sys.argv[1]

    if command == "up":
        if len(sys.argv) < 3:
            console.print("[bold red]Usage: python main.py up <environment_name>[/bold red]")
            sys.exit(1)
        env_name = sys.argv[2]
        start_environment(env_name)
    elif command == "down":
        if len(sys.argv) < 3:
            console.print("[bold red]Usage: python main.py down <environment_name>[/bold red]")
            sys.exit(1)
        env_name = sys.argv[2]
        stop_environment(env_name)
    elif command == "list":
        list_environments()
    elif command == "status":
        if len(sys.argv) < 3:
            console.print("[bold red]Usage: python main.py status <environment_name>[/bold red]")
            sys.exit(1)
        env_name = sys.argv[2]
        get_environment_status(env_name)
    else:
        console.print(f"[bold red]Unknown command: {command}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
