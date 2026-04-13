import sys
import json
import re
from collections import defaultdict

# Mock rationale: This script is designed to run on the target host, so we simulate its behavior for testing.
# In a real scenario, this script would read from a file.

def parse_log_content(log_content, error_keywords, warning_keywords):
    parsed_logs = []
    for line in log_content.splitlines():
        level = "INFO"
        message = line

        # Basic keyword matching for level determination
        if any(keyword in line.lower() for keyword in error_keywords):
            level = "ERROR"
        elif any(keyword in line.lower() for keyword in warning_keywords):
            level = "WARNING"

        # Attempt to extract a cleaner message, removing timestamps/hostnames if possible
        # This is a simplified regex and might need adjustment based on actual log formats
        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*? (.*)', line)
        if match:
            message = match.group(1).strip()
        else:
            # Fallback if regex doesn't match, try to remove common prefixes
            message = re.sub(r'^.*?\s+', '', line).strip()

        parsed_logs.append({"level": level, "message": message})
    return parsed_logs

if __name__ == "__main__":
    # In a real Ansible script execution, we'd read from a file.
    # For testing purposes, we'll use stdin or a hardcoded string.
    # Ansible's 'script' module typically passes file content via stdin if not specified.
    # For this standalone example, we'll assume stdin is available or use a placeholder.

    # Placeholder for log content if stdin is not available (e.g., direct execution)
    # In Ansible, this would be the content of the log file.
    log_content_placeholder = ""
    try:
        # Attempt to read from stdin, which Ansible's script module might use
        log_content_placeholder = sys.stdin.read()
    except Exception:
        # If stdin is not available, use a mock content for demonstration
        log_content_placeholder = ""
        log_content_placeholder += "2023-10-27 10:00:01 server1 kernel: [    0.000000] Linux version 5.15.0-87-generic (buildd@lcy02-amd64-030) (gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #97-Ubuntu SMP Mon Oct 2 21:09:21 UTC 2023\n"
        log_content_placeholder += "2023-10-27 10:00:05 server1 systemd[1]: Starting Network Manager...\n"
        log_content_placeholder += "2023-10-27 10:01:10 server1 apt[1234]: E: Failed to fetch http://archive.ubuntu.com/ubuntu/dists/jammy-updates/InRelease 404  Not Found [IP: 91.189.91.39 80]\n"
        log_content_placeholder += "2023-10-27 10:02:00 server1 systemd[1]: Network Manager started.\n"
        log_content_placeholder += "2023-10-27 10:03:00 server1 sshd[5678]: error: PAM: authentication error for root from 192.168.1.100 port 54321 ssh2\n"
        log_content_placeholder += "2023-10-27 10:04:00 server1 systemd[1]: Warning: Disk space critically low on /var/log.\n"
        log_content_placeholder += "2023-10-27 10:05:00 server1 some_app[9012]: INFO: Processing request #12345.\n"
        log_content_placeholder += "2023-10-27 10:06:00 server1 some_app[9012]: WARNING: Deprecation warning for function X, use Y instead.\n"
        log_content_placeholder += "2023-10-27 10:07:00 server1 systemd[1]: Service xyz crashed unexpectedly. Restarting.\n"

    # These would be passed from Ansible vars
    error_keywords = ['error', 'failed', 'critical', 'exception', 'denied']
    warning_keywords = ['warning', 'warn', 'deprecated', 'notice', 'slow']

    parsed_data = parse_log_content(log_content_placeholder, error_keywords, warning_keywords)
    print(json.dumps(parsed_data))
