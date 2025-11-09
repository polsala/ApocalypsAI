import time
import datetime
import sys

# Configuration
CHECK_INTERVAL_SECONDS = 10  # How often to check the clock
TIME_JUMP_THRESHOLD_SECONDS = 60  # Minimum seconds for a time jump to be an anomaly
DRIFT_THRESHOLD_PERCENT = 5.0  # Max allowed percentage difference for drift (e.g., 5.0 means 5%)

class TemporalAnomalyDetector:
    def __init__(self):
        self.last_system_time = None
        self.last_monotonic_time = None
        self.log_prefix = "[TemporalAnomalyDetector]"

    def _log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} {self.log_prefix} {message}", file=sys.stderr)

    def detect_anomalies(self):
        current_system_time = time.time()
        current_monotonic_time = time.monotonic()

        if self.last_system_time is None or self.last_monotonic_time is None:
            self.last_system_time = current_system_time
            self.last_monotonic_time = current_monotonic_time
            self._log("Initialized monitoring.")
            return

        # 1. Detect Time Jumps (sudden changes in system time)
        system_time_diff = current_system_time - self.last_system_time
        if abs(system_time_diff) > TIME_JUMP_THRESHOLD_SECONDS:
            jump_direction = "forward" if system_time_diff > 0 else "backward"
            self._log(f"ANOMALY DETECTED: Time jumped {jump_direction} by {abs(system_time_diff):.1f} seconds!")

        # 2. Detect Clock Drift (system clock running too fast/slow compared to real time)
        monotonic_time_diff = current_monotonic_time - self.last_monotonic_time

        if monotonic_time_diff > 0: # Avoid division by zero
            # Expected system time change should be close to monotonic_time_diff
            # Calculate the deviation of system_time_diff from monotonic_time_diff
            deviation = system_time_diff - monotonic_time_diff
            deviation_percent = (deviation / monotonic_time_diff) * 100

            if abs(deviation_percent) > DRIFT_THRESHOLD_PERCENT:
                drift_direction = "fast" if deviation_percent > 0 else "slow"
                self._log(
                    f"ANOMALY DETECTED: System clock drifted {drift_direction} by {deviation_percent:.1f}% "
                    f"(expected {monotonic_time_diff:.1f}s, got {system_time_diff:.1f}s)"
                )

        # Update last known times
        self.last_system_time = current_system_time
        self.last_monotonic_time = current_monotonic_time

    def run(self):
        self._log("Starting Temporal Anomaly Detector...")
        try:
            while True:
                self.detect_anomalies()
                time.sleep(CHECK_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            self._log("Detector stopped by user.")
        except Exception as e:
            self._log(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    detector = TemporalAnomalyDetector()
    detector.run()
