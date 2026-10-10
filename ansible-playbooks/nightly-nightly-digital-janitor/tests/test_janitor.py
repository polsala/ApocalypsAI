import os
import tempfile
import shutil
import datetime
from datetime import timedelta
from unittest import TestCase, mock
import subprocess
import yaml

class TestDigitalJanitor(TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.tmp_path = os.path.join(self.test_dir, "mock_tmp")
        self.var_tmp_path = os.path.join(self.test_dir, "mock_var_tmp")
        self.log_path = os.path.join(self.test_dir, "mock_var_log")
        self.archive_path = os.path.join(self.log_path, "archive")

        os.makedirs(self.tmp_path)
        os.makedirs(self.var_tmp_path)
        os.makedirs(self.log_path)

        # Define playbook path
        self.playbook_path = os.path.join(os.path.dirname(__file__), '../src/janitor.yml')
        self.inventory_path = os.path.join(os.path.dirname(__file__), '../src/inventory.ini')

        # Mock rationale: Create mock files with different ages for cleanup tests.
        # These files simulate the state of a system before cleanup.
        # Old files should be removed, new files should remain.
        
        # Create old temporary files (older than 7 days)
        old_date = datetime.datetime.now() - timedelta(days=10)
        for i in range(3):
            file_path = os.path.join(self.tmp_path, f"old_temp_file_{i}.txt")
            with open(file_path, "w") as f:
                f.write("old temp content")
            os.utime(file_path, (old_date.timestamp(), old_date.timestamp()))

        # Create new temporary files (younger than 7 days)
        new_date = datetime.datetime.now() - timedelta(days=1)
        for i in range(2):
            file_path = os.path.join(self.tmp_path, f"new_temp_file_{i}.txt")
            with open(file_path, "w") as f:
                f.write("new temp content")
            os.utime(file_path, (new_date.timestamp(), new_date.timestamp()))

        # Create old var_tmp files
        for i in range(2):
            file_path = os.path.join(self.var_tmp_path, f"old_var_tmp_file_{i}.txt")
            with open(file_path, "w") as f:
                f.write("old var_tmp content")
            os.utime(file_path, (old_date.timestamp(), old_date.timestamp()))

        # Create new var_tmp files
        for i in range(1):
            file_path = os.path.join(self.var_tmp_path, f"new_var_tmp_file_{i}.txt")
            with open(file_path, "w") as f:
                f.write("new var_tmp content")
            os.utime(file_path, (new_date.timestamp(), new_date.timestamp()))

        # Create old log files (older than 30 days)
        old_log_date = datetime.datetime.now() - timedelta(days=40)
        for i in range(2):
            file_path = os.path.join(self.log_path, f"old_log_{i}.log")
            with open(file_path, "w") as f:
                f.write("old log content")
            os.utime(file_path, (old_log_date.timestamp(), old_log_date.timestamp()))

        # Create new log files (younger than 30 days)
        new_log_date = datetime.datetime.now() - timedelta(days=5)
        for i in range(1):
            file_path = os.path.join(self.log_path, f"new_log_{i}.log")
            with open(file_path, "w") as f:
                f.write("new log content")
            os.utime(file_path, (new_log_date.timestamp(), new_log_date.timestamp()))
        
        # Create a non-log file in log_path, should not be archived
        file_path = os.path.join(self.log_path, "important.txt")
        with open(file_path, "w") as f:
            f.write("important text")
        os.utime(file_path, (old_log_date.timestamp(), old_log_date.timestamp()))

        # Create broken symlinks
        broken_link_path = os.path.join(self.tmp_path, "broken_link")
        os.symlink("/nonexistent/path", broken_link_path)
        
        broken_link_path_var = os.path.join(self.var_tmp_path, "broken_link_var")
        os.symlink("/nonexistent/path_var", broken_link_path_var)

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def _run_ansible_playbook(self, playbook, inventory, extra_vars=None):
        cmd = [
            "ansible-playbook",
            "-i", inventory,
            playbook,
            "--connection=local", # Run against localhost
            "--limit=localhost",  # Ensure it only runs on localhost
            "--extra-vars",
            yaml.dump(extra_vars) if extra_vars else "{}"
        ]
        # Mock rationale: subprocess.run is used to execute the Ansible playbook.
        # This is not a mock of Ansible itself, but rather running Ansible in a controlled,
        # isolated environment (localhost, temporary directories) to make the test deterministic
        # and "offline" from the perspective of the actual system.
        # The 'extra_vars' are used to redirect the playbook's actions to the temporary paths.
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print(f"Ansible playbook failed:\n{result.stdout}\n{result.stderr}")
        return result

    def test_syntax_check(self):
        # Mock rationale: This test performs a static syntax check of the Ansible playbook.
        # It's deterministic and offline, ensuring the YAML structure is valid.
        cmd = ["ansible-playbook", "--syntax-check", self.playbook_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, f"Syntax check failed: {result.stderr}")

    def test_janitor_cleanup(self):
        # Initial state checks
        self.assertEqual(len(os.listdir(self.tmp_path)), 6) # 3 old, 2 new temp files, 1 broken link
        self.assertEqual(len(os.listdir(self.var_tmp_path)), 3) # 2 old, 1 new var_tmp files, 1 broken link
        self.assertEqual(len(os.listdir(self.log_path)), 4) # 2 old, 1 new log files, 1 important.txt, 1 archive dir (created by playbook)

        # Run the playbook with mocked paths
        extra_vars = {
            "cleanup_tmp_path": self.tmp_path,
            "cleanup_var_tmp_path": self.var_tmp_path,
            "cleanup_log_path": self.log_path,
            "log_archive_path": self.archive_path,
            "tmp_cleanup_days": 7,
            "log_cleanup_days": 30
        }
        result = self._run_ansible_playbook(self.playbook_path, self.inventory_path, extra_vars)
        self.assertEqual(result.returncode, 0, f"Playbook execution failed: {result.stderr}")

        # Assertions after cleanup
        # Only new temp files should remain in tmp_path, and broken link should be gone
        remaining_tmp_files = os.listdir(self.tmp_path)
        self.assertEqual(len(remaining_tmp_files), 2)
        self.assertIn("new_temp_file_0.txt", remaining_tmp_files)
        self.assertIn("new_temp_file_1.txt", remaining_tmp_files)
        self.assertNotIn("old_temp_file_0.txt", remaining_tmp_files)
        self.assertNotIn("broken_link", remaining_tmp_files)

        # Only new var_tmp files should remain in var_tmp_path, and broken link should be gone
        remaining_var_tmp_files = os.listdir(self.var_tmp_path)
        self.assertEqual(len(remaining_var_tmp_files), 1)
        self.assertIn("new_var_tmp_file_0.txt", remaining_var_tmp_files)
        self.assertNotIn("old_var_tmp_file_0.txt", remaining_var_tmp_files)
        self.assertNotIn("broken_link_var", remaining_var_tmp_files)

        # New log files and important.txt should remain in log_path
        # The archive directory itself is also in log_path
        remaining_log_files = os.listdir(self.log_path)
        self.assertEqual(len(remaining_log_files), 3) # new_log_0.log, important.txt, archive/
        self.assertIn("new_log_0.log", remaining_log_files)
        self.assertIn("important.txt", remaining_log_files)
        self.assertIn("archive", remaining_log_files)
        self.assertNotIn("old_log_0.log", remaining_log_files)

        # Old log files should be in the archive path
        archived_logs = os.listdir(self.archive_path)
        self.assertEqual(len(archived_logs), 2)
        self.assertIn("old_log_0.log", archived_logs)
        self.assertIn("old_log_1.log", archived_logs)
