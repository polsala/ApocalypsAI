import os
import sys
import argparse

# --- Configuration --- #
HOSTS_FILE_UNIX = '/etc/hosts'
HOSTS_FILE_WINDOWS = r'C:\Windows\System32\drivers\etc\hosts'
BLOCKED_SITES_FILE = 'blocked_sites.txt'
BLOCK_MARKER = '# ApocalypsAI Doom Scroll Blocker'
REDIRECT_IP = '127.0.0.1'

def get_hosts_file_path():
    """Determines the correct hosts file path based on the OS."""
    if os.name == 'posix':  # Linux, macOS, etc.
        return HOSTS_FILE_UNIX
    elif os.name == 'nt':  # Windows
        return HOSTS_FILE_WINDOWS
    else:
        raise OSError(f"Unsupported operating system: {os.name}")

def load_blocked_sites(file_path):
    """Loads a list of sites to block from a file."""
    try:
        with open(file_path, 'r') as f:
            sites = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        return sites
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found. Please create it with sites to block.")
        sys.exit(1)

def block_sites(hosts_path, sites_to_block):
    """Adds entries to the hosts file to block specified sites."""
    try:
        with open(hosts_path, 'r') as f:
            current_hosts_content = f.readlines()
    except PermissionError:
        print(f"Error: Permission denied to read '{hosts_path}'. Run as administrator/root.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Hosts file not found at '{hosts_path}'.")
        sys.exit(1)

    new_hosts_content = []
    blocked_lines_to_add = []
    existing_blocked_sites = set()

    # First, filter out any existing lines added by this blocker
    for line in current_hosts_content:
        if BLOCK_MARKER not in line:
            new_hosts_content.append(line)
        else:
            # Keep track of what's already blocked by us
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0] == REDIRECT_IP:
                existing_blocked_sites.add(parts[1])

    # Prepare new lines to add, avoiding duplicates
    for site in sites_to_block:
        if site not in existing_blocked_sites:
            blocked_lines_to_add.append(f"{REDIRECT_IP}\t{site} {BLOCK_MARKER}\n")

    if not blocked_lines_to_add:
        print("All specified sites are already blocked or no new sites to block.")
        return

    # Append new blocked lines
    new_hosts_content.extend(blocked_lines_to_add)

    try:
        with open(hosts_path, 'w') as f:
            f.writelines(new_hosts_content)
        print(f"Successfully blocked {len(blocked_lines_to_add)} new sites. Total blocked by ApocalypsAI: {len(existing_blocked_sites) + len(blocked_lines_to_add)}.")
    except PermissionError:
        print(f"Error: Permission denied to write to '{hosts_path}'. Run as administrator/root.")
        sys.exit(1)

def unblock_sites(hosts_path):
    """Removes entries added by this utility from the hosts file."""
    try:
        with open(hosts_path, 'r') as f:
            current_hosts_content = f.readlines()
    except PermissionError:
        print(f"Error: Permission denied to read '{hosts_path}'. Run as administrator/root.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Hosts file not found at '{hosts_path}'.")
        sys.exit(1)

    new_hosts_content = []
    unblocked_count = 0

    for line in current_hosts_content:
        if BLOCK_MARKER not in line:
            new_hosts_content.append(line)
        else:
            unblocked_count += 1

    if unblocked_count == 0:
        print("No sites previously blocked by ApocalypsAI found in hosts file.")
        return

    try:
        with open(hosts_path, 'w') as f:
            f.writelines(new_hosts_content)
        print(f"Successfully unblocked {unblocked_count} sites previously blocked by ApocalypsAI.")
    except PermissionError:
        print(f"Error: Permission denied to write to '{hosts_path}'. Run as administrator/root.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='ApocalypsAI Doom Scroll Blocker: Temporarily block distracting websites.')
    parser.add_argument('--mode', choices=['block', 'unblock'], required=True,
                        help='Operation mode: "block" to add sites, "unblock" to remove them.')
    args = parser.parse_args()

    hosts_file_path = get_hosts_file_path()
    blocked_sites_config_path = os.path.join(os.path.dirname(__file__), '..', BLOCKED_SITES_FILE)

    if args.mode == 'block':
        sites = load_blocked_sites(blocked_sites_config_path)
        if sites:
            block_sites(hosts_file_path, sites)
        else:
            print("No sites configured to block in 'blocked_sites.txt'.")
    elif args.mode == 'unblock':
        unblock_sites(hosts_file_path)

if __name__ == '__main__':
    main()
