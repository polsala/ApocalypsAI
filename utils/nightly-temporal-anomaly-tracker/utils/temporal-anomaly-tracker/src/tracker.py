import argparse
import json
import os
from datetime import datetime

class TemporalAnomalyTracker:
    def __init__(self, data_file='anomalies.json'):
        self.data_file = data_file
        self.anomalies = self._load_anomalies()

    def _load_anomalies(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # Handle empty or malformed JSON file
                    return []
        return []

    def _save_anomalies(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.anomalies, f, indent=4)

    def add_anomaly(self, description, severity):
        if not (1 <= severity <= 5):
            raise ValueError("Severity must be an integer between 1 and 5.")

        anomaly = {
            'timestamp': datetime.now().isoformat(),
            'description': description,
            'severity': severity
        }
        self.anomalies.append(anomaly)
        self._save_anomalies()
        print(f"Anomaly logged: '{description}' (Severity: {severity})")

    def list_anomalies(self):
        if not self.anomalies:
            print("No temporal anomalies recorded yet. The timeline is suspiciously stable...")
            return

        print("--- Recorded Temporal Anomalies ---")
        for i, anomaly in enumerate(self.anomalies):
            print(f"[{i+1}] Timestamp: {anomaly['timestamp']}")
            print(f"    Description: {anomaly['description']}")
            print(f"    Severity: {anomaly['severity']}/5")
            print("-----------------------------------")

    def export_anomalies(self, output_file):
        with open(output_file, 'w') as f:
            json.dump(self.anomalies, f, indent=4)
        print(f"Anomalies exported to {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Log and track perceived temporal anomalies."
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new temporal anomaly.')
    add_parser.add_argument('description', type=str, help='Description of the anomaly.')
    add_parser.add_argument('--severity', type=int, default=1, choices=range(1, 6),
                            help='Perceived severity (1-5, 5 being most severe).')

    # List command
    list_parser = subparsers.add_parser('list', help='List all recorded anomalies.')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export anomalies to a JSON file.')
    export_parser.add_argument('output_file', type=str, nargs='?', default='anomalies.json',
                               help='Name of the JSON file to export to.')

    args = parser.parse_args()

    tracker = TemporalAnomalyTracker()

    if args.command == 'add':
        try:
            tracker.add_anomaly(args.description, args.severity)
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == 'list':
        tracker.list_anomalies()
    elif args.command == 'export':
        tracker.export_anomalies(args.output_file)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
