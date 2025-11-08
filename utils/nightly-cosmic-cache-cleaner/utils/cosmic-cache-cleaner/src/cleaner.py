import subprocess
import shutil
import os

def _run_command(command, description):
    """Helper to run a shell command and print status."""
    print(f"  Running: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        output = result.stdout.strip()
        if output:
            print(f"  Output:\n{output}\n")
        print(f"Successfully {description}.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error {description}: {e}")
        if e.stdout:
            print(f"  Stdout:\n{e.stdout.strip()}\n")
        if e.stderr:
            print(f"  Stderr:\n{e.stderr.strip()}\n")
        return False
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found for {description}. Is it installed and in PATH?")
        return False

def _check_command_exists(command_name):
    """Checks if a command exists in the system's PATH."""
    return shutil.which(command_name) is not None

def clear_pip_cache():
    """Clears the pip cache."""
    print("\nChecking for pip...")
    if not _check_command_exists('pip'):
        print("  Not found. Skipping pip cache.")
        return
    print("  Found.")
    print("Clearing pip cache...")
    _run_command(['pip', 'cache', 'purge'], 'cleared pip cache')

def clear_npm_cache():
    """Clears the npm cache."""
    print("\nChecking for npm...")
    if not _check_command_exists('npm'):
        print("  Not found. Skipping npm cache.")
        return
    print("  Found.")
    print("Clearing npm cache...")
    _run_command(['npm', 'cache', 'clean', '--force'], 'cleared npm cache')

def clear_yarn_cache():
    """Clears the yarn cache."""
    print("\nChecking for yarn...")
    if not _check_command_exists('yarn'):
        print("  Not found. Skipping yarn cache.")
        return
    print("  Found.")
    print("Clearing yarn cache...")
    _run_command(['yarn', 'cache', 'clean'], 'cleared yarn cache')

def clear_go_mod_cache():
    """Clears the Go module download cache."""
    print("\nChecking for go...")
    if not _check_command_exists('go'):
        print("  Not found. Skipping go module cache.")
        return
    print("  Found.")
    print("Clearing go module cache...")
    _run_command(['go', 'clean', '-modcache'], 'cleared go module cache')

def main():
    print("--- Cosmic Cache Cleaner Initiated ---")
    clear_pip_cache()
    clear_npm_cache()
    clear_yarn_cache()
    clear_go_mod_cache()
    print("\n--- Cosmic Cache Cleaner Complete ---")

if __name__ == '__main__':
    main()
