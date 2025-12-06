import requests
import argparse
import os
import sys

def search_repositories(
    language: str,
    min_stars: int = 0,
    sort_by: str = 'stars',
    order: str = 'desc',
    limit: int = 10,
    github_token: str = None
) -> list:
    """Searches GitHub repositories based on specified criteria.

    Args:
        language: The primary programming language to search for.
        min_stars: Minimum number of stars a repository must have.
        sort_by: Field to sort the results by ('stars', 'forks', 'updated').
        order: Order of sorting ('asc', 'desc').
        limit: Maximum number of repositories to display.
        github_token: Optional GitHub Personal Access Token for higher rate limits.

    Returns:
        A list of dictionaries, each representing a repository.
    """
    base_url = "https://api.github.com/search/repositories"
    query = f"language:{language} stars:>={min_stars}"

    params = {
        'q': query,
        'sort': sort_by,
        'order': order,
        'per_page': limit
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    if github_token:
        headers['Authorization'] = f'token {github_token}'

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        return data.get('items', [])
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403 and 'rate limit exceeded' in response.text.lower():
            print(f"Error: GitHub API rate limit exceeded. Please wait or provide a GitHub token. {e}", file=sys.stderr)
        else:
            print(f"Error fetching repositories: {e}", file=sys.stderr)
        return []
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Could not connect to GitHub API. Check your internet connection. {e}", file=sys.stderr)
        return []
    except requests.exceptions.Timeout as e:
        print(f"Error: Request to GitHub API timed out. {e}", file=sys.stderr)
        return []
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return []

def main():
    parser = argparse.ArgumentParser(
        description="Discover GitHub repositories with the Cosmic Compass."
    )
    parser.add_argument(
        '--language', 
        type=str, 
        required=True, 
        help="Primary programming language (e.g., 'python', 'javascript')."
    )
    parser.add_argument(
        '--min-stars', 
        type=int, 
        default=0, 
        help="Minimum number of stars a repository must have. Default: 0."
    )
    parser.add_argument(
        '--sort-by', 
        type=str, 
        choices=['stars', 'forks', 'updated'], 
        default='stars', 
        help="Field to sort results by. Options: 'stars', 'forks', 'updated'. Default: 'stars'."
    )
    parser.add_argument(
        '--order', 
        type=str, 
        choices=['asc', 'desc'], 
        default='desc', 
        help="Order of sorting. Options: 'asc', 'desc'. Default: 'desc'."
    )
    parser.add_argument(
        '--limit', 
        type=int, 
        default=10, 
        help="Maximum number of repositories to display. Default: 10."
    )
    parser.add_argument(
        '--token', 
        type=str, 
        default=os.environ.get('GITHUB_TOKEN'), 
        help="Your GitHub Personal Access Token. Also checks GITHUB_TOKEN env var."
    )

    args = parser.parse_args()

    repositories = search_repositories(
        language=args.language,
        min_stars=args.min_stars,
        sort_by=args.sort_by,
        order=args.order,
        limit=args.limit,
        github_token=args.token
    )

    if repositories:
        print(f"\n--- Top {len(repositories)} {args.language.capitalize()} Repositories (Stars >= {args.min_stars}) ---")
        for i, repo in enumerate(repositories):
            print(f"\n{i+1}. {repo['full_name']}")
            print(f"   Description: {repo['description'] or 'N/A'}")
            print(f"   Stars: {repo['stargazers_count']}")
            print(f"   Forks: {repo['forks_count']}")
            print(f"   Last Updated: {repo['updated_at']}")
            print(f"   URL: {repo['html_url']}")
        print("\n------------------------------------------------------------------")
    else:
        print(f"No {args.language.capitalize()} repositories found matching your criteria.")

if __name__ == '__main__':
    main()
