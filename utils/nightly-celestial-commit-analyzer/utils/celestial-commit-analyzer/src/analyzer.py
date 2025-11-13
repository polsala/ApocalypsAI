import sys
import re

# Whimsical lexicon for sentiment analysis
POSITIVE_WORDS = {"feat", "fix", "add", "update", "refactor", "improve", "enhance", "resolve", "clean", "pass", "good", "great", "excellent", "perfect", "success"}
NEGATIVE_WORDS = {"bug", "error", "fail", "break", "remove", "revert", "bad", "issue", "problem", "broken"}

CONVENTIONAL_COMMIT_PATTERN = re.compile(r"^(feat|fix|build|chore|ci|docs|perf|refactor|revert|style|test)(\([\w.-]+\))?:\s(.+)$")

def analyze_commit(message: str) -> dict:
    """Analyzes a single commit message for conventional commit adherence and sentiment."""
    result = {
        "message": message,
        "is_conventional": False,
        "type": None,
        "scope": None,
        "subject": None,
        "sentiment_score": 0,
        "celestial_alignment_score": 0,
        "insights": []
    }

    # 1. Conventional Commit Check
    match = CONVENTIONAL_COMMIT_PATTERN.match(message)
    if match:
        result["is_conventional"] = True
        result["type"] = match.group(1)
        result["scope"] = match.group(2)[1:-1] if match.group(2) else None
        result["subject"] = match.group(3)
        result["insights"].append("✨ Conventional Commit structure detected. Well-aligned!")
    else:
        result["insights"].append("🌌 This commit drifts from conventional patterns. Consider a more structured approach.")

    # 2. Simple Sentiment Analysis
    words = set(re.findall(r'\b\w+\b', message.lower()))
    positive_count = len(words.intersection(POSITIVE_WORDS))
    negative_count = len(words.intersection(NEGATIVE_WORDS))
    
    sentiment_score = positive_count - negative_count
    result["sentiment_score"] = sentiment_score

    if sentiment_score > 0:
        result["insights"].append(f"🌟 Positive cosmic energy detected ({positive_count} positive words).")
    elif sentiment_score < 0:
        result["insights"].append(f"🌑 A shadow of negativity looms ({abs(negative_count)} negative words).")
    else:
        result["insights"].append("💫 Neutral cosmic vibrations.")

    # 3. Celestial Alignment Score (0-100)
    score = 0
    if result["is_conventional"]:
        score += 50 # Base for conventional structure
        if result["type"] in ["feat", "fix"]:
            score += 20 # More points for core types
        if result["scope"]:
            score += 10 # Points for having a scope
    
    # Adjust based on sentiment
    if sentiment_score > 0:
        score += min(sentiment_score * 5, 20) # Max 20 points for sentiment
    elif sentiment_score < 0:
        score -= min(abs(sentiment_score) * 5, 20) # Max -20 points for sentiment

    result["celestial_alignment_score"] = max(0, min(100, score)) # Keep score between 0 and 100

    return result

def generate_summary(analysis_results: list[dict]) -> str:
    """Generates a Markdown summary of the analysis results."""
    total_commits = len(analysis_results)
    if total_commits == 0:
        return "No commit messages provided for celestial analysis."

    conventional_count = sum(1 for r in analysis_results if r["is_conventional"])
    avg_alignment_score = sum(r["celestial_alignment_score"] for r in analysis_results) / total_commits

    summary_lines = [
        "# 🌌 Celestial Commit Analysis Report 🌠",
        "",
        f"A total of **{total_commits}** commit messages were scanned for cosmic alignment.",
        "",
        f"## 📊 Overall Cosmic Harmony",
        f"- **Conventional Commits**: {conventional_count} / {total_commits} ({conventional_count/total_commits:.1%})",
        f"- **Average Celestial Alignment Score**: {avg_alignment_score:.2f}/100",
        "",
        "## 🔭 Individual Commit Insights",
        ""
    ]

    for i, result in enumerate(analysis_results):
        alignment_emoji = "🌟" if result["celestial_alignment_score"] >= 80 else ("✨" if result["celestial_alignment_score"] >= 50 else "🌑")
        summary_lines.append(f"### Commit {i+1}: `{result['message']}` {alignment_emoji}")
        summary_lines.append(f"- **Alignment Score**: {result['celestial_alignment_score']}/100")
        summary_lines.append(f"- **Conventional**: {'✅' if result['is_conventional'] else '❌'}")
        if result["type"]:
            summary_lines.append(f"- **Type**: `{result['type']}`")
        if result["scope"]:
            summary_lines.append(f"- **Scope**: `{result['scope']}`")
        summary_lines.append("- **Cosmic Wisdom**:")
        for insight in result["insights"]:
            summary_lines.append(f"  - {insight}")
        summary_lines.append("")

    return "\n".join(summary_lines)

def main():
    """Main entry point for the utility."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python analyzer.py [file_path]")
        print("Reads commit messages line by line from the specified file or from stdin if no file is provided.")
        print("Outputs a Markdown report of the celestial analysis.")
        sys.exit(0)

    commit_messages = []
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                commit_messages = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'", file=sys.stderr)
            sys.exit(1)
    else:
        print("Enter commit messages (one per line). Press Ctrl+D (Unix) or Ctrl+Z then Enter (Windows) to finish:", file=sys.stderr)
        for line in sys.stdin:
            stripped_line = line.strip()
            if stripped_line:
                commit_messages.append(stripped_line)

    if not commit_messages:
        print("No commit messages provided.", file=sys.stderr)
        sys.exit(2) # No-op exit code

    analysis_results = [analyze_commit(msg) for msg in commit_messages]
    report = generate_summary(analysis_results)
    print(report)

if __name__ == "__main__":
    main()
