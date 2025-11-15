import subprocess
import datetime
from collections import Counter
import os

def get_git_log(repo_path='.'):
    """
    Fetches the git log for the specified repository path.
    Returns a list of commit strings or raises an error if git command fails.
    """
    try:
        # --no-merges to simplify the history for storytelling
        # --pretty=format: hash|author|date|subject
        # --date=iso: standard date format for easy parsing
        # --reverse: chronological order
        command = [
            'git',
            '-C',
            repo_path,
            'log',
            '--no-merges',
            '--pretty=format:"%h|%an|%ad|%s"',
            '--date=iso',
            '--reverse'
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # Each line from git log --pretty=format:"..." will be wrapped in quotes
        return [line.strip('"') for line in result.stdout.strip().split('\n') if line.strip()]
    except subprocess.CalledProcessError as e:
        # Git command failed (e.g., not a git repo, or other git error)
        raise RuntimeError(f"Error fetching git log: {e.stderr.strip()}") from e
    except FileNotFoundError:
        # 'git' command itself was not found
        raise FileNotFoundError("Error: 'git' command not found. Please ensure Git is installed and in your PATH.")

def parse_commit_line(line):
    """
    Parses a single line from the git log output into a dictionary.
    """
    parts = line.split('|', 3) # Split only on the first 3 '|' to keep subject intact
    if len(parts) != 4:
        return None # Malformed line
    
    commit_hash, author, date_str, subject = parts
    try:
        # Parse date, ignoring timezone for simplicity in storytelling
        # fromisoformat handles various ISO 8601 formats, including those with timezone offsets
        # We strip the timezone for consistent datetime objects if needed, but fromisoformat is robust.
        commit_date = datetime.datetime.fromisoformat(date_str.split('+')[0].strip())
    except ValueError:
        return None # Malformed date
    
    return {
        'hash': commit_hash,
        'author': author,
        'date': commit_date,
        'subject': subject
    }

def generate_story(commits):
    """
    Generates a whimsical story from a list of parsed commit dictionaries.
    """
    if not commits:
        return "The repository is a blank scroll, awaiting its first tale. No commits have been made yet."

    first_commit = commits[0]
    last_commit = commits[-1]

    total_commits = len(commits)
    authors = Counter(c['author'] for c in commits)
    most_active_author, _ = authors.most_common(1)[0] if authors else ("a mysterious lone wolf", 0)

    story_parts = []

    # Opening
    story_parts.append(f"In the digital realm, a new saga began on {first_commit['date'].strftime('%Y-%m-%d')}. ")
    story_parts.append(f"The first whisper of creation was '{first_commit['subject']}', penned by the legendary {first_commit['author']}.\n")

    # Journey through time
    if total_commits > 1:
        duration = last_commit['date'] - first_commit['date']
        story_parts.append(f"Over a span of {duration.days} days, {total_commits} magical incantations (commits) were cast upon this project.\n")

        # Key milestones
        milestone_keywords = ['initial', 'feat:', 'refactor:', 'fix:', 'docs:', 'chore:', 'build:']
        milestones = [
            c for c in commits 
            if any(keyword in c['subject'].lower() for keyword in milestone_keywords)
        ]
        if milestones:
            story_parts.append("Many pivotal moments shaped its destiny:\n")
            # Show up to 3 key milestones, prioritizing earlier ones for narrative flow
            for m in milestones[:min(3, len(milestones))]: 
                story_parts.append(f"  - On {m['date'].strftime('%Y-%m-%d')}, {m['author']} declared: '{m['subject']}' ({m['hash']})\n")
            if len(milestones) > 3:
                story_parts.append(f"  ...and {len(milestones) - 3} more tales of transformation unfolded.\n")
        else:
            story_parts.append("The journey was steady, though its major turning points remain subtle whispers in the wind.\n")

    # Contributors
    if len(authors) > 1:
        story_parts.append(f"A fellowship of {len(authors)} brave souls contributed to this epic. ")
        story_parts.append(f"The most prolific among them, with {authors[most_active_author]} contributions, was none other than {most_active_author}!\n")
    elif len(authors) == 1 and total_commits > 1:
        story_parts.append(f"This grand endeavor was meticulously crafted by a single visionary, {most_active_author}, who cast {total_commits} spells upon it.\n")

    # Closing
    story_parts.append(f"The latest chapter, '{last_commit['subject']}', was sealed on {last_commit['date'].strftime('%Y-%m-%d')} by {last_commit['author']}. ")
    story_parts.append("The story continues, ever evolving, ever enchanting...")

    return "".join(story_parts)

def is_git_repository(path):
    """
    Checks if the given path is inside a git repository.
    """
    try:
        subprocess.run(['git', '-C', path, 'rev-parse', '--is-inside-work-tree'], 
                       capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        raise FileNotFoundError("Error: 'git' command not found. Please ensure Git is installed and in your PATH.")

def main():
    try:
        repo_path = os.getcwd()
        
        if not is_git_repository(repo_path):
            print(f"Error: '{repo_path}' is not a git repository.")
            return

        log_lines = get_git_log(repo_path)
        commits = [parse_commit_line(line) for line in log_lines if parse_commit_line(line)]
        story = generate_story(commits)
        print(story)
    except FileNotFoundError as e:
        print(e)
    except RuntimeError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
