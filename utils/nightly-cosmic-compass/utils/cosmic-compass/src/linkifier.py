import re
import sys
import os
import argparse

def linkify_github_references(text: str, default_repo: str) -> str:
    """
    Transforms GitHub issue/PR references in text into clickable Markdown links.

    Args:
        text (str): The input text containing GitHub references.
        default_repo (str): The default 'owner/repo' string (e.g., 'polsala/ApocalypsAI')
                            to use for resolving local references like '#123'.

    Returns:
        str: The text with GitHub references replaced by Markdown links.
    """
    if not default_repo:
        raise ValueError("default_repo cannot be empty. Please provide a repository in 'owner/repo' format.")

    # Regex to find GitHub references:
    # 1. `owner/repo#issue_number` (e.g., `octocat/Spoon-Knife#42`)
    # 2. `#issue_number` (e.g., `#123`)
    # Issue numbers are typically positive integers.
    # We use a non-capturing group for the optional owner/repo part.
    pattern = re.compile(r'(?:(?P<owner>[a-zA-Z0-9_-]+)/(?P<repo>[a-zA-Z0-9_-]+))?#(?P<issue>\d+)')

    def replacer(match):
        owner = match.group('owner')
        repo = match.group('repo')
        issue = match.group('issue')

        if owner and repo:
            # Cross-repository reference
            full_repo = f"{owner}/{repo}"
            link_text = f"{owner}/{repo}#{issue}"
        else:
            # Local repository reference
            full_repo = default_repo
            link_text = f"#{issue}"

        # GitHub issues and PRs share the same URL structure for numbers
        url = f"https://github.com/{full_repo}/issues/{issue}"
        return f"[{link_text}]({url})"

    return pattern.sub(replacer, text)

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Compass: Transforms GitHub issue/PR references into clickable Markdown links."
    )
    parser.add_argument(
        "--repo",
        type=str,
        help="The default GitHub repository (e.g., 'polsala/ApocalypsAI') for local issue references. "
             "Falls back to GITHUB_REPOSITORY environment variable if not provided."
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a text file to process. If not provided, reads from standard input."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to a file where the linked output will be written. If not provided, writes to standard output."
    )

    args = parser.parse_args()

    default_repo = args.repo or os.environ.get("GITHUB_REPOSITORY")

    if not default_repo:
        print("Error: No default repository provided. Use --repo argument or set GITHUB_REPOSITORY environment variable.", file=sys.stderr)
        sys.exit(1)

    input_content = ""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_content = f.read()
        except FileNotFoundError:
            print(f"Error: Input file not found at '{args.file}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        input_content = sys.stdin.read()

    try:
        linked_content = linkify_github_references(input_content, default_repo)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(linked_content)
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        sys.stdout.write(linked_content)

if __name__ == "__main__":
    main()
