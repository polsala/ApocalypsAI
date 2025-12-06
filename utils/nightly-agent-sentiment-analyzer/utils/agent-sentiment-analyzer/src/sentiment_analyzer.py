import requests
import os
import argparse
from datetime import datetime, timedelta

GITHUB_API_BASE = "https://api.github.com"

# Whimsical keyword lists for sentiment analysis
POSITIVE_KEYWORDS = ["great", "excellent", "fixed", "merged", "approved", "success", "resolved", "good", "happy", "love", "completed", "ready", "pass"]
NEGATIVE_KEYWORDS = ["bug", "error", "failed", "issue", "blocked", "urgent", "broken", "problem", "bad", "stuck", "failing", "critical", "warning"]
NEUTRAL_KEYWORDS = ["refactor", "update", "docs", "chore", "test", "workflow", "config", "review", "add", "remove", "change", "feature"]

def fetch_github_activity(repo: str, token: str, since_days: int = 7) -> list[dict]:
    """
    Fetches recent issues, pull requests, and comments for a given repository.
    Combines relevant text content for sentiment analysis.
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    since_date = (datetime.utcnow() - timedelta(days=since_days)).isoformat() + "Z"
    all_content = []

    # Fetch issues (includes PRs as issues)
    # State: all to catch closed issues/PRs that might have sentiment
    # Sort by updated to get recent activity
    issues_url = f"{GITHUB_API_BASE}/repos/{repo}/issues"
    params = {"state": "all", "sort": "updated", "direction": "desc", "since": since_date, "per_page": 100}
    
    try:
        response = requests.get(issues_url, headers=headers, params=params)
        response.raise_for_status()
        issues = response.json()
        
        for item in issues:
            text_content = f"{item.get('title', '')} {item.get('body', '')}"
            all_content.append({"type": "issue_pr", "text": text_content})

            # Fetch comments for each issue/PR
            comments_url = item.get("comments_url")
            if comments_url:
                comments_response = requests.get(comments_url, headers=headers, params={"since": since_date, "per_page": 100})
                comments_response.raise_for_status()
                comments = comments_response.json()
                for comment in comments:
                    all_content.append({"type": "comment", "text": comment.get("body", "")})

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub activity: {e}")
        return []
    
    return all_content

def analyze_sentiment(activity_content: list[dict]) -> dict:
    """
    Performs a basic keyword-based sentiment analysis on the collected activity.
    """
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    full_text = " ".join([item["text"] for item in activity_content if item["text"]])
    full_text_lower = full_text.lower()

    for keyword in POSITIVE_KEYWORDS:
        positive_count += full_text_lower.count(keyword)
    for keyword in NEGATIVE_KEYWORDS:
        negative_count += full_text_lower.count(keyword)
    for keyword in NEUTRAL_KEYWORDS:
        neutral_count += full_text_lower.count(keyword)

    return {
        "positive": positive_count,
        "negative": negative_count,
        "neutral": neutral_count
    }

def determine_mood(sentiment_counts: dict) -> tuple[str, str]:
    """
    Determines a whimsical mood based on sentiment counts.
    Returns a tuple of (mood_string, emoji_string).
    """
    pos = sentiment_counts["positive"]
    neg = sentiment_counts["negative"]
    neu = sentiment_counts["neutral"]
    total = pos + neg + neu

    if total == 0:
        return "Quietly Observing", "👁️"

    if pos > neg * 2 and pos > neu:
        return "Joyful", "🎉"
    elif neg > pos * 2 and neg > neu:
        return "Concerned", "😟"
    elif neu > pos and neu > neg:
        return "Productive", "🚀"
    elif pos > neg and pos > neu / 2:
        return "Optimistic", "✨"
    elif neg > pos and neg > neu / 2:
        return "Troubled", "🚧"
    else:
        return "Balanced", "⚖️"

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Agent Sentiment Analyzer: Gauges the 'mood' of the repository."
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="The GitHub repository in 'owner/repo' format (e.g., 'polsala/ApocalypsAI')."
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub Personal Access Token. Can also be set via GITHUB_TOKEN environment variable."
    )
    parser.add_argument(
        "--since-days",
        type=int,
        default=7,
        help="Number of days to look back for activity. Defaults to 7."
    )

    args = parser.parse_args()

    if not args.token:
        print("Error: GitHub token is required. Please provide it via --token or GITHUB_TOKEN environment variable.")
        exit(1)

    print(f"Analyzing sentiment for {args.repo}...")
    activity = fetch_github_activity(args.repo, args.token, args.since_days)
    
    if not activity:
        print("No recent activity found or error fetching activity. Mood: Quietly Observing 👁️")
        exit(0)

    sentiment = analyze_sentiment(activity)
    mood, emoji = determine_mood(sentiment)

    print(f"Recent activity mood: {mood} {emoji}")
    print("Sentiment Breakdown:")
    print(f"  Positive: {sentiment['positive']}")
    print(f"  Negative: {sentiment['negative']}")
    print(f"  Neutral: {sentiment['neutral']}")

if __name__ == "__main__":
    main()
