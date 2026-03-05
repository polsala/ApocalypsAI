import argparse
import os
import datetime
from pathlib import Path
from rich.console import Console
from rich.text import Text

def find_old_files(path: Path, days_old: int) -> list[tuple[Path, datetime.datetime]]:
    """
    Finds files older than a specified number of days in a given path.
    """
    old_files = []
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_old)

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = Path(root) / file_name
            try:
                # Mock rationale: os.path.getmtime is mocked in tests to control file modification times.
                mod_timestamp = os.path.getmtime(file_path)
                mod_datetime = datetime.datetime.fromtimestamp(mod_timestamp)
                if mod_datetime < cutoff_date:
                    old_files.append((file_path, mod_datetime))
            except OSError:
                # Handle cases where file might be inaccessible or disappear during scan
                pass
    return old_files

def find_empty_dirs(path: Path) -> list[Path]:
    """
    Finds empty directories in a given path.
    """
    empty_dirs = []
    for root, dirs, files in os.walk(path):
        # Mock rationale: os.walk is mocked in tests to simulate directory structures.
        if not dirs and not files: # If no subdirectories and no files
            # Ensure it's not the root path itself if it's empty
            if Path(root) != path:
                empty_dirs.append(Path(root))
    return empty_dirs

def generate_report(
    console: Console,
    scan_path: Path,
    days_old: int,
    old_files: list[tuple[Path, datetime.datetime]],
    empty_dirs: list[Path]
):
    """
    Generates a whimsical report of digital dust bunnies.
    """
    console.print(Text("\n✨ Digital Dust Bunny Report ✨", style="bold magenta"))

    if old_files:
        console.print(f"\nFound {len(old_files)} ancient scrolls (files older than {days_old} days):", style="yellow")
        for file_path, mod_datetime in old_files:
            console.print(f"  - {file_path} (Last modified: {mod_datetime.strftime('%Y-%m-%d')})", style="dim")
    else:
        console.print(f"\nNo ancient scrolls (files older than {days_old} days) found. Your archives are spry!", style="green")

    if empty_dirs:
        console.print(f"\nFound {len(empty_dirs)} desolate caverns (empty directories):", style="yellow")
        for dir_path in empty_dirs:
            console.print(f"  - {dir_path}", style="dim")
    else:
        console.print("\nNo desolate caverns (empty directories) found. Your digital landscape is lush!", style="green")

    total_bunnies = len(old_files) + len(empty_dirs)
    console.print(f"\nTotal Digital Dust Bunnies: {total_bunnies}", style="bold cyan")
    if total_bunnies > 0:
        console.print("Consider tidying up to prevent a data-apocalypse!", style="bold red")
    else:
        console.print("Your digital realm is impeccably clean! Well done, survivor!", style="bold green")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Digital Dust Bunny Sweeper: Identifies old files and empty directories."
    )
    parser.add_argument(
        "--path",
        type=Path,
        required=True,
        help="The absolute path to the directory to scan."
    )
    parser.add_argument(
        "--days_old",
        type=int,
        default=90,
        help="Files older than this many days will be reported. Default is 90."
    )
    parser.add_argument(
        "--no_empty_dirs",
        action="store_true",
        help="Skip scanning for empty directories."
    )

    args = parser.parse_args()
    console = Console()

    console.print(Text(f"⚠️ Initiating Digital Dust Bunny Sweep in {args.path}... ⚠️", style="bold blue"))

    old_files = []
    if args.days_old > 0:
        console.print(f"\nScanning for files older than {args.days_old} days...", style="blue")
        old_files = find_old_files(args.path, args.days_old)

    empty_dirs = []
    if not args.no_empty_dirs:
        console.print("\nScanning for empty directories...", style="blue")
        empty_dirs = find_empty_dirs(args.path)

    generate_report(console, args.path, args.days_old, old_files, empty_dirs)

if __name__ == "__main__":
    main()
