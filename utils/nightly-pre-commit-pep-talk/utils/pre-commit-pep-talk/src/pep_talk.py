import subprocess
import sys

def get_staged_changes_stats():
    """
    Retrieves the number of files, additions, and deletions in the Git staging area.
    Returns a tuple: (num_files, additions, deletions).
    Returns (-1, -1, -1) if an error occurs (e.g., Git not found or command fails).
    """
    try:
        # Use --numstat to get file stats (additions, deletions, filename)
        result = subprocess.run(
            ['git', 'diff', '--cached', '--numstat'],
            capture_output=True,
            text=True,
            check=True
        )
        output_lines = result.stdout.strip().split('\n')

        num_files = 0
        additions = 0
        deletions = 0

        if not output_lines or output_lines == ['']:
            return 0, 0, 0

        for line in output_lines:
            if line:
                parts = line.split('\t')
                if len(parts) == 3:
                    try:
                        # Git uses '-' for binary files in numstat, so handle ValueError
                        additions += int(parts[0])
                        deletions += int(parts[1])
                        num_files += 1
                    except ValueError:
                        # If additions/deletions are not numbers (e.g., binary files),
                        # still count the file but don't add to line counts.
                        num_files += 1
                        pass # Continue processing other lines
        return num_files, additions, deletions
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e.cmd} exited with {e.returncode}. Stderr: {e.stderr.strip()}", file=sys.stderr)
        return -1, -1, -1 # Indicate an error
    except FileNotFoundError:
        print("Error: Git command not found. Is Git installed and in your PATH?", file=sys.stderr)
        return -1, -1, -1 # Indicate an error

def generate_pep_talk(num_files, additions, deletions):
    """
    Generates a whimsical pep talk based on the staged changes.
    """
    total_lines = additions + deletions

    if num_files == -1: # Error state from get_staged_changes_stats
        return "The cosmic energies of Git seem... unavailable. Perhaps the universe is telling you to take a break, or check your `PATH`. Either way, your efforts are still appreciated!"
    elif num_files == 0 and total_lines == 0:
        return "The staging area is quiet tonight. Perhaps your code is already in a state of zen, or patiently awaiting its next grand evolution. Either way, take a moment to breathe!"
    elif num_files == 1 and total_lines < 10:
        return "A focused effort! Even the smallest commit can ripple through the cosmos. Keep that precision sharp, future legend!"
    elif num_files <= 5 and total_lines <= 50:
        return "You're weaving a tapestry of logic, one thoughtful change at a time. The digital loom hums with your progress. Keep up the excellent work!"
    else: # num_files > 5 or total_lines > 50
        return "Behold the architect of digital empires! This commit is a testament to your vision and courage. Remember to review your kingdom before sealing its fate. You've got this!"

def main():
    print("✨ ApocalypsAI Pre-Commit Pep Talk ✨\n")
    num_files, additions, deletions = get_staged_changes_stats()
    pep_talk = generate_pep_talk(num_files, additions, deletions)
    print(pep_talk)

if __name__ == "__main__":
    main()
