import platform
import os
import sys

# Unique marker to identify lines added by this utility
BLOCKER_MARKER = '# APOCALYPSAI_DOOM_BLOCKER'

def get_hosts_file_path():
    """Returns the path to the hosts file based on the operating system."""
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32", "drivers", "etc", "hosts")
    else: # Linux, macOS, etc.
        return "/etc/hosts"

def block_sites(sites):
    """Adds entries to the hosts file to block specified sites."""
    hosts_path = get_hosts_file_path()
    try:
        with open(hosts_path, 'r+') as f:
            content = f.readlines()
            f.seek(0) # Go to the beginning of the file

            # Filter out existing blocker entries to prevent duplicates
            filtered_content = [line for line in content if BLOCKER_MARKER not in line]
            f.writelines(filtered_content)

            # Add new entries
            blocked_lines = []
            for site in sites:
                if site.strip():
                    blocked_lines.append(f"127.0.0.1 {site.strip()} {BLOCKER_MARKER}\n")
            f.writelines(blocked_lines)
            f.truncate() # Remove any remaining old content if new content is shorter

        print(f"Successfully blocked: {', '.join(sites)}")
        print("You might need to flush your DNS cache for changes to take effect.")
    except PermissionError:
        print(f"Error: Permission denied. Please run this script with administrative/root privileges (e.g., sudo).", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Hosts file not found at {hosts_path}.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def unblock_sites():
    """Removes entries added by this utility from the hosts file."""
    hosts_path = get_hosts_file_path()
    try:
        with open(hosts_path, 'r+') as f:
            lines = f.readlines()
            f.seek(0) # Go to the beginning of the file
            # Write back only lines that do NOT contain our blocker marker
            for line in lines:
                if BLOCKER_MARKER not in line:
                    f.write(line)
            f.truncate() # Remove any remaining old content
        print("Successfully unblocked all sites previously blocked by ApocalypsAI Doom Blocker.")
        print("You might need to flush your DNS cache for changes to take effect.")
    except PermissionError:
        print(f"Error: Permission denied. Please run this script with administrative/root privileges (e.g., sudo).", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Hosts file not found at {hosts_path}.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python blocker.py <block|unblock> [--sites <comma-separated-sites>]", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "block":
        if "--sites" not in sys.argv:
            print("Error: '--sites' argument is required for 'block' command.", file=sys.stderr)
            sys.exit(1)
        try:
            sites_index = sys.argv.index("--sites")
            sites_str = sys.argv[sites_index + 1]
            sites = [s.strip() for s in sites_str.split(',') if s.strip()]
            if not sites:
                print("Error: No sites provided for blocking.", file=sys.stderr)
                sys.exit(1)
            block_sites(sites)
        except (ValueError, IndexError):
            print("Error: Invalid '--sites' argument. Please provide a comma-separated list of sites.", file=sys.stderr)
            sys.exit(1)
    elif command == "unblock":
        unblock_sites()
    else:
        print(f"Unknown command: {command}. Use 'block' or 'unblock'.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
