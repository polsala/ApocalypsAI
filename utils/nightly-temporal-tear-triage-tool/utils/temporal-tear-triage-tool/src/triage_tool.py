import argparse
import json
import os
from typing import List, Dict, Any

class TriageTool:
    def __init__(self, data_file: str = "anomalies.json"):
        self.data_file = data_file
        self.anomalies: List[Dict[str, Any]] = self._load_anomalies()
        self._next_id = max([a['id'] for a in self.anomalies]) + 1 if self.anomalies else 1

    def _load_anomalies(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []

    def _save_anomalies(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.anomalies, f, indent=4)

    def add_anomaly(self, description: str, urgency: int, impact: int) -> Dict[str, Any]:
        if not (1 <= urgency <= 5 and 1 <= impact <= 5):
            raise ValueError("Urgency and Impact must be between 1 and 5.")

        anomaly = {
            "id": self._next_id,
            "description": description,
            "urgency": urgency,
            "impact": impact,
            "triage_score": urgency * impact,
            "completed": False
        }
        self.anomalies.append(anomaly)
        self._next_id += 1
        self._save_anomalies()
        return anomaly

    def list_anomalies(self, include_completed: bool = False) -> List[Dict[str, Any]]:
        active_anomalies = [a for a in self.anomalies if include_completed or not a['completed']]
        # Sort by triage_score (desc), then urgency (desc), then id (asc) for stable sort
        active_anomalies.sort(key=lambda x: (x['triage_score'], x['urgency'], -x['id']), reverse=True)
        return active_anomalies

    def complete_anomaly(self, anomaly_id: int) -> bool:
        for anomaly in self.anomalies:
            if anomaly['id'] == anomaly_id and not anomaly['completed']:
                anomaly['completed'] = True
                self._save_anomalies()
                return True
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Temporal Tear Triage Tool: Prioritize your temporal anomalies.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new temporal anomaly.")
    add_parser.add_argument("description", type=str, help="Description of the anomaly.")
    add_parser.add_argument("--urgency", type=int, required=True, choices=range(1, 6),
                            help="Urgency level (1-5, 5 being most urgent).")
    add_parser.add_argument("--impact", type=int, required=True, choices=range(1, 6),
                            help="Impact level (1-5, 5 being highest impact).")

    # List command
    list_parser = subparsers.add_parser("list", help="List active temporal anomalies by priority.")
    list_parser.add_argument("--all", action="store_true", help="Include completed anomalies in the list.")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a temporal anomaly as complete.")
    complete_parser.add_argument("id", type=int, help="ID of the anomaly to mark as complete.")

    args = parser.parse_args()

    tool = TriageTool()

    if args.command == "add":
        try:
            anomaly = tool.add_anomaly(args.description, args.urgency, args.impact)
            print(f"Anomaly '{anomaly['description']}' (ID: {anomaly['id']}) added with Triage Score: {anomaly['triage_score']}.")
        except ValueError as e:
            print(f"Error: {e}")
            exit(1)
    elif args.command == "list":
        anomalies = tool.list_anomalies(args.all)
        if not anomalies:
            print("No active temporal anomalies found. The timeline is stable... for now.")
            return

        print("\n--- Active Temporal Anomalies ---")
        for anomaly in anomalies:
            status = "[COMPLETED]" if anomaly['completed'] else ""
            print(f"ID: {anomaly['id']:<3} | Score: {anomaly['triage_score']:<2} (U:{anomaly['urgency']} I:{anomaly['impact']}) | {anomaly['description']} {status}")
        print("---------------------------------\n")
    elif args.command == "complete":
        if tool.complete_anomaly(args.id):
            print(f"Anomaly ID {args.id} marked as complete. One step closer to timeline stability!")
        else:
            print(f"Anomaly ID {args.id} not found or already completed.")
            exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
