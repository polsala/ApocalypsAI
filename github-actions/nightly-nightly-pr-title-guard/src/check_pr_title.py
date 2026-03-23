import argparse
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser(description='Validate PR title prefix')
    parser.add_argument('--prefix', required=True, help='Required prefix for the PR title')
    args = parser.parse_args()

    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path or not os.path.isfile(event_path):
        print('::error::GITHUB_EVENT_PATH is not set or file does not exist')
        sys.exit(1)

    try:
        with open(event_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f'::error::Failed to read event payload: {e}')
        sys.exit(1)

    title = data.get('pull_request', {}).get('title', '')
    if not isinstance(title, str):
        print('::error::PR title is missing or not a string')
        sys.exit(1)

    if not title.startswith(args.prefix):
        print(f"::error::PR title does not start with required prefix '{args.prefix}'. Title: '{title}'")
        sys.exit(1)

    print('PR title validation passed.')
    sys.exit(0)

if __name__ == '__main__':
    main()
