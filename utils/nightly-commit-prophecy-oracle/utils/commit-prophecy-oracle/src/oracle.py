import subprocess
import sys
import os

def get_commit_messages(repo_path="."):
    """
    Retrieves the last N commit messages from a Git repository.
    # Mock rationale: subprocess.run is mocked to avoid actual git calls
    # and ensure deterministic test results.
    """
    try:
        # Limit to last 10 commits for performance and relevance
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', '--oneline', '-n', '10', '--pretty=format:%s'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e}", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("Git command not found. Is Git installed and in your PATH?", file=sys.stderr)
        return []

def divine_prophecy(commit_messages):
    """
    Analyzes commit messages and generates a whimsical prophecy.
    """
    if not commit_messages:
        return "The scrolls are blank. No recent commits to divine the future. Perhaps the stars are aligning for a grand new beginning, or perhaps... nothing at all."

    keywords = {
        "fix": 0, "bug": 0, "error": 0,
        "feat": 0, "feature": 0, "add": 0,
        "refactor": 0, "clean": 0, "improve": 0,
        "test": 0, "ci": 0, "docs": 0,
        "breaking": 0, "major": 0, "deprecate": 0,
        "chore": 0, "config": 0, "build": 0
    }

    for msg in commit_messages:
        lower_msg = msg.lower()
        for keyword in keywords:
            if keyword in lower_msg:
                keywords[keyword] += 1

    total_commits = len(commit_messages)

    # Prophecy logic based on keyword counts
    if keywords["breaking"] > 0 or keywords["major"] > 0:
        return "A great upheaval is foretold! The very foundations of your realm are shifting. Prepare for a period of intense reconstruction and adaptation."
    elif keywords["fix"] + keywords["bug"] + keywords["error"] >= total_commits / 2:
        return "The spirits of past transgressions linger. Many wounds have been mended, but vigilance is key lest old demons resurface. Seek the root cause, not just the symptom."
    elif keywords["feat"] + keywords["feature"] + keywords["add"] >= total_commits / 2:
        return "The winds of innovation blow strong! New lands are being charted, and bountiful harvests of functionality await. Ensure your maps are clear and your compass true."
    elif keywords["refactor"] + keywords["clean"] + keywords["improve"] >= total_commits / 2:
        return "The ancient texts speak of a great cleansing. The pathways are being cleared, and the structures refined. Expect greater clarity and efficiency in the days to come."
    elif keywords["test"] + keywords["ci"] + keywords["docs"] >= total_commits / 2:
        return "The scribes and guardians are diligent! The scrolls are being meticulously documented, and the defenses strengthened. A period of stability and trust is at hand."
    elif keywords["chore"] + keywords["config"] + keywords["build"] >= total_commits / 2:
        return "The gears of the machine are being oiled and adjusted. Though unseen, these efforts ensure the smooth operation of your grand design. Small adjustments yield great stability."
    else:
        return "The cosmic energies are balanced, yet subtle. The future holds a tapestry woven with threads of routine and minor adjustments. Keep a watchful eye for emerging patterns."

def main():
    repo_path = "."
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]

    if not os.path.isdir(os.path.join(repo_path, '.git')):
        print(f"Error: '{repo_path}' is not a Git repository.", file=sys.stderr)
        sys.exit(1)

    print(f"Consulting the Commit Prophecy Oracle for repository: {os.path.abspath(repo_path)}\n")
    messages = get_commit_messages(repo_path)
    prophecy = divine_prophecy(messages)
    print(prophecy)

if __name__ == "__main__":
    main()
