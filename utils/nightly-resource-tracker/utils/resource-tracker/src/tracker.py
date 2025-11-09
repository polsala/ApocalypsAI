import argparse
import json
import sys
from pathlib import Path
from typing import Dict


class ResourceTracker:
    """Simple JSON‑backed resource tracker.

    The JSON schema is a flat mapping of resource name → integer amount.
    """

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self._resources: Dict[str, int] = {}
        self._load()

    # ---------------------------------------------------------------------
    # Persistence helpers
    # ---------------------------------------------------------------------
    def _load(self) -> None:
        if self.storage_path.is_file():
            try:
                with self.storage_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                # Ensure all values are ints
                self._resources = {k: int(v) for k, v in data.items()}
            except (json.JSONDecodeError, ValueError) as exc:
                raise RuntimeError(f"Corrupted storage file: {self.storage_path}") from exc
        else:
            self._resources = {}

    def _save(self) -> None:
        # Ensure parent directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with self.storage_path.open("w", encoding="utf-8") as f:
            json.dump(self._resources, f, indent=2, sort_keys=True)

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def add_resource(self, name: str, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Amount to add must be positive")
        self._resources[name] = self._resources.get(name, 0) + amount
        self._save()

    def consume_resource(self, name: str, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Amount to consume must be positive")
        if name not in self._resources:
            raise KeyError(f"Resource '{name}' not found")
        if self._resources[name] < amount:
            raise ValueError(
                f"Not enough of '{name}' to consume: have {self._resources[name]}, need {amount}"
            )
        self._resources[name] -= amount
        if self._resources[name] == 0:
            del self._resources[name]
        self._save()

    def list_resources(self) -> Dict[str, int]:
        return dict(self._resources)

    # ---------------------------------------------------------------------
    # CLI helpers
    # ---------------------------------------------------------------------
    @staticmethod
    def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            prog="resource-tracker",
            description="Track post‑apocalypse supplies in a local JSON file.",
        )
        parser.add_argument(
            "--storage",
            type=Path,
            default=Path(__file__).resolve().parent.parent / "resources.json",
            help="Path to the JSON storage file (default: utils/resource-tracker/resources.json)",
        )
        subparsers = parser.add_subparsers(dest="command", required=True)

        # add command
        add_parser = subparsers.add_parser("add", help="Add a quantity to a resource")
        add_parser.add_argument("--name", required=True, help="Resource name")
        add_parser.add_argument("--amount", type=int, required=True, help="Amount to add (positive integer)")

        # consume command
        cons_parser = subparsers.add_parser("consume", help="Consume a quantity from a resource")
        cons_parser.add_argument("--name", required=True, help="Resource name")
        cons_parser.add_argument("--amount", type=int, required=True, help="Amount to consume (positive integer)")

        # list command
        subparsers.add_parser("list", help="List all tracked resources")

        return parser.parse_args(argv)

    @classmethod
    def main(cls, argv: list[str] | None = None) -> int:
        args = cls._parse_args(argv)
        tracker = cls(args.storage)

        try:
            if args.command == "add":
                tracker.add_resource(args.name, args.amount)
                print(f"Added {args.amount} of '{args.name}'.")
            elif args.command == "consume":
                tracker.consume_resource(args.name, args.amount)
                print(f"Consumed {args.amount} of '{args.name}'.")
            elif args.command == "list":
                resources = tracker.list_resources()
                if not resources:
                    print("No resources tracked.")
                else:
                    for name, amt in sorted(resources.items()):
                        print(f"{name}: {amt}")
            else:
                raise RuntimeError("Unknown command")
        except (ValueError, KeyError, RuntimeError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        return 0


if __name__ == "__main__":
    sys.exit(ResourceTracker.main())
