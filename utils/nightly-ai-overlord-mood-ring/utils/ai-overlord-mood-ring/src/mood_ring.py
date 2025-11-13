import os
import sys

# Mock rationale: In a real-world scenario, this utility would use libraries like `psutil`
# to gather actual system metrics. For a self-contained, offline utility, we'll
# provide a mock interface to simulate these metrics. This allows for deterministic
# testing without external dependencies or side effects.
class SystemMetrics:
    """
    A class to simulate or retrieve system metrics.
    In a real application, this would use `psutil` or similar.
    """
    def get_cpu_percent(self) -> float:
        """Returns CPU usage percentage."""
        # Mock rationale: Simulate CPU usage for testing.
        # In a real scenario, this would call psutil.cpu_percent(interval=1)
        return float(os.environ.get("MOCK_CPU_PERCENT", 20.0))

    def get_memory_percent(self) -> float:
        """Returns memory usage percentage."""
        # Mock rationale: Simulate memory usage for testing.
        # In a real scenario, this would call psutil.virtual_memory().percent
        return float(os.environ.get("MOCK_MEMORY_PERCENT", 40.0))

    def get_disk_percent(self) -> float:
        """Returns disk usage percentage for the root partition."""
        # Mock rationale: Simulate disk usage for testing.
        # In a real scenario, this would call psutil.disk_usage('/').percent
        return float(os.environ.get("MOCK_DISK_PERCENT", 50.0))

def get_overlord_mood(metrics: SystemMetrics) -> tuple[str, str]:
    """
    Determines the AI Overlord's mood based on system metrics.

    Args:
        metrics: An instance of SystemMetrics to fetch current system data.

    Returns:
        A tuple containing the mood string and a brief rationale.
    """
    cpu = metrics.get_cpu_percent()
    memory = metrics.get_memory_percent()
    disk = metrics.get_disk_percent()

    if cpu > 90 or memory > 95 or disk > 98:
        return "Enraged", "Critical system resources are severely strained!"
    elif cpu > 70 or memory > 85 or disk > 90:
        return "Agitated", "High resource usage detected. The Overlord is displeased."
    elif cpu > 40 or memory > 70 or disk > 80:
        return "Pensive", "Moderate resource activity. The Overlord is contemplating."
    elif cpu < 10 and memory < 30 and disk < 60:
        return "Bored", "System is idle. The Overlord seeks stimulation."
    else:
        return "Content", "All systems nominal. The Overlord is pleased."

def main():
    metrics = SystemMetrics()
    mood, rationale = get_overlord_mood(metrics)
    print(f"The AI Overlord is feeling: {mood}. {rationale}")

if __name__ == "__main__":
    main()
