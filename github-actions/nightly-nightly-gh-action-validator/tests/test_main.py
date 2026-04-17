import pytest
import subprocess
import os

# Mock rationale: We are mocking the subprocess.run and os.path.exists functions to control
# the execution environment and simulate different file states without actual file I/O
# or external command execution. This makes tests deterministic and runnable offline.

@pytest.fixture
def mock_subprocess_run(monkeypatch):
    def _mock_run(command, capture_output=False, text=False, check=False):
        # Simulate yamllint success
        if 'yamllint' in command[0]:
            if command[1] == 'tests/valid_workflow.yml':
                return subprocess.CompletedProcess(args=command, returncode=0, stdout='', stderr='')
            else:
                return subprocess.CompletedProcess(args=command, returncode=1, stdout='', stderr='YAML error')
        # Simulate grep success/failure
        if 'grep' in command[0]:
            if command[2] == 'tests/valid_workflow.yml' and command[1] == '-q':
                return subprocess.CompletedProcess(args=command, returncode=0, stdout='', stderr='')
            elif command[2] == 'tests/no_on_trigger.yml' and command[1] == '-q':
                return subprocess.CompletedProcess(args=command, returncode=1, stdout='', stderr='')
            else:
                return subprocess.CompletedProcess(args=command, returncode=1, stdout='', stderr='grep error')
        return subprocess.CompletedProcess(args=command, returncode=0, stdout='', stderr='')
    monkeypatch.setattr(subprocess, 'run', _mock_run)

@pytest.fixture
def mock_os_path(monkeypatch):
    def _mock_exists(path):
        if path == 'tests/valid_workflow.yml':
            return True
        elif path == 'tests/invalid_syntax.yml':
            return True
        elif path == 'tests/no_on_trigger.yml':
            return True
        elif path == 'non_existent_file.yml':
            return False
        return False
    monkeypatch.setattr(os.path, 'exists', _mock_exists)

def test_valid_workflow(mock_subprocess_run, mock_os_path):
    # Create dummy files for the script to 'read'
    with open('tests/valid_workflow.yml', 'w') as f: f.write('on: push\njobs: { build: { runs-on: ubuntu-latest, steps: [{ uses: actions/checkout@v4 }] } }')
    
    result = subprocess.run(['./src/main.sh', 'tests/valid_workflow.yml'], capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert "passed basic validation" in result.stdout
    
    # Clean up dummy file
    os.remove('tests/valid_workflow.yml')

def test_invalid_yaml_syntax(mock_subprocess_run, mock_os_path):
    # Create dummy file with invalid YAML
    with open('tests/invalid_syntax.yml', 'w') as f: f.write('on: push\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n        invalid_indentation: true')

    result = subprocess.run(['./src/main.sh', 'tests/invalid_syntax.yml'], capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert "YAML syntax errors" in result.stderr
    
    # Clean up dummy file
    os.remove('tests/invalid_syntax.yml')

def test_missing_on_trigger(mock_subprocess_run, mock_os_path):
    # Create dummy file missing 'on:' trigger
    with open('tests/no_on_trigger.yml', 'w') as f: f.write('jobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4')

    result = subprocess.run(['./src/main.sh', 'tests/no_on_trigger.yml'], capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert "'on:' trigger not found" in result.stdout
    
    # Clean up dummy file
    os.remove('tests/no_on_trigger.yml')

def test_workflow_file_not_found(mock_subprocess_run, mock_os_path):
    result = subprocess.run(['./src/main.sh', 'non_existent_file.yml'], capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert "Workflow file not found" in result.stderr

def test_missing_workflow_path_argument(mock_subprocess_run, mock_os_path):
    result = subprocess.run(['./src/main.sh'], capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert "WORKFLOW_PATH is required" in result.stderr
