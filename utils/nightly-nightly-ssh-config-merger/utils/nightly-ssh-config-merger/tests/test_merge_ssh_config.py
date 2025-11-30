import pathlib
import tempfile

from utils.nightly-ssh-config-merger.src.merge_ssh_config import merge_ssh_configs


def _write_snippet(dir_path: pathlib.Path, filename: str, content: str) -> pathlib.Path:
    file_path = dir_path / filename
    file_path.write_text(content, encoding="utf-8")
    return file_path


def test_merge_deduplicates_hosts(tmp_path: pathlib.Path) -> None:
    # Setup input directory with two snippets
    input_dir = tmp_path / "snippets"
    input_dir.mkdir()

    # First snippet defines Host alpha and beta
    _write_snippet(
        input_dir,
        "01-first.conf",
        """Host alpha
    HostName alpha.example.com
    User alice

Host beta
    HostName beta.example.com
    User bob
""",
    )

    # Second snippet redefines Host beta (should be ignored) and adds gamma
    _write_snippet(
        input_dir,
        "02-second.conf",
        """Host beta
    HostName beta2.example.com
    User bob2

Host gamma
    HostName gamma.example.com
    User carol
""",
    )

    output_file = tmp_path / "merged_config"

    # Run merger (no external calls, deterministic)
    merge_ssh_configs(input_dir, output_file)

    merged_content = output_file.read_text(encoding="utf-8").splitlines()

    # Expected lines (order preserved, duplicate beta omitted)
    expected = [
        "Host alpha",
        "    HostName alpha.example.com",
        "    User alice",
        "",
        "Host beta",
        "    HostName beta.example.com",
        "    User bob",
        "",
        "Host gamma",
        "    HostName gamma.example.com",
        "    User carol",
    ]

    assert merged_content == expected

# Mock rationale: No network or filesystem side‑effects beyond the temporary directory are performed.
