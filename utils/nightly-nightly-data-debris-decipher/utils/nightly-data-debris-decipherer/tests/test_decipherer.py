import unittest
import os
import json
from unittest.mock import patch, mock_open
from io import StringIO
from src.decipherer import decipher_file, main

class TestDecipherer(unittest.TestCase):

    def test_decipher_file_basic_extraction(self):
        # Mock rationale: Simulate file content without actual file I/O.
        mock_file_content = (
            "Visit our site at http://example.com/page?id=123. "
            "Contact us at user@domain.org. "
            "Logged on 2023-10-27T14:30:00Z. Another date: 2023-10-26. "
            "Also, check https://sub.example.net/path. "
            "Email: admin@sub.domain.org."
        )
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = decipher_file("/fake/path/test.txt")
            self.assertEqual(result["filepath"], "/fake/path/test.txt")
            self.assertIn("http://example.com/page?id=123", result["urls"])
            self.assertIn("https://sub.example.net/path", result["urls"])
            self.assertIn("user@domain.org", result["emails"])
            self.assertIn("admin@sub.domain.org", result["emails"])
            self.assertIn("2023-10-27T14:30:00Z", result["timestamps"])
            self.assertIn("2023-10-26", result["timestamps"])
            self.assertEqual(len(result["urls"]), 2)
            self.assertEqual(len(result["emails"]), 2)
            self.assertEqual(len(result["timestamps"]), 2)

    def test_decipher_file_no_matches(self):
        # Mock rationale: Simulate a file with no relevant patterns.
        mock_file_content = "This is just plain text with no special patterns."
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = decipher_file("/fake/path/empty.txt")
            self.assertEqual(result["filepath"], "/fake/path/empty.txt")
            self.assertEqual(result["urls"], [])
            self.assertEqual(result["emails"], [])
            self.assertEqual(result["timestamps"], [])

    def test_decipher_file_empty_file(self):
        # Mock rationale: Simulate an empty file.
        mock_file_content = ""
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = decipher_file("/fake/path/empty.txt")
            self.assertEqual(result["filepath"], "/fake/path/empty.txt")
            self.assertEqual(result["urls"], [])
            self.assertEqual(result["emails"], [])
            self.assertEqual(result["timestamps"], [])

    def test_decipher_file_with_duplicates(self):
        # Mock rationale: Ensure duplicates are handled (sets are used internally).
        mock_file_content = (
            "http://example.com http://example.com "
            "user@domain.org user@domain.org "
            "2023-01-01 2023-01-01"
        )
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = decipher_file("/fake/path/duplicates.txt")
            self.assertEqual(len(result["urls"]), 1)
            self.assertEqual(len(result["emails"]), 1)
            self.assertEqual(len(result["timestamps"]), 1)

    def test_decipher_file_error_handling(self):
        # Mock rationale: Simulate an IOError during file reading.
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            result = decipher_file("/fake/path/unreadable.txt")
            self.assertEqual(result["filepath"], "/fake/path/unreadable.txt")
            self.assertIn("error", result)
            self.assertEqual(result["urls"], [])
            self.assertEqual(result["emails"], [])
            self.assertEqual(result["timestamps"], [])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_stdout_output(self, mock_parse_args, mock_stdout, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Simulate command-line arguments, file system structure,
        # file content, and capture stdout for verification.
        mock_parse_args.return_value = argparse.Namespace(
            input_dir="/test/debris",
            output_file=None,
            file_extensions="txt,log"
        )
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ("/test/debris", [], ["file1.txt", "file2.log", "image.png"]),
            ("/test/debris/sub", [], ["subfile.txt"])
        ]
        
        # Configure mock_file_open to return different content for different files
        def mock_read_data(filepath, *args, **kwargs):
            if "file1.txt" in filepath:
                return "URL: http://a.com Email: a@b.com Date: 2023-01-01"
            elif "file2.log" in filepath:
                return "URL: https://c.org"
            elif "subfile.txt" in filepath:
                return "Email: x@y.net"
            return ""

        mock_file_open.side_effect = lambda *args, **kwargs: mock_open(read_data=mock_read_data(args[0])).return_value

        main()

        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(len(output), 3)
        
        # Check content of the first file
        file1_result = next(item for item in output if "file1.txt" in item["filepath"])
        self.assertIn("http://a.com", file1_result["urls"])
        self.assertIn("a@b.com", file1_result["emails"])
        self.assertIn("2023-01-01", file1_result["timestamps"])

        # Check content of the second file
        file2_result = next(item for item in output if "file2.log" in item["filepath"])
        self.assertIn("https://c.org", file2_result["urls"])
        self.assertEqual(len(file2_result["emails"]), 0)

        # Check content of the third file
        subfile_result = next(item for item in output if "subfile.txt" in item["filepath"])
        self.assertIn("x@y.net", subfile_result["emails"])
        self.assertEqual(len(subfile_result["urls"]), 0)

        # Ensure image.png was skipped
        self.assertFalse(any("image.png" in item["filepath"] for item in output))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_file_output(self, mock_parse_args, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Simulate command-line arguments, file system structure,
        # file content, and verify that the output file is written correctly.
        mock_parse_args.return_value = argparse.Namespace(
            input_dir="/test/debris",
            output_file="/output/report.json",
            file_extensions="txt"
        )
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ("/test/debris", [], ["data.txt"])
        ]
        mock_file_open.return_value.read.return_value = "Test data: http://test.com"

        main()

        # Check that open was called to write the output file
        mock_file_open.assert_called_with("/output/report.json", 'w', encoding='utf-8')
        
        # Verify the content written to the mock file
        written_content = mock_file_open().write.call_args[0][0]
        output_data = json.loads(written_content)
        self.assertEqual(len(output_data), 1)
        self.assertIn("http://test.com", output_data[0]["urls"])
        self.assertEqual(output_data[0]["filepath"], os.path.join("/test/debris", "data.txt"))

    @patch('os.path.isdir')
    @patch('sys.exit')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_input_dir(self, mock_parse_args, mock_print, mock_exit, mock_isdir):
        # Mock rationale: Simulate an invalid input directory and check for error handling.
        mock_parse_args.return_value = argparse.Namespace(
            input_dir="/nonexistent/dir",
            output_file=None,
            file_extensions="txt"
        )
        mock_isdir.return_value = False

        main()
        mock_print.assert_called_with("Error: Input directory '/nonexistent/dir' does not exist or is not a directory.")
        mock_exit.assert_called_with(1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_output_file_write_error(self, mock_parse_args, mock_print, mock_exit, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Simulate an error when writing to the output file.
        mock_parse_args.return_value = argparse.Namespace(
            input_dir="/test/debris",
            output_file="/unwritable/report.json",
            file_extensions="txt"
        )
        mock_isdir.return_value = True
        mock_walk.return_value = [("/test/debris", [], ["data.txt"])]
        mock_file_open.side_effect = IOError("Disk full") # Simulate write error on the output file

        main()
        mock_print.assert_called_with("Error: Could not write to output file /unwritable/report.json - Disk full")
        mock_exit.assert_called_with(1)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_custom_extensions(self, mock_parse_args, mock_stdout, mock_file_open, mock_walk, mock_isdir):
        # Mock rationale: Test that custom file extensions are respected.
        mock_parse_args.return_value = argparse.Namespace(
            input_dir="/test/debris",
            output_file=None,
            file_extensions="yml,conf"
        )
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ("/test/debris", [], ["config.yml", "settings.conf", "notes.txt"])
        ]
        
        def mock_read_data(filepath, *args, **kwargs):
            if "config.yml" in filepath:
                return "url: http://yaml.com"
            elif "settings.conf" in filepath:
                return "email=conf@example.com"
            return ""

        mock_file_open.side_effect = lambda *args, **kwargs: mock_open(read_data=mock_read_data(args[0])).return_value

        main()

        output = json.loads(mock_stdout.getvalue())
        self.assertEqual(len(output), 2) # Only yml and conf files should be processed

        yml_result = next(item for item in output if "config.yml" in item["filepath"])
        self.assertIn("http://yaml.com", yml_result["urls"])

        conf_result = next(item for item in output if "settings.conf" in item["filepath"])
        self.assertIn("conf@example.com", conf_result["emails"])

        self.assertFalse(any("notes.txt" in item["filepath"] for item in output))


if __name__ == '__main__':
    unittest.main()
