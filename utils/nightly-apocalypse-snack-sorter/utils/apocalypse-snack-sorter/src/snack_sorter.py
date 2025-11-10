import argparse
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "snack_stash.json"
DATE_FORMAT = "%Y-%m-%d"

class SnackStash:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.snacks = self._load_snacks()

    def _load_snacks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode {self.data_file}. Starting with empty stash.")
                    return []
        return []

    def _save_snacks(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.snacks, f, indent=4)

    def add_snack(self, name, quantity, expiry_date_str):
        try:
            datetime.strptime(expiry_date_str, DATE_FORMAT)
        except ValueError:
            print(f"Error: Invalid expiry date format. Please use YYYY-MM-DD (e.g., {datetime.now().strftime(DATE_FORMAT)}).")
            return

        snack = {
            "name": name,
            "quantity": quantity,
            "expiry": expiry_date_str
        }
        self.snacks.append(snack)
        self._save_snacks()
        print(f"Added {quantity}x '{name}' (expires {expiry_date_str}) to your apocalypse stash.")

    def list_snacks(self):
        if not self.snacks:
            print("Your apocalypse snack stash is currently empty. Better stock up!")
            return

        sorted_snacks = sorted(self.snacks, key=lambda s: datetime.strptime(s["expiry"], DATE_FORMAT))

        print("\n--- Your Apocalypse Snack Stash ---")
        for i, snack in enumerate(sorted_snacks):
            expiry_dt = datetime.strptime(snack["expiry"], DATE_FORMAT)
            days_left = (expiry_dt - datetime.now()).days
            status = ""
            if days_left < 0:
                status = " (EXPIRED!) 💀"
            elif days_left <= 30:
                status = f" (Expires in {days_left} days!) ⚠️"
            print(f"{i+1}. {snack['name']} (x{snack['quantity']}) - Expires: {snack['expiry']}{status}")
        print("-----------------------------------\n")

    def get_urgent_snacks(self):
        if not self.snacks:
            print("Your apocalypse snack stash is currently empty. No urgent munchies needed!")
            return

        today = datetime.now()
        urgent_threshold = today + timedelta(days=60) # Snacks expiring in next 60 days

        urgent_list = []
        for snack in self.snacks:
            expiry_dt = datetime.strptime(snack["expiry"], DATE_FORMAT)
            if expiry_dt < urgent_threshold:
                urgent_list.append(snack)

        if not urgent_list:
            print("All your snacks are safe for now. Keep calm and carry on munching!")
            return

        sorted_urgent = sorted(urgent_list, key=lambda s: datetime.strptime(s["expiry"], DATE_FORMAT))

        print("\n--- Urgent Munchies! (Eat These First!) ---")
        for i, snack in enumerate(sorted_urgent):
            expiry_dt = datetime.strptime(snack["expiry"], DATE_FORMAT)
            days_left = (expiry_dt - today).days
            status = ""
            if days_left < 0:
                status = " (EXPIRED!) 💀"
            elif days_left <= 7:
                status = f" (Expires in {days_left} days! DANGER!) 🔥"
            elif days_left <= 30:
                status = f" (Expires in {days_left} days!) ⚠️"
            else:
                status = f" (Expires in {days_left} days)"
            print(f"{i+1}. {snack['name']} (x{snack['quantity']}) - Expires: {snack['expiry']}{status}")
        print("-------------------------------------------\n")


def main():
    parser = argparse.ArgumentParser(
        description="Manage your apocalypse snack stash.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new snack to the stash.")
    add_parser.add_argument("--name", required=True, help="Name of the snack (e.g., 'Survival S'mores').")
    add_parser.add_argument("--quantity", type=int, required=True, help="Number of units (e.g., 3).")
    add_parser.add_argument("--expiry", required=True, help="Expiry date in YYYY-MM-DD format (e.g., '2025-06-15').")

    # List command
    list_parser = subparsers.add_parser("list", help="Display all snacks, sorted by expiry date.")

    # Urgent command
    urgent_parser = subparsers.add_parser("urgent", help="Show snacks that are expiring soonest.")

    args = parser.parse_args()

    stash = SnackStash()

    if args.command == "add":
        stash.add_snack(args.name, args.quantity, args.expiry)
    elif args.command == "list":
        stash.list_snacks()
    elif args.command == "urgent":
        stash.get_urgent_snacks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
