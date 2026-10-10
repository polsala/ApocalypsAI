#!/usr/bin/env python3

import random
import datetime
import os
import sys

# Configuration (these will be templated by Ansible or passed as env vars)
WHISPERS_FILE = os.environ.get('WHISPERS_FILE', '/opt/whisperwind_relay/whispers.txt')
LOG_FILE = os.environ.get('LOG_FILE', '/var/log/whisperwind_relay.log')

def get_random_whisper(whispers_path):
    """Reads a random whisper from the specified file."""
    try:
        with open(whispers_path, 'r') as f:
            whispers = [line.strip() for line in f if line.strip()]
        if whispers:
            return random.choice(whispers)
        else:
            return "The wind carries no words today."
    except FileNotFoundError:
        return f"Whispers file not found at {whispers_path}. Silence prevails."
    except Exception as e:
        return f"Error reading whispers: {e}"

def log_whisper(log_path, whisper):
    """Appends the timestamped whisper to the log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Whisperwind: {whisper}\n"
    try:
        # Ensure the log directory exists
        log_dir = os.path.dirname(log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        with open(log_path, 'a') as f:
            f.write(log_entry)
        print(f"Logged: {whisper}")
    except Exception as e:
        print(f"Error logging whisper to {log_path}: {e}", file=sys.stderr)

if __name__ == "__main__":
    whisper = get_random_whisper(WHISPERS_FILE)
    log_whisper(LOG_FILE, whisper)
