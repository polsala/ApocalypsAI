import argparse
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

ASSETS_FILE = "assets.json"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

class AssetAuditor:
    def __init__(self, assets_file: str = ASSETS_FILE):
        self.assets_file = assets_file
        self.assets: List[Dict[str, Any]] = []
        self._load_assets()

    def _load_assets(self) -> None:
        if os.path.exists(self.assets_file):
            with open(self.assets_file, 'r') as f:
                self.assets = json.load(f)
        else:
            self.assets = []

    def _save_assets(self) -> None:
        with open(self.assets_file, 'w') as f:
            json.dump(self.assets, f, indent=4)

    def init_store(self) -> None:
        if not os.path.exists(self.assets_file):
            self._save_assets()
            print(f"Initialized new asset store at '{self.assets_file}'.")
        else:
            print(f"Asset store '{self.assets_file}' already exists. No action taken.")

    def add_asset(self, name: str, asset_type: str, path_or_url: str, description: str, backup_location: str) -> None:
        if any(asset['name'] == name for asset in self.assets):
            print(f"Error: Asset with name '{name}' already exists.")
            return

        now = datetime.now().strftime(DATE_FORMAT)
        new_asset = {
            "name": name,
            "type": asset_type,
            "path_or_url": path_or_url,
            "description": description,
            "backup_location": backup_location,
            "last_audited": now,
        }
        self.assets.append(new_asset)
        self._save_assets()
        print(f"Asset '{name}' added successfully.")

    def update_asset(self, name: str, **kwargs: str) -> None:
        found = False
        for asset in self.assets:
            if asset['name'] == name:
                for key, value in kwargs.items():
                    if key.startswith("new_"):
                        original_key = key[4:] # Remove 'new_' prefix
                        if original_key in asset:
                            asset[original_key] = value
                        else:
                            print(f"Warning: Field '{original_key}' not found for asset '{name}'.")
                    else:
                        print(f"Warning: Invalid update field '{key}'. Use 'new_<field_name>'.")
                asset['last_audited'] = datetime.now().strftime(DATE_FORMAT) # Mark as audited on update
                found = True
                break
        if found:
            self._save_assets()
            print(f"Asset '{name}' updated successfully.")
        else:
            print(f"Error: Asset with name '{name}' not found.")

    def list_assets(self) -> None:
        if not self.assets:
            print("No assets found.")
            return

        for asset in self.assets:
            print("-" * 30)
            for key, value in asset.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        print("-" * 30)

    def audit_asset(self, name: str) -> None:
        found = False
        for asset in self.assets:
            if asset['name'] == name:
                asset['last_audited'] = datetime.now().strftime(DATE_FORMAT)
                found = True
                break
        if found:
            self._save_assets()
            print(f"Asset '{name}' marked as audited successfully.")
        else:
            print(f"Error: Asset with name '{name}' not found.")

    def find_stale_assets(self, days: int) -> List[Dict[str, Any]]:
        stale_threshold = datetime.now() - timedelta(days=days)
        stale_assets = []
        for asset in self.assets:
            try:
                last_audited_dt = datetime.strptime(asset['last_audited'], DATE_FORMAT)
                if last_audited_dt < stale_threshold:
                    stale_assets.append(asset)
            except ValueError:
                print(f"Warning: Could not parse 'last_audited' for asset '{asset['name']}'. Skipping.")
        
        if stale_assets:
            print(f"Assets not audited in the last {days} days:")
            for asset in stale_assets:
                print(f"- {asset['name']} (Last Audited: {asset['last_audited']})")
        else:
            print(f"All assets audited within the last {days} days.")
        return stale_assets


def main():
    parser = argparse.ArgumentParser(description="Apocalypse Asset Auditor: Track your crucial digital assets.")
    parser.add_argument("--assets-file", default=ASSETS_FILE, help=f"Path to the assets JSON file (default: {ASSETS_FILE})")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new empty asset store.")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new digital asset.")
    add_parser.add_argument("--name", required=True, help="Unique name for the asset.")
    add_parser.add_argument("--type", required=True, help="Type of asset (e.g., Document, Software License, URL).")
    add_parser.add_argument("--path-or-url", required=True, help="File path, folder path, or URL of the asset.")
    add_parser.add_argument("--description", required=True, help="Brief description of the asset.")
    add_parser.add_argument("--backup-location", required=True, help="Where the asset is backed up.")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing asset.")
    update_parser.add_argument("--name", required=True, help="Name of the asset to update.")
    update_parser.add_argument("--new-name", help="New unique name for the asset.")
    update_parser.add_argument("--new-type", help="New type for the asset.")
    update_parser.add_argument("--new-path-or-url", help="New path/URL for the asset.")
    update_parser.add_argument("--new-description", help="New description for the asset.")
    update_parser.add_argument("--new-backup-location", help="New backup location for the asset.")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tracked assets.")

    # Audit command
    audit_parser = subparsers.add_parser("audit", help="Mark an asset as recently audited.")
    audit_parser.add_argument("--name", required=True, help="Name of the asset to mark as audited.")

    # Stale command
    stale_parser = subparsers.add_parser("stale", help="Find assets not audited in the last N days.")
    stale_parser.add_argument("--days", type=int, default=30, help="Number of days to consider an asset 'stale' (default: 30).")

    args = parser.parse_args()

    auditor = AssetAuditor(args.assets_file)

    if args.command == "init":
        auditor.init_store()
    elif args.command == "add":
        auditor.add_asset(args.name, args.type, args.path_or_url, args.description, args.backup_location)
    elif args.command == "update":
        update_kwargs = {k: v for k, v in vars(args).items() if k.startswith("new_") and v is not None}
        if not update_kwargs:
            print("Error: No update fields provided. Use --new-<field_name>.")
        else:
            auditor.update_asset(args.name, **update_kwargs)
    elif args.command == "list":
        auditor.list_assets()
    elif args.command == "audit":
        auditor.audit_asset(args.name)
    elif args.command == "stale":
        auditor.find_stale_assets(args.days)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
