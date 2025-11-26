import os
import time
import argparse
from datetime import datetime, timedelta

class AnomalyDetector:
    def __init__(self, threshold_days=30):
        self.threshold_seconds = threshold_days * 24 * 60 * 60
        self.current_time = time.time()
        self.anomalies = []

    def _get_timestamps(self, path):
        try:
            stat = os.stat(path)
            return stat.st_mtime, stat.st_ctime
        except OSError:
            return None, None

    def _report_anomaly(self, anomaly_type, path, details):
        self.anomalies.append({
            'type': anomaly_type,
            'path': path,
            'details': details
        })
        print(f"[ANOMALY] {anomaly_type}: {path} - {details}")

    def scan_directory(self, root_path):
        if not os.path.isdir(root_path):
            print(f"Error: Path '{root_path}' is not a valid directory.")
            return

        print(f"Scanning '{root_path}' for chrono-sync anomalies (threshold: {self.threshold_seconds / (24*60*60):.0f} days)...")

        for dirpath, dirnames, filenames in os.walk(root_path):
            dir_mtime, _ = self._get_timestamps(dirpath)
            if dir_mtime is None:
                continue

            # Check for future-dated directory
            if dir_mtime > self.current_time + 60: # Allow 60s grace for clock sync
                self._report_anomaly(
                    "Future-Dated Directory",
                    dirpath,
                    f"Modified: {datetime.fromtimestamp(dir_mtime)} (Current: {datetime.fromtimestamp(self.current_time)})")

            for name in filenames:
                file_path = os.path.join(dirpath, name)
                file_mtime, file_ctime = self._get_timestamps(file_path)

                if file_mtime is None:
                    continue

                # 1. Future-Dated Files
                if file_mtime > self.current_time + 60: # Allow 60s grace for clock sync
                    self._report_anomaly(
                        "Future-Dated File",
                        file_path,
                        f"Modified: {datetime.fromtimestamp(file_mtime)} (Current: {datetime.fromtimestamp(self.current_time)})")

                # 2. Files Much Older Than Parent Directory
                if file_mtime < dir_mtime - self.threshold_seconds:
                    self._report_anomaly(
                        "File Much Older Than Parent",
                        file_path,
                        f"File Modified: {datetime.fromtimestamp(file_mtime)}, Parent Modified: {datetime.fromtimestamp(dir_mtime)}")

                # 3. Files Much Newer Than Parent Directory
                if file_mtime > dir_mtime + self.threshold_seconds:
                    self._report_anomaly(
                        "File Much Newer Than Parent",
                        file_path,
                        f"File Modified: {datetime.fromtimestamp(file_mtime)}, Parent Modified: {datetime.fromtimestamp(dir_mtime)}")
        
        if not self.anomalies:
            print("No chrono-sync anomalies detected. Your filesystem is temporally sound!")
        else:
            print(f"\nDetected {len(self.anomalies)} chrono-sync anomalies.")


def main():
    parser = argparse.ArgumentParser(
        description="Detects chrono-sync anomalies (timestamp inconsistencies) in your filesystem."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for anomalies."
    )
    parser.add_argument(
        "--threshold-days",
        type=int,
        default=30,
        help="Number of days for 'much older/newer' threshold (default: 30)."
    )

    args = parser.parse_args()

    detector = AnomalyDetector(threshold_days=args.threshold_days)
    detector.scan_directory(args.path)


if __name__ == "__main__":
    main()
