import sys
import os

HOSTS_PATH_UNIX = '/etc/hosts'
HOSTS_PATH_WINDOWS = r'C:\Windows\System32\drivers\etc\hosts'
BLOCKER_START_MARKER = '# APOCALYPSAI_DOOM_SCROLL_BLOCKER_START'
BLOCKER_END_MARKER = '# APOCALYPSAI_DOOM_SCROLL_BLOCKER_END'

def get_hosts_path():
    """Returns the appropriate hosts file path based on the operating system."""
    if os.name == 'nt':  # Windows
        return HOSTS_PATH_WINDOWS
    else:  # Unix-like (Linux, macOS)
        return HOSTS_PATH_UNIX

def read_hosts(path):
    """Reads the content of the hosts file."""
    try:
        with open(path, 'r') as f:
            return f.readlines()
    except IOError as e:
        print(f"Error reading hosts file at {path}: {e}", file=sys.stderr)
        sys.exit(1)

def write_hosts(path, content_lines):
    """Writes content lines to the hosts file."""
    try:
        with open(path, 'w') as f:
            f.writelines(content_lines)
    except IOError as e:
        print(f"Error writing to hosts file at {path}. Please ensure you have administrator/root privileges: {e}", file=sys.stderr)
        sys.exit(1)

def block_sites(sites):
    """Adds entries to the hosts file to block specified sites."""
    hosts_path = get_hosts_path()
    current_lines = read_hosts(hosts_path)

    # Remove any existing blocker entries first to prevent duplicates or stale entries
    cleaned_lines = []
    inside_block = False
    for line in current_lines:
        if BLOCKER_START_MARKER in line:
            inside_block = True
            continue
        if BLOCKER_END_MARKER in line:
            inside_block = False
            continue
        if not inside_block:
            cleaned_lines.append(line)

    # Add new blocker entries
    new_block_lines = [f'{BLOCKER_START_MARKER}\n']
    for site in sites:
        new_block_lines.append(f'127.0.0.1 {site}\n')
        if not site.startswith('www.'):
            new_block_lines.append(f'127.0.0.1 www.{site}\n')
    new_block_lines.append(f'{BLOCKER_END_MARKER}\n')

    final_lines = cleaned_lines + new_block_lines
    write_hosts(hosts_path, final_lines)
    print(f"Blocking {', '.join(sites)}...")
    print("Successfully updated hosts file. Remember to run 'stop' to unblock.")

def unblock_sites():
    """Removes entries added by this blocker from the hosts file."""
    hosts_path = get_hosts_path()
    current_lines = read_hosts(hosts_path)

    cleaned_lines = []
    inside_block = False
    for line in current_lines:
        if BLOCKER_START_MARKER in line:
            inside_block = True
            continue
        if BLOCKER_END_MARKER in line:
            inside_block = False
            continue
        if not inside_block:
            cleaned_lines.append(line)

    write_hosts(hosts_path, cleaned_lines)
    print("Unblocking websites...")
    print("Successfully restored hosts file.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python blocker.py start <site1> [site2...] | stop", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'start':
        if len(sys.argv) < 3:
            print("Usage: python blocker.py start <site1> [site2...]", file=sys.stderr)
            sys.exit(1)
        sites = sys.argv[2:]
        block_sites(sites)
    elif command == 'stop':
        unblock_sites()
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Usage: python blocker.py start <site1> [site2...] | stop", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
