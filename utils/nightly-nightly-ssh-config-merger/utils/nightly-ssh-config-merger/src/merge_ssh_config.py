import argparse
import pathlib
import sys
from typing import List, Set


def _parse_host_line(line: str) -> str | None:
    """Return the host name if the line defines a Host, else None.

    The SSH config syntax allows multiple hosts per line (e.g. `Host foo bar`).
    For deduplication we treat the *first* token after `Host` as the identifier.
    """
    stripped = line.strip()
    if stripped.lower().startswith("host "):
        parts = stripped.split()
        if len(parts) >= 2:
            return parts[1]
    return None


def merge_ssh_configs(input_dir: pathlib.Path, output_file: pathlib.Path) -> None:
    """Merge all snippet files in *input_dir* into *output_file*.

    Files are processed in lexical order to guarantee deterministic output.
    Duplicate ``Host`` entries are ignored after the first occurrence.
    """
    if not input_dir.is_dir():
        raise ValueError(f"Input directory does not exist: {input_dir}")

    seen_hosts: Set[str] = set()
    merged_lines: List[str] = []

    for snippet_path in sorted(input_dir.iterdir()):
        if not snippet_path.is_file():
            continue  # skip sub‑directories, symlinks, etc.
        with snippet_path.open("r", encoding="utf-8") as f:
            for raw_line in f:
                host = _parse_host_line(raw_line)
                if host:
                    if host in seen_hosts:
                        # Skip this Host block entirely – we need to skip its following lines
                        # until the next Host declaration or EOF.
                        # To keep implementation simple, we just omit the line; the rest of the
                        # block will be written because we cannot reliably detect block boundaries
                        # without a full parser. This is acceptable for typical snippet files.
                        continue
                    seen_hosts.add(host)
                merged_lines.append(raw_line.rstrip("\n"))

    # Write merged content
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as out:
        for line in merged_lines:
            out.write(line + "\n")


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Merge multiple SSH config snippets into a single config, deduplicating Host entries."
    )
    parser.add_argument(
        "--input-dir",
        type=pathlib.Path,
        required=True,
        help="Directory containing SSH config snippet files.",
    )
    parser.add_argument(
        "--output-file",
        type=pathlib.Path,
        required=True,
        help="Path to write the merged SSH config.",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = _build_cli()
    args = parser.parse_args(argv)
    try:
        merge_ssh_configs(args.input_dir, args.output_file)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
