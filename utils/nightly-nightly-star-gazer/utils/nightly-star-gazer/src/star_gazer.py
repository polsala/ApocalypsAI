import argparse
import os
import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

STAR_TIERS = [
    (0, 99, "Dust Cloud"),
    (100, 499, "Nebula Nook"),
    (500, 999, "Comet Cluster"),
    (1000, 4999, "Stellar Swarm"),
    (5000, 9999, "Galactic Gem"),
    (10000, float('inf'), "Cosmic Colossus"),
]

def get_repo_stars(repo_full_name: str, github_token: str = None) -> int:
    """Fetches the star count for a given GitHub repository."""
    url = f"https://api.github.com/repos/{repo_full_name}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data.get("stargazers_count", 0)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            console.print(f"[bold red]Error:[/bold red] Repository '{repo_full_name}' not found.")
        elif e.response.status_code == 403 and 'rate limit exceeded' in e.response.text:
            console.print("[bold red]Error:[/bold red] GitHub API rate limit exceeded. Please try again later or provide a GITHUB_TOKEN.")
        else:
            console.print(f"[bold red]Error:[/bold red] HTTP error fetching stars: {e}")
        return -1 # Indicate an error
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Error:[/bold red] Could not connect to GitHub API. Check your internet connection.")
        return -1
    except requests.exceptions.Timeout:
        console.print("[bold red]Error:[/bold red] GitHub API request timed out.")
        return -1
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error:[/bold red] An unexpected error occurred: {e}")
        return -1

def get_constellation_name(star_count: int) -> str:
    """Determines the constellation name based on the star count."""
    for min_stars, max_stars, name in STAR_TIERS:
        if min_stars <= star_count <= max_stars:
            return name
    return "Unknown Realm" # Should not happen with float('inf') but as a fallback

def main():
    parser = argparse.ArgumentParser(
        description="Gaze upon the stars of your GitHub repository!"
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="Full name of the GitHub repository (e.g., owner/repo_name)"
    )
    args = parser.parse_args()

    repo_full_name = args.repo
    github_token = os.environ.get("GITHUB_TOKEN")

    console.print(Panel(
        Text("🌌 Nightly Star-Gazing Report 🌌", justify="center", style="bold yellow"),
        title=f"[bold blue]For {repo_full_name}[/bold blue]",
        border_style="magenta"
    ))

    star_count = get_repo_stars(repo_full_name, github_token)

    if star_count == -1:
        console.print("[bold red]Failed to retrieve star count. Exiting.[/bold red]")
        exit(1)
    elif star_count == 0:
        constellation = get_constellation_name(star_count)
        console.print(f"Repository: [bold green]{repo_full_name}[/bold green]")
        console.print(f"Current Stars: [bold white]{star_count}[/bold white]")
        console.print(f"Constellation: [bold cyan]{constellation}[/bold cyan]")
        console.print("\n[italic blue]Just starting its cosmic journey! Keep building![/italic blue]")
    else:
        constellation = get_constellation_name(star_count)
        console.print(f"Repository: [bold green]{repo_full_name}[/bold green]")
        console.print(f"Current Stars: [bold white]{star_count}[/bold white]")
        console.print(f"Constellation: [bold cyan]{constellation}[/bold cyan]")
        console.print("\n[italic blue]Keep shining bright, cosmic voyager![/italic blue]")

if __name__ == "__main__":
    main()
