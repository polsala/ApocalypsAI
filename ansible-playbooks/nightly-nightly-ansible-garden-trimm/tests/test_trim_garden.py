import unittest
import subprocess
import tempfile
import os
import shutil
from datetime import datetime, timedelta

class TestDigitalGardenTrimmer(unittest.TestCase):
    """
    Tests the nightly-ansible-garden-trimmer playbook.
    """
    temp_dir = None
    inventory_path = None
    config_path = None
    log_dir = None
    temp_clear_dir = None

    @classmethod
    def setUpClass(cls):
        """
        Set up a temporary environment for all tests.
        This includes creating a temporary directory, mock log files,
        and temporary configuration files for Ansible.
        """
        cls.temp_dir = tempfile.mkdtemp()
        print(f"\nCreated temporary test directory: {cls.temp_dir}")

        # Define paths within the temporary directory
        cls.log_dir = os.path.join(cls.temp_dir, "mock_logs")
        cls.temp_clear_dir = os.path.join(cls.temp_dir, "mock_temp")
        os.makedirs(cls.log_dir, exist_ok=True)
        os.makedirs(cls.temp_clear_dir, exist_ok=True)

        # Create mock log files
        # Old file (should be deleted)
        old_file_path = os.path.join(cls.log_dir, "old_log.log")
        with open(old_file_path, "w") as f:
            f.write("This is an old log entry.")
        # Mock rationale: Simulate an old file by setting its modification time.
        # This is deterministic as it uses a fixed past date.
        os.utime(old_file_path, (datetime.now() - timedelta(days=10)).timestamp(),
                                (datetime.now() - timedelta(days=10)).timestamp())

        # Newer file (should remain)
        new_file_path = os.path.join(cls.log_dir, "new_log.log")
        with open(new_file_path, "w") as f:
            f.write("This is a new log entry.")
        # Mock rationale: Simulate a new file by setting its modification time
        # to a recent date. This is deterministic.
        os.utime(new_file_path, (datetime.now() - timedelta(days=1)).timestamp(),
                                (datetime.now() - timedelta(days=1)).timestamp())

        # Another old file in a subdirectory (should be deleted)
        subdir = os.path.join(cls.log_dir, "subdir")
        os.makedirs(subdir, exist_ok=True)
        old_subdir_file_path = os.path.join(subdir, "old_subdir_log.log")
        with open(old_subdir_file_path, "w") as f:
            f.write("This is an old log entry in a subdirectory.")
        # Mock rationale: Simulate an old file in a subdirectory. Deterministic.
        os.utime(old_subdir_file_path, (datetime.now() - timedelta(days=15)).timestamp(),
                                       (datetime.now() - timedelta(days=15)).timestamp())

        # Create mock temporary files
        temp_file_1 = os.path.join(cls.temp_clear_dir, "temp_file_1.tmp")
        with open(temp_file_1, "w") as f:
            f.write("Temporary content 1.")
        temp_file_2 = os.path.join(cls.temp_clear_dir, "temp_file_2.tmp")
        with open(temp_file_2, "w") as f:
            f.write("Temporary content 2.")
        # Mock rationale: Create files that should be cleared. Deterministic.

        # Create a temporary inventory file
        cls.inventory_path = os.path.join(cls.temp_dir, "inventory_test.ini")
        with open(cls.inventory_path, "w") as f:
            f.write("[local]\nlocalhost ansible_connection=local\n")
        # Mock rationale: Provide a minimal, local inventory for testing. Deterministic.

        # Create a temporary garden_config.yml
        cls.config_path = os.path.join(cls.temp_dir, "garden_config_test.yml")
        with open(cls.config_path, "w") as f:
            f.write(f"""
log_paths_to_trim:
  - {cls.log_dir}
log_age_days: 7 # Files older than 7 days will be deleted

temp_paths_to_clear:
  - {cls.temp_clear_dir}
""")
        # Mock rationale: Configure the playbook to target the mock directories. Deterministic.

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the temporary environment after all tests.
        """
        if cls.temp_dir and os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)
            print(f"Cleaned up temporary test directory: {cls.temp_dir}")

    def test_playbook_execution_and_trimming(self):
        """
        Tests that the playbook runs successfully and correctly prunes files.
        """
        playbook_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/trim_garden.yml"))
        
        # Ensure the playbook path is correct
        self.assertTrue(os.path.exists(playbook_path), f"Playbook not found at {playbook_path}")

        # Run the Ansible playbook
        print(f"Running Ansible playbook: {playbook_path}")
        print(f"  Inventory: {self.inventory_path}")
        print(f"  Config: {self.config_path}")
        
        try:
            result = subprocess.run(
                [
                    "ansible-playbook",
                    "-i", self.inventory_path,
                    playbook_path,
                    "-e", f"ansible_python_interpreter={os.sys.executable}", # Use current python for ansible
                    "-e", f"garden_config_path={self.config_path}" # Pass config path as extra var
                ],
                capture_output=True,
                text=True,
                check=True # Raise an exception for non-zero exit codes
            )
            print("Ansible Playbook Output (stdout):\n", result.stdout)
            if result.stderr:
                print("Ansible Playbook Output (stderr):\n", result.stderr)

        except subprocess.CalledProcessError as e:
            self.fail(f"Ansible playbook failed with error:\n{e.stdout}\n{e.stderr}")
        except FileNotFoundError:
            self.fail("Ansible command not found. Please ensure Ansible is installed and in your PATH.")

        # Assertions
        # Check if old log files are deleted
        self.assertFalse(os.path.exists(os.path.join(self.log_dir, "old_log.log")),
                         "Old log file 'old_log.log' should have been deleted.")
        self.assertFalse(os.path.exists(os.path.join(self.log_dir, "subdir", "old_subdir_log.log")),
                         "Old log file 'old_subdir_log.log' in subdirectory should have been deleted.")

        # Check if new log file remains
        self.assertTrue(os.path.exists(os.path.join(self.log_dir, "new_log.log")),
                        "New log file 'new_log.log' should have remained.")

        # Check if temporary directory contents are cleared
        self.assertFalse(os.path.exists(os.path.join(self.temp_clear_dir, "temp_file_1.tmp")),
                         "Temporary file 'temp_file_1.tmp' should have been cleared.")
        self.assertFalse(os.path.exists(os.path.join(self.temp_clear_dir, "temp_file_2.tmp")),
                         "Temporary file 'temp_file_2.tmp' should have been cleared.")
        # Ensure the directory itself still exists
        self.assertTrue(os.path.exists(self.temp_clear_dir),
                        "Temporary directory 'mock_temp' should still exist after clearing its contents.")
        self.assertTrue(os.path.isdir(self.temp_clear_dir),
                        "Temporary directory 'mock_temp' should still be a directory.")
        self.assertEqual(len(os.listdir(self.temp_clear_dir)), 0,
                         "Temporary directory 'mock_temp' should be empty.")

if __name__ == "__main__":
    unittest.main()
