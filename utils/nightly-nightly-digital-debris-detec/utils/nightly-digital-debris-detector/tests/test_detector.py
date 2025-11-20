import pytest
import os
import subprocess
from unittest.mock import patch, MagicMock
from src.detector import get_git_untracked_files, get_empty_directories, detect_digital_debris, print_report

# Mock rationale: subprocess.run is used to interact with the Git CLI. 
# Mocking it ensures tests are deterministic, fast, and don't rely on a real Git repository or external processes.
@patch('subprocess.run')
def test_get_git_untracked_files_no_untracked(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout='', stderr='', returncode=0)
    files = get_git_untracked_files('/mock/repo')
    assert files == []
    mock_subprocess_run.assert_called_once_with(
        ['git', '-C', '/mock/repo', 'ls-files', '--others', '--exclude-standard'],
        capture_output=True,
        text=True,
        check=True
    )

# Mock rationale: subprocess.run is used to interact with the Git CLI. 
# Mocking it ensures tests are deterministic, fast, and don't rely on a real Git repository or external processes.
@patch('subprocess.run')
def test_get_git_untracked_files_with_untracked(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout='file1.txt\nfolder/file2.log\n', stderr='', returncode=0)
    files = get_git_untracked_files('/mock/repo')
    assert files == ['file1.txt', 'folder/file2.log']

# Mock rationale: subprocess.run is used to interact with the Git CLI. 
# Mocking it ensures tests are deterministic, fast, and don't rely on a real Git repository or external processes.
@patch('subprocess.run')
def test_get_git_untracked_files_git_error(mock_subprocess_run):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'git ls-files', stderr='fatal: not a git repository')
    files = get_git_untracked_files('/mock/repo')
    assert files == []

# Mock rationale: subprocess.run is used to interact with the Git CLI. 
# Mocking it ensures tests are deterministic, fast, and don't rely on a real Git repository or external processes.
@patch('subprocess.run')
def test_get_git_untracked_files_git_not_found(mock_subprocess_run):
    mock_subprocess_run.side_effect = FileNotFoundError()
    files = get_git_untracked_files('/mock/repo')
    assert files == []

# Mock rationale: os.walk is used to traverse the file system. 
# Mocking it ensures tests are deterministic, fast, and don't rely on actual file system state.
@patch('os.walk')
@patch('os.path.relpath', side_effect=lambda path, start: path.replace(start, '').lstrip(os.sep))
def test_get_empty_directories_no_empty_dirs(mock_os_walk, mock_relpath):
    # Simulate a directory structure with no empty directories
    mock_os_walk.return_value = [
        ('/mock/repo', ['dir1', 'dir2'], ['file1.txt']),
        ('/mock/repo/dir1', [], ['file2.txt']),
        ('/mock/repo/dir2', ['subdir'], []),
        ('/mock/repo/dir2/subdir', [], ['file3.txt']),
    ]
    empty_dirs = get_empty_directories('/mock/repo')
    assert empty_dirs == []

# Mock rationale: os.walk is used to traverse the file system. 
# Mocking it ensures tests are deterministic, fast, and don't rely on actual file system state.
@patch('os.walk')
@patch('os.path.relpath', side_effect=lambda path, start: path.replace(start, '').lstrip(os.sep))
def test_get_empty_directories_with_empty_dirs(mock_os_walk, mock_relpath):
    # Simulate a directory structure with empty directories
    mock_os_walk.return_value = [
        ('/mock/repo', ['dir1', 'empty_dir1', 'dir2'], ['file1.txt']),
        ('/mock/repo/dir1', [], ['file2.txt']),
        ('/mock/repo/empty_dir1', [], []),
        ('/mock/repo/dir2', ['empty_subdir'], ['file3.txt']),
        ('/mock/repo/dir2/empty_subdir', [], []),
    ]
    empty_dirs = get_empty_directories('/mock/repo')
    assert sorted(empty_dirs) == sorted(['empty_dir1', 'dir2/empty_subdir'])

# Mock rationale: os.walk is used to traverse the file system. 
# Mocking it ensures tests are deterministic, fast, and don't rely on actual file system state.
@patch('os.walk')
@patch('os.path.relpath', side_effect=lambda path, start: path.replace(start, '').lstrip(os.sep))
def test_get_empty_directories_ignores_git_dir(mock_os_walk, mock_relpath):
    # Simulate a .git directory that might appear empty during walk
    mock_os_walk.return_value = [
        ('/mock/repo', ['.git', 'src'], ['README.md']),
        ('/mock/repo/.git', ['objects'], []),
        ('/mock/repo/.git/objects', [], []),
        ('/mock/repo/src', [], ['main.py']),
    ]
    empty_dirs = get_empty_directories('/mock/repo')
    assert empty_dirs == [] # .git/objects should not be reported as empty

# Mock rationale: os.path.isdir is used to validate the input path. 
# Mocking it ensures tests are deterministic and don't rely on actual file system state.
@patch('os.path.isdir', return_value=False)
@patch('sys.stderr', new_callable=MagicMock)
def test_detect_digital_debris_invalid_path(mock_stderr, mock_isdir):
    debris = detect_digital_debris('/nonexistent/path')
    assert debris == {"untracked_files": [], "empty_directories": []}
    mock_isdir.assert_called_once_with('/nonexistent/path')
    assert "Error: Repository path" in mock_stderr.write.call_args[0][0]

# Mock rationale: subprocess.run and os.walk are external dependencies. 
# Mocking them ensures tests are deterministic, fast, and don't rely on a real Git repository or actual file system state.
@patch('src.detector.get_git_untracked_files', return_value=['untracked.txt', 'temp/log.tmp'])
@patch('src.detector.get_empty_directories', return_value=['empty_folder', 'src/empty_sub'])
@patch('os.path.isdir', return_value=True)
@patch('os.path.abspath', side_effect=lambda x: f'/abs/{x.lstrip(".")}')
def test_detect_digital_debris_with_findings(mock_abspath, mock_isdir, mock_get_empty_dirs, mock_get_untracked_files):
    repo_path = '.'
    debris = detect_digital_debris(repo_path)
    assert debris == {
        "untracked_files": ['untracked.txt', 'temp/log.tmp'],
        "empty_directories": ['empty_folder', 'src/empty_sub']
    }
    mock_get_untracked_files.assert_called_once_with(repo_path)
    mock_get_empty_directories.assert_called_once_with(repo_path)

# Mock rationale: subprocess.run and os.walk are external dependencies. 
# Mocking them ensures tests are deterministic, fast, and don't rely on a real Git repository or actual file system state.
@patch('src.detector.get_git_untracked_files', return_value=[])
@patch('src.detector.get_empty_directories', return_value=[])
@patch('os.path.isdir', return_value=True)
@patch('os.path.abspath', side_effect=lambda x: f'/abs/{x.lstrip(".")}')
def test_detect_digital_debris_no_findings(mock_abspath, mock_isdir, mock_get_empty_dirs, mock_get_untracked_files):
    repo_path = '.'
    debris = detect_digital_debris(repo_path)
    assert debris == {"untracked_files": [], "empty_directories": []}
    mock_get_untracked_files.assert_called_once_with(repo_path)
    mock_get_empty_directories.assert_called_once_with(repo_path)

# Mock rationale: sys.stdout is used for printing the report. 
# Mocking it allows capturing the output for assertion without affecting the console.
@patch('sys.stdout', new_callable=MagicMock)
@patch('os.path.abspath', side_effect=lambda x: f'/abs/{x.lstrip(".")}')
def test_print_report_with_findings(mock_abspath, mock_stdout):
    debris_data = {
        "untracked_files": ['file1.txt', 'dir/file2.log'],
        "empty_directories": ['empty_dir/', 'another_empty/']
    }
    repo_path = '/test/repo'
    print_report(debris_data, repo_path)

    output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
    assert "--- Digital Debris Report ---" in output
    assert "Scanning repository: /abs/test/repo" in output
    assert "🗑️ Untracked Files (Forgotten Relics):" in output
    assert "  - file1.txt" in output
    assert "  - dir/file2.log" in output
    assert "🕳️ Empty Directories (Hollow Ruins):" in output
    assert "  - empty_dir/" in output
    assert "  - another_empty/" in output
    assert "--- End of Report ---" in output

# Mock rationale: sys.stdout is used for printing the report. 
# Mocking it allows capturing the output for assertion without affecting the console.
@patch('sys.stdout', new_callable=MagicMock)
@patch('os.path.abspath', side_effect=lambda x: f'/abs/{x.lstrip(".")}')
def test_print_report_no_findings(mock_abspath, mock_stdout):
    debris_data = {
        "untracked_files": [],
        "empty_directories": []
    }
    repo_path = '/test/repo'
    print_report(debris_data, repo_path)

    output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
    assert "--- Digital Debris Report ---" in output
    assert "Scanning repository: /abs/test/repo" in output
    assert "✅ No untracked files found. Your relics are accounted for!" in output
    assert "✅ No empty directories found. Your structures are sound!" in output
    assert "--- End of Report ---" in output

# Mock rationale: sys.argv is used to pass command-line arguments. 
# Mocking it allows testing the script's entry point with different arguments.
# Mock rationale: sys.exit is called to terminate the script. 
# Mocking it prevents actual script termination during tests and allows checking the exit code.
# Mock rationale: detect_digital_debris and print_report are core functions. 
# Mocking them allows testing the main execution flow without running the full detection logic.
@patch('sys.argv', ['detector.py', '.'])
@patch('sys.exit')
@patch('src.detector.detect_digital_debris', return_value={'untracked_files': ['a.txt'], 'empty_directories': []})
@patch('src.detector.print_report')
def test_main_with_findings(mock_print_report, mock_detect_debris, mock_sys_exit):
    # Re-import the module to ensure __name__ == "__main__" block is executed
    import importlib
    import src.detector
    importlib.reload(src.detector)

    mock_detect_debris.assert_called_once_with('.')
    mock_print_report.assert_called_once_with({'untracked_files': ['a.txt'], 'empty_directories': []}, '.')
    mock_sys_exit.assert_called_once_with(0)

# Mock rationale: sys.argv is used to pass command-line arguments. 
# Mocking it allows testing the script's entry point with different arguments.
# Mock rationale: sys.exit is called to terminate the script. 
# Mocking it prevents actual script termination during tests and allows checking the exit code.
# Mock rationale: detect_digital_debris and print_report are core functions. 
# Mocking them allows testing the main execution flow without running the full detection logic.
@patch('sys.argv', ['detector.py', '.'])
@patch('sys.exit')
@patch('src.detector.detect_digital_debris', return_value={'untracked_files': [], 'empty_directories': []})
@patch('src.detector.print_report')
def test_main_no_findings(mock_print_report, mock_detect_debris, mock_sys_exit):
    # Re-import the module to ensure __name__ == "__main__" block is executed
    import importlib
    import src.detector
    importlib.reload(src.detector)

    mock_detect_debris.assert_called_once_with('.')
    mock_print_report.assert_called_once_with({'untracked_files': [], 'empty_directories': []}, '.')
    mock_sys_exit.assert_called_once_with(0)

# Mock rationale: sys.argv is used to pass command-line arguments. 
# Mocking it allows testing the script's entry point with different arguments.
# Mock rationale: sys.exit is called to terminate the script. 
# Mocking it prevents actual script termination during tests and allows checking the exit code.
@patch('sys.argv', ['detector.py'])
@patch('sys.exit')
@patch('sys.stderr', new_callable=MagicMock)
def test_main_no_args(mock_stderr, mock_sys_exit):
    # Re-import the module to ensure __name__ == "__main__" block is executed
    import importlib
    import src.detector
    importlib.reload(src.detector)

    assert "Usage: python3 src/detector.py <path_to_repository>" in mock_stderr.write.call_args[0][0]
    mock_sys_exit.assert_called_once_with(1)
