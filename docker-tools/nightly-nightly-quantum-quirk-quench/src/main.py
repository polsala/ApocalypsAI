import docker
import os
import re
import time
import logging

logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO').upper(), format='%(asctime)s - %(levelname)s - %(message)s')

QUIRK_PATTERNS_ENV = os.getenv('QUIRK_PATTERNS', 'error|fail|exception|denied')
QUENCH_ACTION_ENV = os.getenv('QUENCH_ACTION', 'restart') # 'restart' or 'notify'
MONITORED_LABELS_ENV = os.getenv('MONITORED_LABELS', 'apocalypsai.monitor=true')

def parse_patterns(patterns_str):
    """Parses a pipe-separated string of patterns into a list of compiled regex objects."""
    return [re.compile(p.strip(), re.IGNORECASE) for p in patterns_str.split('|') if p.strip()]

def parse_labels(labels_str):
    """Parses a comma-separated string of key=value pairs into a dictionary."""
    labels = {}
    for pair in labels_str.split(','):
        if '=' in pair:
            key, value = pair.split('=', 1)
            labels[key.strip()] = value.strip()
    return labels

def detect_quirk(log_line, quirk_patterns):
    """Checks if a log line matches any of the defined quirk patterns."""
    for pattern in quirk_patterns:
        if pattern.search(log_line):
            return True
    return False

def quench_quirk(container, action, log_line):
    """Performs the specified quench action on the container."""
    logging.info(f"Quirk detected in container '{container.name}'. Initiating quench action: {action}")
    if action == 'restart':
        try:
            container.restart()
            logging.info(f"Container '{container.name}' restarted successfully.")
        except docker.errors.APIError as e:
            logging.error(f"Failed to restart container '{container.name}': {e}")
    elif action == 'notify':
        # In a real scenario, this would send a notification (e.g., email, Slack, webhook)
        logging.info(f"Notification: Quirk in '{container.name}' detected. Log snippet: {log_line[:200]}")
    else:
        logging.warning(f"Unknown quench action: {action}. No action taken for '{container.name}'.")

def main():
    client = docker.from_env()
    quirk_patterns = parse_patterns(QUIRK_PATTERNS_ENV)
    quench_action = QUENCH_ACTION_ENV
    monitored_labels = parse_labels(MONITORED_LABELS_ENV)

    if not quirk_patterns:
        logging.warning("No quirk patterns defined. The Quencher will not detect anything.")

    logging.info(f"Quantum Quirk Quencher starting...")
    logging.info(f"Monitoring for patterns: '{QUIRK_PATTERNS_ENV}'")
    logging.info(f"Quench action on detection: '{quench_action}'")
    logging.info(f"Monitoring containers with labels: '{MONITORED_LABELS_ENV}'")

    while True:
        try:
            containers = client.containers.list()
            for container in containers:
                # Check if container has all specified monitored labels
                if not all(container.labels.get(k) == v for k, v in monitored_labels.items()):
                    logging.debug(f"Skipping container '{container.name}' (labels mismatch).")
                    continue # Skip if labels don't match

                logging.debug(f"Monitoring logs for container: {container.name}")
                try:
                    for line_bytes in container.logs(stream=True, follow=True):
                        log_line = line_bytes.decode('utf-8').strip()
                        if log_line:
                            logging.debug(f"[{container.name}] {log_line}")
                            if detect_quirk(log_line, quirk_patterns):
                                logging.warning(f"Quirk detected in '{container.name}': {log_line}")
                                quench_quirk(container, quench_action, log_line)
                                # After a quench action, break from current container's log stream
                                # and re-list containers after a short delay to ensure we don't process old logs
                                # and to pick up any new containers or state changes.
                                break # Exit inner log stream loop
                except docker.errors.APIError as e:
                    logging.error(f"Error streaming logs from '{container.name}': {e}")
                except Exception as e:
                    logging.error(f"Unexpected error processing logs for '{container.name}': {e}")
            time.sleep(5) # Wait before re-listing containers if no logs were streamed or after processing all
        except docker.errors.APIError as e:
            logging.error(f"Docker API error: {e}. Retrying in 10 seconds.")
            time.sleep(10)
        except Exception as e:
            logging.critical(f"An unexpected error occurred in main loop: {e}. Restarting monitoring in 10 seconds.")
            time.sleep(10)

if __name__ == "__main__":
    main()
