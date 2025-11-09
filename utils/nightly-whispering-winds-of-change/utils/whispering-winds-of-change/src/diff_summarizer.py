import argparse
import subprocess
import sys
import os

def get_git_diff(ref1: str, ref2: str) -> str:
    """Executes git diff between two references and returns the output."""
    try:
        result = subprocess.run(
            ['git', 'diff', ref1, ref2],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Git command not found. Please ensure Git is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

def parse_diff(diff_content: str) -> dict:
    """Parses a git diff string and extracts summary information."""
    lines_added = 0
    lines_removed = 0
    files_changed = set()

    for line in diff_content.splitlines():
        if line.startswith('+++ b/') or line.startswith('--- a/'):
            # Extract file path, remove 'a/' or 'b/' prefix
            file_path = line[6:] if line.startswith('+++ b/') else line[6:]
            if file_path:
                files_changed.add(file_path)
        elif line.startswith('+') and not line.startswith('+++'):
            lines_added += 1
        elif line.startswith('-') and not line.startswith('---'):
            lines_removed += 1

    return {
        'lines_added': lines_added,
        'lines_removed': lines_removed,
        'files_changed': sorted(list(files_changed))
    }

def main():
    parser = argparse.ArgumentParser(
        description="Summarize changes from a Git diff."
    )
    parser.add_argument(
        'ref1', nargs='?',
        help="First Git reference (e.g., commit hash, branch name). Required if --file is not used."
    )
    parser.add_argument(
        'ref2', nargs='?',
        help="Second Git reference. Required if --file is not used."
    )
    parser.add_argument(
        '--file', '-f',
        help="Path to a file containing the Git diff output."
    )

    args = parser.parse_args()

    diff_content = ""

    if args.file:
        if args.ref1 or args.ref2:
            parser.error("Cannot use --file with Git references (ref1, ref2).")
        if not os.path.exists(args.file):
            parser.error(f"Diff file not found: {args.file}")
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                diff_content = f.read()
        except IOError as e:
            print(f"Error reading diff file: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.ref1 and args.ref2:
        diff_content = get_git_diff(args.ref1, args.ref2)
    else:
        parser.error("Either provide two Git references or use the --file option.")

    if not diff_content:
        print("No diff content to summarize.")
        sys.exit(0)

    summary = parse_diff(diff_content)

    print("\n--- Whispering Winds of Change Summary ---")
    print(f"\nTotal Lines Added: {summary['lines_added']}")
    print(f"Total Lines Removed: {summary['lines_removed']}")

    if summary['files_changed']:
        print("\nFiles Changed:")
        for f in summary['files_changed']:
            print(f"- {f}")
    else:
        print("\nNo files changed (or diff was empty).")

    print("\n------------------------------------------\n")


if __name__ == '__main__':
    main()
