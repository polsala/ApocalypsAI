import argparse
import json
import os
from datetime import datetime

DATA_FILE = 'prep_kit_data.json'

def _load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE} is corrupted or empty. Starting with empty data.")
        return {}

def _save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_asset(name, location):
    data = _load_data()
    if name in data:
        print(f"Error: Asset '{name}' already exists. Use 'verify' to update it.")
        return
    data[name] = {
        'location': location,
        'last_verified': datetime.now().isoformat()
    }
    _save_data(data)
    print(f"Asset '{name}' added, located at '{location}'.")

def list_assets():
    data = _load_data()
    if not data:
        print("No digital assets tracked yet. Add some with 'add' command.")
        return
    print("\n--- Digital Doomsday Prep Kit Assets ---")
    for name, details in data.items():
        print(f"  Asset: {name}")
        print(f"    Location: {details.get('location', 'N/A')}")
        print(f"    Last Verified: {details.get('last_verified', 'Never')}")
        print("----------------------------------------")

def verify_asset(name):
    data = _load_data()
    if name not in data:
        print(f"Error: Asset '{name}' not found. Add it first with 'add' command.")
        return
    data[name]['last_verified'] = datetime.now().isoformat()
    _save_data(data)
    print(f"Asset '{name}' verified. Last verified: {data[name]['last_verified']}")

def main():
    parser = argparse.ArgumentParser(description='Digital Doomsday Prep Kit: Track your vital digital assets.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new digital asset.')
    add_parser.add_argument('name', type=str, help='Name of the digital asset.')
    add_parser.add_argument('location', type=str, help='Location where the asset is backed up.')

    # List command
    list_parser = subparsers.add_parser('list', help='List all tracked digital assets.')

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Update the verification timestamp for an asset.')
    verify_parser.add_argument('name', type=str, help='Name of the asset to verify.')

    args = parser.parse_args()

    if args.command == 'add':
        add_asset(args.name, args.location)
    elif args.command == 'list':
        list_assets()
    elif args.command == 'verify':
        verify_asset(args.name)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
