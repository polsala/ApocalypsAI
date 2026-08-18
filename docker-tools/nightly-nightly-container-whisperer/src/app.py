import os
import time
import docker
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class ContainerWhisperer:
    def __init__(self, container_names_str, polling_interval):
        self.container_names = [name.strip() for name in container_names_str.split(',') if name.strip()]
        self.polling_interval = int(polling_interval)
        self.docker_client = self._get_docker_client()

        if not self.container_names:
            logging.warning("No container names specified. The Whisperer will be silent.")

    def _get_docker_client(self):
        # Mock rationale: In a real scenario, this connects to the Docker daemon.
        # For testing, we might mock `docker.from_env()` to return a mock client.
        try:
            return docker.from_env()
        except Exception as e:
            logging.error(f"Could not connect to Docker daemon: {e}. Ensure /var/run/docker.sock is mounted.")
            # Exit or handle gracefully if Docker client is essential
            raise

    def _get_container_by_name(self, name):
        try:
            return self.docker_client.containers.get(name)
        except docker.errors.NotFound:
            logging.warning(f"Container '{name}' not found. Skipping.")
            return None
        except Exception as e:
            logging.error(f"Error getting container '{name}': {e}")
            return None

    def _analyze_logs(self, container_name, logs):
        error_count = 0
        warning_count = 0
        info_count = 0

        for line in logs.splitlines():
            line_str = line.decode('utf-8', errors='ignore').upper()
            if "ERROR" in line_str or "EXCEPTION" in line_str or "FAILED" in line_str:
                error_count += 1
            elif "WARN" in line_str:
                warning_count += 1
            elif "INFO" in line_str:
                info_count += 1
        
        return error_count, warning_count, info_count

    def _determine_mood(self, error_count, warning_count, info_count):
        if error_count > 0:
            return "Grumpy 😠", f"Multiple errors ({error_count}) indicate it's having a very bad day."
        elif warning_count > 0:
            return "Anxious 😨", f"A few warnings ({warning_count}) suggest it's a bit stressed."
        elif info_count > 0:
            return "Chatty 🗣️", f"It's actively communicating, with {info_count} info messages."
        else:
            return "Serene 😌", "All is calm in its digital garden."

    def _get_new_logs(self, container):
        # Mock rationale: `container.logs(stream=True, since=...)` is hard to mock deterministically.
        # For this whimsical utility, fetching a limited tail is sufficient for "mood" detection.
        try:
            # Fetch the last 100 lines for a quick check
            logs_bytes = container.logs(tail=100)
            return logs_bytes
        except Exception as e:
            logging.error(f"Error fetching logs for container '{container.name}': {e}")
            return b""

    def whisper_loop(self):
        logging.info("🌙 Nightly Container Whisperer is listening... 🌙")
        while True:
            logging.info("-" * 40)
            logging.info("🌙 Nightly Container Whisperer Report 🌙")
            logging.info("-" * 40)
            
            if not self.container_names:
                logging.info("No containers to whisper to. Zzz...")

            for name in self.container_names:
                container = self._get_container_by_name(name)
                if container:
                    logs = self._get_new_logs(container)
                    error_c, warning_c, info_c = self._analyze_logs(name, logs)
                    mood, description = self._determine_mood(error_c, warning_c, info_c)
                    logging.info(f"Container '{name}': Feeling {mood}. {description}")
            
            logging.info("-" * 40)
            time.sleep(self.polling_interval)

if __name__ == "__main__":
    container_names_env = os.getenv("CONTAINER_NAMES", "")
    polling_interval_env = os.getenv("POLLING_INTERVAL_SECONDS", "60")

    if not container_names_env:
        logging.error("Environment variable CONTAINER_NAMES is not set. Please specify containers to monitor.")
        exit(1)

    try:
        whisperer = ContainerWhisperer(container_names_env, polling_interval_env)
        whisperer.whisper_loop()
    except Exception as e:
        logging.error(f"Whisperer encountered a critical error: {e}")
        exit(1)
