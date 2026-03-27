import pytest
import subprocess
import json
from unittest.mock import patch, MagicMock
from src.main import (
    run_docker_command,
    get_dangling_images,
    get_exited_containers,
    get_unused_volumes,
    get_system_df,
    generate_report,
    generate_prune_suggestions,
    main
)

# Mock rationale: subprocess.run interacts with the host's Docker daemon,
# which is an external dependency. For deterministic and offline tests,
# we must mock its behavior to return predefined outputs.

@patch('subprocess.run')
def test_run_docker_command_success(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout="success output", stderr="", returncode=0)
    result = run_docker_command(["docker", "info"])
    assert result == "success output"
    mock_subprocess_run.assert_called_once_with(
        ["docker", "info"], check=True, capture_output=True, text=True, encoding='utf-8'
    )

@patch('subprocess.run')
def test_run_docker_command_error(mock_subprocess_run, capsys):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd=["docker", "fail"], stderr="error output"
    )
    with pytest.raises(SystemExit) as excinfo:
        run_docker_command(["docker", "fail"])
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error running command: docker fail" in captured.stderr
    assert "Stderr: error output" in captured.stderr

@patch('subprocess.run')
def test_run_docker_command_not_found(mock_subprocess_run, capsys):
    mock_subprocess_run.side_effect = FileNotFoundError
    with pytest.raises(SystemExit) as excinfo:
        run_docker_command(["docker", "nonexistent"])
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: 'docker' command not found." in captured.stderr

@patch('src.main.run_docker_command')
def test_get_dangling_images(mock_run_docker_command):
    mock_run_docker_command.return_value = "img1\nimg2"
    images = get_dangling_images()
    assert images == ["img1", "img2"]
    mock_run_docker_command.assert_called_once_with(["docker", "images", "-f", "dangling=true", "-q"])

@patch('src.main.run_docker_command')
def test_get_dangling_images_empty(mock_run_docker_command):
    mock_run_docker_command.return_value = ""
    images = get_dangling_images()
    assert images == []

@patch('src.main.run_docker_command')
def test_get_exited_containers(mock_run_docker_command):
    mock_run_docker_command.return_value = "cont1\ncont2"
    containers = get_exited_containers()
    assert containers == ["cont1", "cont2"]
    mock_run_docker_command.assert_called_once_with(["docker", "ps", "-a", "-f", "status=exited", "-q"])

@patch('src.main.run_docker_command')
def test_get_unused_volumes(mock_run_docker_command):
    mock_run_docker_command.return_value = "vol1\nvol2"
    volumes = get_unused_volumes()
    assert volumes == ["vol1", "vol2"]
    mock_run_docker_command.assert_called_once_with(["docker", "volume", "ls", "-f", "dangling=true", "-q"])

@patch('src.main.run_docker_command')
def test_get_system_df(mock_run_docker_command):
    mock_run_docker_command.return_value = (
        json.dumps({"Type": "Images", "Total": "2", "Size": "100MB", "Reclaimable": "50MB"}) + "\n" +
        json.dumps({"Type": "Containers", "Total": "5", "Size": "20MB", "Reclaimable": "10MB"})
    )
    df = get_system_df()
    assert df == {
        "Images": {"Type": "Images", "Total": "2", "Size": "100MB", "Reclaimable": "50MB"},
        "Containers": {"Type": "Containers", "Total": "5", "Size": "20MB", "Reclaimable": "10MB"}
    }
    mock_run_docker_command.assert_called_once_with(["docker", "system", "df", "--format", "{{json .}}"])

def test_generate_report_with_items():
    dangling_images = ["img1"]
    exited_containers = ["cont1"]
    unused_volumes = ["vol1"]
    system_df = {
        "Images": {"Type": "Images", "Size": "100MB", "Reclaimable": "50MB"}
    }
    report = generate_report(dangling_images, exited_containers, unused_volumes, system_df)
    assert "🌱 Dangling Images (1 found):" in report
    assert "- Image ID: img1" in report
    assert "🥀 Exited Containers (1 found):" in report
    assert "- Container ID: cont1" in report
    assert "🏺 Unused Volumes (1 found):" in report
    assert "- Volume Name: vol1" in report
    assert "🌳 Images: 100MB (Reclaimable: 50MB)" in report

def test_generate_report_no_items():
    dangling_images = []
    exited_containers = []
    unused_volumes = []
    system_df = {
        "Images": {"Type": "Images", "Size": "0B", "Reclaimable": "0B"}
    }
    report = generate_report(dangling_images, exited_containers, unused_volumes, system_df)
    assert "✨ Your garden is pristine! No digital weeds found." in report
    assert "🌳 Images: 0B (Reclaimable: 0B)" in report

def test_generate_prune_suggestions_with_items():
    dangling_images = ["img1"]
    exited_containers = ["cont1"]
    unused_volumes = ["vol1"]
    suggestions = generate_prune_suggestions(dangling_images, exited_containers, unused_volumes)
    assert "✂️ Suggested Pruning Tools ✂️" in suggestions
    assert "docker system prune" in suggestions
    assert "docker rmi img1" in suggestions
    assert "docker rm cont1" in suggestions
    assert "docker volume rm vol1" in suggestions

def test_generate_prune_suggestions_no_items():
    dangling_images = []
    exited_containers = []
    unused_volumes = []
    suggestions = generate_prune_suggestions(dangling_images, exited_containers, unused_volumes)
    assert "No pruning needed! Your garden is perfectly manicured." in suggestions

@patch('src.main.run_docker_command')
@patch('src.main.get_dangling_images')
@patch('src.main.get_exited_containers')
@patch('src.main.get_unused_volumes')
@patch('src.main.get_system_df')
@patch('builtins.print') # Mock print to capture output
def test_main_dry_run(mock_print, mock_get_system_df, mock_get_unused_volumes,
                      mock_get_exited_containers, mock_get_dangling_images,
                      mock_run_docker_command):
    # Mock rationale: We need to control the output of the Docker commands
    # and verify that the report and suggestions are generated correctly
    # without actually executing Docker commands or printing to console.
    mock_get_dangling_images.return_value = ["img1"]
    mock_get_exited_containers.return_value = ["cont1"]
    mock_get_unused_volumes.return_value = ["vol1"]
    mock_get_system_df.return_value = {"Images": {"Type": "Images", "Size": "100MB", "Reclaimable": "50MB"}}
    mock_run_docker_command.return_value = "" # Ensure no actual prune command runs

    main()

    # Verify that report and suggestions are generated and printed
    assert any("🌱 Dangling Images (1 found):" in call.args[0] for call in mock_print.call_args_list)
    assert any("✂️ Suggested Pruning Tools ✂️" in call.args[0] for call in mock_print.call_args_list)
    # Ensure prune command was NOT called
    # run_docker_command is called by get_* functions, but not for the prune action itself in dry run
    # We check that it's not called with the prune specific arguments
    assert not any("prune" in arg for call in mock_run_docker_command.call_args_list for arg in call.args[0])

@patch('src.main.run_docker_command')
@patch('src.main.get_dangling_images')
@patch('src.main.get_exited_containers')
@patch('src.main.get_unused_volumes')
@patch('src.main.get_system_df')
@patch('builtins.print') # Mock print to capture output
def test_main_prune_mode(mock_print, mock_get_system_df, mock_get_unused_volumes,
                         mock_get_exited_containers, mock_get_dangling_images,
                         mock_run_docker_command):
    # Mock rationale: Similar to dry run, we mock Docker command outputs.
    # Additionally, we mock the `docker system prune` call to ensure it's
    # invoked correctly when `--prune` is passed.
    mock_get_dangling_images.return_value = ["img1"]
    mock_get_exited_containers.return_value = ["cont1"]
    mock_get_unused_volumes.return_value = ["vol1"]
    mock_get_system_df.return_value = {"Images": {"Type": "Images", "Size": "100MB", "Reclaimable": "50MB"}}
    # Mock the prune command specifically
    mock_run_docker_command.return_value = "Total reclaimed space: 150MB"

    # Simulate command line arguments
    with patch('sys.argv', ['main.py', '--prune']):
        main()

    # Verify that report is generated and prune command is called
    assert any("🌱 Dangling Images (1 found):" in call.args[0] for call in mock_print.call_args_list)
    assert any("Initiating garden pruning..." in call.args[0] for call in mock_print.call_args_list)
    assert any("Garden pruned successfully! 🌱" in call.args[0] for call in mock_print.call_args_list)
    # Check that run_docker_command was called with the prune command
    mock_run_docker_command.assert_any_call(["docker", "system", "prune", "-f"], capture_output=False)

@patch('src.main.run_docker_command')
@patch('src.main.get_dangling_images')
@patch('src.main.get_exited_containers')
@patch('src.main.get_unused_volumes')
@patch('src.main.get_system_df')
@patch('builtins.print')
def test_main_prune_mode_error(mock_print, mock_get_system_df, mock_get_unused_volumes,
                               mock_get_exited_containers, mock_get_dangling_images,
                               mock_run_docker_command, capsys):
    # Mock rationale: Test error handling during the prune operation.
    mock_get_dangling_images.return_value = ["img1"]
    mock_get_exited_containers.return_value = ["cont1"]
    mock_get_unused_volumes.return_value = ["vol1"]
    mock_get_system_df.return_value = {"Images": {"Type": "Images", "Size": "100MB", "Reclaimable": "50MB"}}
    # Simulate an error during prune
    mock_run_docker_command.side_effect = Exception("Prune failed!")

    with patch('sys.argv', ['main.py', '--prune']):
        with pytest.raises(SystemExit) as excinfo:
            main()
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error during pruning: Prune failed!" in captured.stderr
