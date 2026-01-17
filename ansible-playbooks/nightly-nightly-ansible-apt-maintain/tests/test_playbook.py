import unittest
import pathlib

class TestAptPlaybook(unittest.TestCase):
    def setUp(self):
        # Resolve the path to the playbook relative to this test file
        self.playbook_path = pathlib.Path(__file__).resolve().parents[1] / 'src' / 'playbook.yml'
        self.content = self.playbook_path.read_text()

    def test_contains_update_cache(self):
        self.assertIn('update_cache: yes', self.content)

    def test_contains_autoremove(self):
        self.assertIn('autoremove: yes', self.content)

    def test_contains_autoclean(self):
        self.assertIn('autoclean: yes', self.content)

    def test_contains_debug_message(self):
        self.assertIn('msg: "Apt maintenance completed."', self.content)

if __name__ == '__main__':
    unittest.main()
