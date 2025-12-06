import argparse
import sys

def calculate_vibe(open_issues: int, failed_workflows_24h: int, days_since_last_commit: int) -> tuple[str, str, float]:
    """
    Calculates the repository's 'vibe' based on provided metrics.

    Args:
        open_issues: Number of currently open issues.
        failed_workflows_24h: Number of workflow runs that failed in the last 24 hours.
        days_since_last_commit: Days since the last commit to the main branch.

    Returns:
        A tuple containing (mood_string, emoji, vibe_score).
    """

    # Configuration for scoring weights and thresholds
    WEIGHT_OPEN_ISSUES = 0.5
    WEIGHT_FAILED_WORKFLOWS = 2.0
    WEIGHT_DAYS_SINCE_COMMIT = 0.2

    THRESHOLD_SERENE = 5.0
    THRESHOLD_GLOOMY = 15.0
    THRESHOLD_CHAOTIC = 30.0

    vibe_score = (
        (open_issues * WEIGHT_OPEN_ISSUES) +
        (failed_workflows_24h * WEIGHT_FAILED_WORKFLOWS) +
        (days_since_last_commit * WEIGHT_DAYS_SINCE_COMMIT)
    )

    if vibe_score < THRESHOLD_SERENE:
        return "Serenely Doomed", "🌿", vibe_score
    elif vibe_score < THRESHOLD_GLOOMY:
        return "Mildly Gloomy", "🌧️", vibe_score
    elif vibe_score < THRESHOLD_CHAOTIC:
        return "Chaotic Neutral", "🌀", vibe_score
    else:
        return "Imminent Collapse", "💥", vibe_score

def main():
    parser = argparse.ArgumentParser(
        description="Calculate the ApocalypsAI repository's vibe based on health metrics."
    )
    parser.add_argument(
        "--open-issues",
        type=int,
        required=True,
        help="Number of currently open issues."
    )
    parser.add_argument(
        "--failed-workflows-24h",
        type=int,
        required=True,
        help="Number of workflow runs that failed in the last 24 hours."
    )
    parser.add_argument(
        "--days-since-last-commit",
        type=int,
        required=True,
        help="Days since the last commit to the main branch."
    )

    args = parser.parse_args()

    mood, emoji, score = calculate_vibe(
        args.open_issues,
        args.failed_workflows_24h,
        args.days_since_last_commit
    )

    print(f"Repository Vibe: {mood} {emoji} (Score: {score:.1f})")

if __name__ == "__main__":
    main()
