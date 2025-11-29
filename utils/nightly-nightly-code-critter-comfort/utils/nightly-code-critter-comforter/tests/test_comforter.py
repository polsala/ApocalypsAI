import unittest
import os
from unittest.mock import patch, mock_open
from src.comforter import (
    find_critters_in_file,
    scan_directory_for_critters,
    generate_report,
    CRITTER_KEYWORDS,
    DEFAULT_EXTENSIONS,
    DEFAULT_EXCLUDE_DIRS
)

class TestComforter(unittest.TestCase):

    def setUp(self):
        # Reset CRITTER_KEYWORDS for each test to ensure consistency
        # (though not strictly necessary as it's a constant, good practice for mutable globals)
        self.original_critter_keywords = list(CRITTER_KEYWORDS)

    def tearDown(self):
        # Restore CRITTER_KEYWORDS if it were ever modified (it shouldn't be)
        CRITTER_KEYWORDS[:] = self.original_critter_keywords

    @patch("builtins.open", new_callable=mock_open)
    def test_find_critters_in_file_basic(self, mock_file_open):
        # Mock rationale: Simulate reading a file's content without actual file I/O.
        mock_file_open.return_value.read.return_value = (
            "line 1\n"
            "# TODO: Do something\n"
            "line 3\n"
            "// FIXME: Fix this bug\n"
            "line 5\n"
        )
        mock_file_open.return_value.__enter__.return_value = mock_file_open.return_value # For 'with open(...)'

        critters = find_critters_in_file("dummy.py")
        self.assertEqual(len(critters), 2)
        self.assertEqual(critters[0], (2, "# TODO: Do something"))
        self.assertEqual(critters[1], (4, "// FIXME: Fix this bug"))

    @patch("builtins.open", new_callable=mock_open)
    def test_find_critters_in_file_no_critters(self, mock_file_open):
        # Mock rationale: Simulate a file with no critter comments.
        mock_file_open.return_value.read.return_value = (
            "line 1\n"
            "some code\n"
            "another line\n"
        )
        mock_file_open.return_value.__enter__.return_value = mock_file_open.return_value

        critters = find_critters_in_file("dummy.py")
        self.assertEqual(len(critters), 0)

    @patch("builtins.open", new_callable=mock_open)
    def test_find_critters_in_file_case_insensitivity(self, mock_file_open):
        # Mock rationale: Ensure critter keywords are found regardless of case.
        mock_file_open.return_value.read.return_value = (
            "line 1\n"
            "# todo: lowercase todo\n"
            "// fixme: lowercase fixme\n"
            "/* BUG: uppercase bug */\n"
            "# HaCk: mixed case hack\n"
        )
        mock_file_open.return_value.__enter__.return_value = mock_file_open.return_value

        critters = find_critters_in_file("dummy.js")
        self.assertEqual(len(critters), 4)
        self.assertEqual(critters[0], (2, "# todo: lowercase todo"))
        self.assertEqual(critters[1], (3, "// fixme: lowercase fixme"))
        self.assertEqual(critters[2], (4, "/* BUG: uppercase bug */"))
        self.assertEqual(critters[3], (5, "# HaCk: mixed case hack"))

    @patch("builtins.open", new_callable=mock_open)
    def test_find_critters_in_file_multiple_on_same_line(self, mock_file_open):
        # Mock rationale: Verify that only one critter is reported per line, even if multiple keywords exist.
        mock_file_open.return_value.read.return_value = (
            "line 1\n"
            "# TODO: first critter // FIXME: second critter\n"
            "line 3\n"
        )
        mock_file_open.return_value.__enter__.return_value = mock_file_open.return_value

        critters = find_critters_in_file("dummy.py")
        self.assertEqual(len(critters), 1)
        self.assertEqual(critters[0], (2, "# TODO: first critter // FIXME: second critter"))

    @patch("builtins.open", new_callable=mock_open)
    def test_find_critters_in_file_empty_file(self, mock_file_open):
        # Mock rationale: Test behavior with an empty file.
        mock_file_open.return_value.read.return_value = ""
        mock_file_open.return_value.__enter__.return_value = mock_file_open.return_value

        critters = find_critters_in_file("empty.txt")
        self.assertEqual(len(critters), 0)

    @patch("os.walk")
    @patch("src.comforter.find_critters_in_file")
    def test_scan_directory_for_critters_basic(self, mock_find_critters, mock_os_walk):
        # Mock rationale: Simulate a directory structure and file content without actual file system access.
        # mock_os_walk simulates the directory traversal.
        # mock_find_critters simulates the file content analysis.

        mock_os_walk.return_value = [
            ("/root", ["dir1", "dir2"], ["file1.py", "file2.txt"]),
            ("/root/dir1", [], ["file3.js"]),
        ]
        mock_find_critters.side_effect = [
            [(10, "# TODO: In file1")],  # For file1.py
            [],                        # For file2.txt (no critters)
            [(5, "// FIXME: In file3")] # For file3.js
        ]

        root_dir = "/root"
        include_extensions = [".py", ".js"]
        exclude_dirs = []

        result = scan_directory_for_critters(root_dir, include_extensions, exclude_dirs)

        self.assertEqual(len(result), 2)
        self.assertIn(os.path.join(root_dir, "file1.py"), result)
        self.assertIn(os.path.join(root_dir, "dir1", "file3.js"), result)
        self.assertEqual(result[os.path.join(root_dir, "file1.py")], [(10, "# TODO: In file1")])
        self.assertEqual(result[os.path.join(root_dir, "dir1", "file3.js")], [(5, "// FIXME: In file3")])

        # Ensure find_critters_in_file was called for relevant files
        mock_find_critters.assert_any_call(os.path.join(root_dir, "file1.py"))
        mock_find_critters.assert_any_call(os.path.join(root_dir, "file2.txt")) # Called but returned empty
        mock_find_critters.assert_any_call(os.path.join(root_dir, "dir1", "file3.js"))

    @patch("os.walk")
    @patch("src.comforter.find_critters_in_file")
    def test_scan_directory_for_critters_exclude_dirs(self, mock_find_critters, mock_os_walk):
        # Mock rationale: Test that specified directories are correctly excluded from the scan.
        mock_os_walk.return_value = [
            ("/root", ["excluded_dir", "included_dir"], ["main.py"]),
            ("/root/excluded_dir", [], ["secret.py"]), # Should be skipped
            ("/root/included_dir", [], ["feature.py"]),
        ]
        mock_find_critters.side_effect = [
            [(1, "# TODO: Main")], # For main.py
            [(1, "# FIXME: Feature")] # For feature.py
        ]

        root_dir = "/root"
        include_extensions = [".py"]
        exclude_dirs = ["excluded_dir"]

        result = scan_directory_for_critters(root_dir, include_extensions, exclude_dirs)

        self.assertEqual(len(result), 2) # main.py and feature.py
        self.assertIn(os.path.join(root_dir, "main.py"), result)
        self.assertIn(os.path.join(root_dir, "included_dir", "feature.py"), result)
        self.assertNotIn(os.path.join(root_dir, "excluded_dir", "secret.py"), result)

        # Ensure find_critters_in_file was NOT called for files in excluded_dir
        mock_find_critters.assert_any_call(os.path.join(root_dir, "main.py"))
        mock_find_critters.assert_any_call(os.path.join(root_dir, "included_dir", "feature.py"))
        self.assertFalse(mock_find_critters.called_with(os.path.join(root_dir, "excluded_dir", "secret.py")))

    @patch("os.walk")
    @patch("src.comforter.find_critters_in_file")
    def test_scan_directory_for_critters_include_extensions(self, mock_find_critters, mock_os_walk):
        # Mock rationale: Test that only files with specified extensions are scanned.
        mock_os_walk.return_value = [
            ("/root", [], ["app.py", "config.json", "README.md"]),
        ]
        mock_find_critters.side_effect = [
            [(1, "# TODO: Python")], # For app.py
            [(1, "<!-- FIXME: Markdown -->")] # For README.md
        ]

        root_dir = "/root"
        include_extensions = [".py", ".md"]
        exclude_dirs = []

        result = scan_directory_for_critters(root_dir, include_extensions, exclude_dirs)

        self.assertEqual(len(result), 2)
        self.assertIn(os.path.join(root_dir, "app.py"), result)
        self.assertIn(os.path.join(root_dir, "README.md"), result)
        self.assertNotIn(os.path.join(root_dir, "config.json"), result)

        mock_find_critters.assert_any_call(os.path.join(root_dir, "app.py"))
        mock_find_critters.assert_any_call(os.path.join(root_dir, "README.md"))
        # find_critters_in_file should not be called for config.json
        self.assertFalse(mock_find_critters.called_with(os.path.join(root_dir, "config.json")))


    def test_generate_report_no_critters(self):
        # Mock rationale: Test report generation when no critters are found.
        report = generate_report({}, "/test/path")
        self.assertIn("No critters found. Your codebase is sparkling clean!", report)
        self.assertIn("Critter Report for: /test/path", report)
        self.assertNotIn("Total Critters Found:", report)

    def test_generate_report_with_critters(self):
        # Mock rationale: Test report generation with sample critter data.
        critter_data = {
            "/project/src/file1.py": [
                (10, "# TODO: Implement feature X"),
                (25, "# FIXME: Broken logic here")
            ],
            "/project/docs/README.md": [
                (5, "- [ ] HACK: Temporary note")
            ]
        }
        root_dir = "/project"
        report = generate_report(critter_data, root_dir)

        expected_report_lines = [
            "Critter Report for: /project",
            "",
            "---",
            "File: /project/src/file1.py",
            "  Line 10: # TODO: Implement feature X",
            "  Line 25: # FIXME: Broken logic here",
            "---",
            "File: /project/docs/README.md",
            "  Line 5: - [ ] HACK: Temporary note",
            "---",
            "Total Critters Found: 3 in 2 files."
        ]
        self.assertEqual(report, "\n".join(expected_report_lines))

    @patch("os.path.isdir", return_value=True)
    @patch("src.comforter.scan_directory_for_critters", return_value={})
    @patch("src.comforter.generate_report", return_value="Mock Report")
    @patch("builtins.print")
    def test_main_no_critters(self, mock_print, mock_generate_report, mock_scan_directory, mock_isdir):
        # Mock rationale: Test the main function's flow without actual file system or output.
        # os.path.isdir is mocked to confirm the path is valid.
        # scan_directory_for_critters is mocked to return no critters.
        # generate_report is mocked to return a predefined report string.
        # builtins.print is mocked to capture output.

        from src.comforter import main
        with patch("sys.argv", ["comforter.py", "--path", "/test/project"]):
            main()
            mock_isdir.assert_called_once_with(os.path.abspath("/test/project"))
            mock_scan_directory.assert_called_once()
            mock_generate_report.assert_called_once()
            mock_print.assert_called_once_with("Mock Report")

    @patch("os.path.isdir", return_value=False)
    @patch("builtins.print")
    @patch("sys.exit")
    def test_main_invalid_path(self, mock_exit, mock_print, mock_isdir):
        # Mock rationale: Test error handling for an invalid path.
        # os.path.isdir is mocked to return False.
        # builtins.print is mocked to capture error output.
        # sys.exit is mocked to prevent actual program exit and check exit code.

        from src.comforter import main
        with patch("sys.argv", ["comforter.py", "--path", "/nonexistent/path"]):
            main()
            mock_isdir.assert_called_once_with(os.path.abspath("/nonexistent/path"))
            mock_print.assert_called_once_with("Error: The specified path '/nonexistent/path' is not a valid directory.")
            mock_exit.assert_called_once_with(1)

    @patch("os.path.isdir", return_value=True)
    @patch("src.comforter.scan_directory_for_critters")
    @patch("src.comforter.generate_report")
    @patch("builtins.print")
    def test_main_custom_extensions_and_excludes(self, mock_print, mock_generate_report, mock_scan_directory, mock_isdir):
        # Mock rationale: Test that custom extensions and exclude directories are passed correctly.
        from src.comforter import main
        mock_scan_directory.return_value = {}
        mock_generate_report.return_value = "Custom Report"

        with patch("sys.argv", [
            "comforter.py",
            "--path", "/test/project",
            "--extensions", "txt,log",
            "--exclude", "temp,cache"
        ]):
            main()
            mock_scan_directory.assert_called_once_with(
                os.path.abspath("/test/project"),
                [".txt", ".log"],
                ["temp", "cache"]
            )
            mock_print.assert_called_once_with("Custom Report")


if __name__ == "__main__":
    unittest.main()
