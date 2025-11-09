import subprocess
import sys
from collections import Counter

def get_git_log_messages(num_commits: int = 20) -> list[str]:
    """
    Retrieves the last N commit messages from the Git log.
    """
    try:
        # Use --no-pager to ensure git doesn't try to use a pager
        # Use --pretty=format:%s to get only the subject line of the commit message
        result = subprocess.run(
            ['git', '--no-pager', 'log', f'-n{num_commits}', '--pretty=format:%s'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("Error: 'git' command not found. Is Git installed and in your PATH?", file=sys.stderr)
        return []

def analyze_sentiment(message: str) -> str:
    """
    Performs a simple keyword-based sentiment analysis on a commit message.
    Returns 'Positive', 'Negative', or 'Neutral/Mixed'.
    """
    message_lower = message.lower()

    positive_keywords = [
        'feat', 'feature', 'add', 'implement', 'improve', 'enhance', 'refactor',
        'optimize', 'fix', 'resolve', 'update', 'upgrade', 'pass', 'green',
        'good', 'better', 'success', 'complete', 'done', 'release', 'ship'
    ]
    negative_keywords = [
        'bug', 'error', 'fail', 'issue', 'broken', 'revert', 'bad', 'problem',
        'struggle', 'red', 'blocker', 'deprecate', 'remove', 'security'
    ]

    is_positive = any(keyword in message_lower for keyword in positive_keywords)
    is_negative = any(keyword in message_lower for keyword in negative_keywords)

    if is_positive and not is_negative:
        return 'Positive'
    elif is_negative and not is_positive:
        return 'Negative'
    else:
        # If both positive and negative keywords are present, or neither, it's mixed/neutral
        return 'Neutral/Mixed'

def main():
    num_commits = 20
    if len(sys.argv) > 1:
        try:
            num_commits = int(sys.argv[1])
            if num_commits <= 0:
                raise ValueError("Number of commits must be positive.")
        except ValueError:
            print("Invalid number of commits. Using default of 20.", file=sys.stderr)
            num_commits = 20

    commit_messages = get_git_log_messages(num_commits)

    if not commit_messages or commit_messages == ['']: # Handle empty repo or no commits
        print("No commit messages found to analyze.")
        return

    sentiments = [analyze_sentiment(msg) for msg in commit_messages]
    sentiment_counts = Counter(sentiments)

    total_commits = len(commit_messages)
    positive_count = sentiment_counts.get('Positive', 0)
    negative_count = sentiment_counts.get('Negative', 0)
    neutral_count = sentiment_counts.get('Neutral/Mixed', 0)

    print("\n🔮 Repo Mood Ring Analysis 🔮")
    print(f"Total Commits Analyzed: {total_commits}")
    print(f"Positive Commits:      {positive_count} ({positive_count / total_commits:.1%} )")
    print(f"Negative Commits:       {negative_count} ({negative_count / total_commits:.1%} )")
    print(f"Neutral/Mixed Commits:  {neutral_count} ({neutral_count / total_commits:.1%} )")
    print()

    overall_mood = "Neutral/Mixed"
    if positive_count > negative_count and positive_count > neutral_count:
        overall_mood = "✨ Positive ✨"
    elif negative_count > positive_count and negative_count > neutral_count:
        overall_mood = "⛈️ Negative ⛈️"
    elif positive_count == negative_count and positive_count > 0:
        overall_mood = "⚖️ Mixed Feelings ⚖️"
    elif positive_count == 0 and negative_count == 0 and neutral_count > 0:
        overall_mood = "☁️ Calm (Neutral) ☁️"
    else:
        overall_mood = "☁️ Calm (Neutral) ☁️" # Default for cases like all zeros or complex ties

    print(f"Overall Repo Mood: {overall_mood}")
    print("\nRecent Commit Moods:")
    for msg, sentiment in zip(commit_messages, sentiments):
        print(f"- {msg} ({sentiment})")

if __name__ == '__main__':
    main()
