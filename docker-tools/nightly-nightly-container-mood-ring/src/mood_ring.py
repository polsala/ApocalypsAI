import docker
import sys
import time
from datetime import datetime, timedelta

# Configuration for mood thresholds
CPU_HIGH_THRESHOLD = 70.0  # %
MEM_HIGH_THRESHOLD = 80.0  # %
LOG_WARNING_KEYWORDS = ["warn", "warning", "deprecated"]
LOG_ERROR_KEYWORDS = ["error", "fail", "exception", "critical"]
RECENT_RESTART_WINDOW_SECONDS = 300 # 5 minutes

def get_container_stats(container):
    """Fetches CPU and memory usage for a container."""
    stats = container.stats(stream=False)
    cpu_percent = 0.0
    mem_percent = 0.0

    if 'cpu_stats' in stats and 'precpu_stats' in stats:
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                    stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                       stats['precpu_stats']['system_cpu_usage']
        if system_delta > 0 and cpu_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * \
                          len(stats['cpu_stats']['cpu_usage']['percpu_usage'] or [0]) * 100.0

    if 'memory_stats' in stats and 'usage' in stats['memory_stats'] and 'limit' in stats['memory_stats']:
        mem_usage = stats['memory_stats']['usage']
        mem_limit = stats['memory_stats']['limit']
        if mem_limit > 0:
            mem_percent = (mem_usage / mem_limit) * 100.0

    return cpu_percent, mem_percent

def get_container_logs(container, since_seconds=300):
    """Fetches recent logs and checks for warnings/errors."""
    warnings = []
    errors = []
    log_activity = False
    try:
        # Fetch logs from the last 'since_seconds'
        since_time = datetime.now() - timedelta(seconds=since_seconds)
        logs = container.logs(since=since_time, stream=False).decode('utf-8').splitlines()
        
        if logs:
            log_activity = True

        for line in logs:
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in LOG_ERROR_KEYWORDS):
                errors.append(line)
            elif any(keyword in lower_line for keyword in LOG_WARNING_KEYWORDS):
                warnings.append(line)
    except Exception as e:
        # Handle cases where logs might not be accessible or container is not running
        pass # We'll assume no logs if an error occurs

    return warnings, errors, log_activity

def determine_mood(container_info, cpu_percent, mem_percent, warnings, errors, log_activity):
    """Determines the mood of a container based on its status, stats, and logs."""
    status = container_info.get('Status', '').lower()
    state = container_info.get('State', {})
    
    container_name = container_info.get('Name', 'Unknown')

    if 'running' not in status:
        if state.get('ExitCode') == 0:
            return "Asleep", "Exited gracefully."
        elif state.get('ExitCode') is not None:
            return "Deceased", f"Exited with status {state.get('ExitCode')}."
        return "Asleep", "Not running." # Default for non-running

    # Check for recent restarts
    if state.get('RestartCount', 0) > 0:
        # Check if the last restart was recent
        # This is a bit tricky as docker-py doesn't directly expose last restart time
        # We'll assume if RestartCount > 0 and container is running, it might be fickle
        # A more robust check would involve inspecting 'State.StartedAt' and comparing to 'Created'
        # For simplicity, if restart count > 0, we flag it.
        # Mock rationale: In a real scenario, we'd compare StartedAt with Created or previous StartedAt.
        # For this mock, we'll just use the presence of RestartCount > 0 as an indicator.
        if state.get('RestartCount', 0) > 0:
             return "Fickle", f"Has restarted {state.get('RestartCount')} times."

    if errors:
        return "Distressed", f"Errors detected in logs ({len(errors)}). Example: {errors[0][:50]}..."
    if cpu_percent >= CPU_HIGH_THRESHOLD or mem_percent >= MEM_HIGH_THRESHOLD:
        if cpu_percent >= CPU_HIGH_THRESHOLD and mem_percent >= MEM_HIGH_THRESHOLD:
            return "Anxious", f"High CPU ({cpu_percent:.1f}%) and Memory ({mem_percent:.1f}%) usage."
        elif cpu_percent >= CPU_HIGH_THRESHOLD:
            return "Anxious", f"High CPU usage detected ({cpu_percent:.1f}%)."
        else:
            return "Anxious", f"High Memory usage detected ({mem_percent:.1f}%)."
    if warnings:
        return "Grumpy", f"Warnings detected in logs ({len(warnings)}). Example: {warnings[0][:50]}..."
    
    if cpu_percent < 5.0 and mem_percent < 5.0 and not log_activity:
        return "Bored", "Very low resource usage and no recent log activity."
    
    if log_activity:
        return "Jubilant", "Normal operation, recent activity, no issues."

    return "Serene", "Normal operation, no issues."

def main():
    if len(sys.argv) < 2:
        print("Usage: python mood_ring.py <container_name_or_id> [container_name_or_id...]")
        sys.exit(1)

    client = docker.from_env()

    for container_arg in sys.argv[1:]:
        try:
            container = client.containers.get(container_arg)
            container_info = container.attrs # Get full container info for state
            
            cpu_percent, mem_percent = get_container_stats(container)
            warnings, errors, log_activity = get_container_logs(container)
            
            mood, reason = determine_mood(container_info, cpu_percent, mem_percent, warnings, errors, log_activity)
            print(f"Container {container.name}: {mood} - {reason}")
        except docker.errors.NotFound:
            print(f"Container {container_arg}: Invisible - Container not found.")
        except Exception as e:
            print(f"Container {container_arg}: Confused - Error checking container: {e}")

if __name__ == "__main__":
    main()
