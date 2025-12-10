import subprocess
import json
import pytest


def run_docker_command(cmd):
    """Run a command in the devbox container and return the result."""
    compose_cmd = ["docker", "compose", "run", "--rm", "devbox"] + cmd
    try:
        result = subprocess.run(compose_cmd, capture_output=True, text=True, check=True)
        return result
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Command failed: {' '.join(compose_cmd)}\nOutput: {e.stderr}")


def test_python_installed():
    """Test that Python 3.11 is installed and accessible."""
    result = run_docker_command(["python3", "--version"])
    assert "Python 3.11" in result.stdout


def test_pip_installed():
    """Test that pip is installed."""
    result = run_docker_command(["pip3", "--version"])
    assert "pip" in result.stdout


def test_git_installed():
    """Test that git is installed."""
    result = run_docker_command(["git", "--version"])
    assert "git version" in result.stdout


def test_curl_installed():
    """Test that curl is installed."""
    result = run_docker_command(["curl", "--version"])
    assert "curl" in result.stdout


def test_jq_installed():
    """Test that jq is installed."""
    result = run_docker_command(["jq", "--version"])
    assert result.returncode == 0


def test_rust_installed():
    """Test that Rust and Cargo are installed."""
    result = run_docker_command(["rustc", "--version"])
    assert "rustc" in result.stdout
    
    result = run_docker_command(["cargo", "--version"])
    assert "cargo" in result.stdout


def test_go_installed():
    """Test that Go is installed."""
    result = run_docker_command(["go", "version"])
    assert "go version" in result.stdout


def test_node_installed():
    """Test that Node.js is installed."""
    result = run_docker_command(["node", "--version"])
    assert "v18." in result.stdout
    
    result = run_docker_command(["npm", "--version"])
    assert result.returncode == 0


def test_docker_cli_installed():
    """Test that Docker CLI is installed."""
    result = run_docker_command(["docker", "--version"])
    assert "Docker version" in result.stdout


def test_workspace_mounted():
    """Test that the workspace directory is properly mounted."""
    result = run_docker_command(["ls", "/workspace/README.md"])
    assert result.returncode == 0


def test_make_installed():
    """Test that make is installed."""
    result = run_docker_command(["make", "--version"])
    assert "GNU Make" in result.stdout


def test_vim_installed():
    """Test that vim is installed."""
    result = run_docker_command(["vim", "--version"])
    assert "Vi IMproved" in result.stdout


def test_tmux_installed():
    """Test that tmux is installed."""
    result = run_docker_command(["tmux", "-V"])
    assert "tmux" in result.stdout


def test_workspace_permissions():
    """Test that we can create and modify files in the workspace."""
    # Create a test file
    result = run_docker_command(["touch", "/workspace/test_file.txt"])
    assert result.returncode == 0
    
    # Write to it
    result = run_docker_command(["echo", "test content", ">", "/workspace/test_file.txt"])
    assert result.returncode == 0
    
    # Read it back
    result = run_docker_command(["cat", "/workspace/test_file.txt"])
    assert "test content" in result.stdout
    
    # Clean up
    result = run_docker_command(["rm", "/workspace/test_file.txt"])
    assert result.returncode == 0
