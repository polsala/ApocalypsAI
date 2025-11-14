import subprocess
import json
import os
import argparse
from collections import Counter

def get_commit_messages(repo_path, num_commits=50):
    """
    Fetches the last N commit messages from a Git repository.
    """
    try:
        # Use --no-merges to avoid merge commit messages which often add noise
        # Use --pretty=format:%s to get only the subject line
        command = ['git', '-C', repo_path, 'log', f'-n{num_commits}', '--no-merges', '--pretty=format:%s']
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Handle cases where git log returns empty string or only whitespace
        output = result.stdout.strip()
        if not output:
            return []
        return output.split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        print(f"Stderr: {e.stderr}")
        return []
    except FileNotFoundError:
        print("Git command not found. Please ensure Git is installed and in your PATH.")
        return []

def analyze_mood(messages):
    """
    Analyzes commit messages for keywords to determine the repository's mood.
    """
    if not messages:
        return "Mysterious (No recent commits)", "The repository is a blank slate, or perhaps just very quiet."

    mood_scores = Counter()

    # Define keywords for different moods
    mood_keywords = {
        "Joyful/Optimistic": ["feat", "add", "implement", "happy", "yay", "improve", "enhance", "refactor", "new", "release"],
        "Stressed/Urgent": ["fix", "urgent", "hotfix", "bug", "error", "broken", "fail", "panic", "deadline", "critical", "ASAP", "revert"],
        "Calm/Steady": ["docs", "chore", "style", "test", "ci", "build", "update", "config", "refactor"],
        "Confused/Uncertain": ["question", "investigate", "explore", "unsure", "maybe", "wip", "experiment", "draft"]
    }

    # Specific phrases/emojis that might strongly indicate a mood
    override_keywords = {
        "Stressed/Urgent": ["fix(critical)", "urgent fix", "hotfix for", "revert"],
        "Joyful/Optimistic": ["🎉", "✨", "🚀", "🥳", "initial commit"], # Initial commit can be optimistic
    }

    for msg in messages:
        lower_msg = msg.lower()
        
        # Check for override keywords first (higher weight)
        for mood, keywords in override_keywords.items():
            for keyword in keywords:
                if keyword in lower_msg:
                    mood_scores[mood] += 3 # Higher score for overrides

        # Check for general keywords
        for mood, keywords in mood_keywords.items():
            for keyword in keywords:
                if keyword in lower_msg:
                    # Simple heuristic: 'fix' without 'bug' might be neutral/positive, with 'bug' it's urgent.
                    if keyword == "fix" and "bug" in lower_msg:
                        mood_scores["Stressed/Urgent"] += 1
                    elif keyword == "refactor" and any(pos_word in lower_msg for pos_word in ["improve", "clean", "better"]):
                        mood_scores["Joyful/Optimistic"] += 1
                    else:
                        mood_scores[mood] += 1

    if not mood_scores:
        return "Neutral/Routine", "The repository hums along with routine tasks, a steady rhythm."

    # Determine the dominant mood
    dominant_mood = mood_scores.most_common(1)[0][0]
    
    # Generate a whimsical summary based on the dominant mood
    summaries = {
        "Joyful/Optimistic": "A vibrant glow! The repository is buzzing with positive energy and exciting new developments.",
        "Stressed/Urgent": "A flickering red light! There are critical issues demanding immediate attention. Brace for impact!",
        "Calm/Steady": "A serene blue hue. The repository is in a state of peaceful maintenance and steady progress.",
        "Confused/Uncertain": "A swirling grey mist. The path forward is unclear, with much exploration and experimentation underway.",
        "Neutral/Routine": "A gentle hum. The repository is performing routine tasks, a steady rhythm of development.",
        "Mysterious (No recent commits)": "The repository is a blank slate, or perhaps just very quiet. Its mood remains a mystery."
    }
    
    return dominant_mood, summaries.get(dominant_mood, summaries["Neutral/Routine"])

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Repo Mood Ring: Gaze into the Git log and discern the repository's current emotional state."
    )
    parser.add_argument(
        "repo_path",
        type=str,
        help="Path to the Git repository (e.g., '.')."
    )
    parser.add_argument(
        "--num-commits",
        type=int,
        default=50,
        help="Number of recent commits to analyze (default: 50)."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.repo_path):
        print(f"Error: Repository path '{args.repo_path}' does not exist or is not a directory.")
        exit(1)
    
    # Check if it's a Git repository by looking for the .git directory
    if not os.path.isdir(os.path.join(args.repo_path, '.git')):
        print(f"Error: '{args.repo_path}' is not a Git repository.")
        exit(1)

    messages = get_commit_messages(args.repo_path, args.num_commits)
    mood, summary = analyze_mood(messages)

    print(json.dumps({
        "mood": mood,
        "summary": summary,
        "analyzed_commits": len(messages)
    }, indent=2))

if __name__ == "__main__":
    main()
