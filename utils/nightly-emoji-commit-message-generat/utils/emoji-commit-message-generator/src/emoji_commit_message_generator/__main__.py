'''Entry point for the emoji commit message generator CLI.

Usage:
    python -m emoji_commit_message_generator "Your commit message"
'''

import sys
from .emoji_generator import format_commit


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print('Usage: python -m emoji_commit_message_generator "<message>"')
        return 2
    message = ' '.join(argv)
    print(format_commit(message))
    return 0


if __name__ == '__main__':
    sys.exit(main())
