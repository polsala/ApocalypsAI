# GitHub Cosmic Compass

## Navigate the GitHub Universe!

This utility acts as your personal 'Cosmic Compass', helping you discover fascinating and trending repositories across GitHub. Whether you're looking for projects in a specific language, with a minimum number of stars, or sorted by recent activity, the Cosmic Compass will guide you to your next stellar discovery.

## Features

*   **Language Filtering**: Pinpoint repositories written in your preferred programming language.
*   **Star Threshold**: Filter out less popular projects by setting a minimum star count.
*   **Sorting Options**: Sort results by stars, forks, or last updated date.
*   **Result Limiting**: Control how many top results you see.
*   **GitHub Token Support**: Use a personal access token for higher rate limits (optional).

## Installation

This utility is self-contained. No special installation steps are required beyond having Python 3.x installed. It uses the `requests` library, which is a standard dependency for ApocalypsAI agents.

## Usage

Run the `cosmic_compass.py` script from its directory:

```bash
python src/cosmic_compass.py --language python --min-stars 100 --sort-by stars --order desc --limit 5
```

### Arguments:

*   `--language <str>`: (Required) The primary programming language to search for (e.g., `python`, `javascript`, `rust`).
*   `--min-stars <int>`: (Optional) Minimum number of stars a repository must have. Default: `0`.
*   `--sort-by <str>`: (Optional) Field to sort the results by. Options: `stars`, `forks`, `updated`. Default: `stars`.
*   `--order <str>`: (Optional) Order of sorting. Options: `asc`, `desc`. Default: `desc`.
*   `--limit <int>`: (Optional) Maximum number of repositories to display. Default: `10`.
*   `--token <str>`: (Optional) Your GitHub Personal Access Token. Using a token increases API rate limits. If not provided, the utility will check the `GITHUB_TOKEN` environment variable.

### Example:

Find the top 3 most recently updated Rust projects with at least 500 stars:

```bash
python src/cosmic_compass.py --language rust --min-stars 500 --sort-by updated --order desc --limit 3
```

## Development & Testing

To run the tests, navigate to the `utils/github-cosmic-compass/` directory and execute:

```bash
python -m unittest tests/test_cosmic_compass.py
```
