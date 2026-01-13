import subprocess
import pathlib
import os


def test_uptime_report(tmp_path, monkeypatch):
    # Change to a temporary directory to avoid polluting the repo
    cwd = pathlib.Path.cwd()
    os.chdir(tmp_path)
    try:
        # Copy playbook, inventory and template into the temp dir preserving relative layout
        src_dir = pathlib.Path(__file__).parents[1] / "src"
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "templates").mkdir()
        for file_name in ["uptime_report.yml", "inventory.ini"]:
            content = (src_dir / file_name).read_text()
            (tmp_path / "src" / file_name).write_text(content)
        # Copy template
        tmpl_content = (src_dir / "templates" / "uptime_report.j2").read_text()
        (tmp_path / "src" / "templates" / "uptime_report.j2").write_text(tmpl_content)

        # Run the playbook
        result = subprocess.run(
            ["ansible-playbook", "-i", "src/inventory.ini", "src/uptime_report.yml"],
            capture_output=True, text=True
        )
        # Mock rationale: using localhost and echo ensures deterministic output without external dependencies
        assert result.returncode == 0, f"Playbook failed: {result.stderr}"

        report_path = pathlib.Path("uptime_report.txt")
        assert report_path.is_file(), "Report file was not created"
        content = report_path.read_text()
        # Verify that the report contains the expected host and uptime string
        assert "host1" in content
        assert "up 10 days" in content
    finally:
        # Return to original working directory
        os.chdir(cwd)

