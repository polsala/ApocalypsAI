import os
import subprocess
import tempfile
import shutil
import pathlib

def test_ssh_key_rotator():
    # Setup temporary working directory
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = pathlib.Path(__file__).resolve().parents[2]
        src_dir = repo_root / "ansible-playbooks" / "nightly-ansible-ssh-key-rotator" / "src"
        # Copy playbook and inventory to temp dir
        shutil.copytree(src_dir, pathlib.Path(tmpdir) / "src")
        # Run ansible-playbook
        result = subprocess.run(
            ["ansible-playbook", "-i", "src/inventory.ini", "src/playbook.yml"],
            cwd=tmpdir,
            capture_output=True,
            text=True,
        )
        # Mock rationale: we expect ansible to exit with 0
        assert result.returncode == 0, f"Ansible failed: {result.stderr}"
        # Verify key file exists
        key_path = pathlib.Path(tmpdir) / "src" / "ssh_keys" / "id_rsa"
        assert key_path.is_file(), "Private key was not created"
