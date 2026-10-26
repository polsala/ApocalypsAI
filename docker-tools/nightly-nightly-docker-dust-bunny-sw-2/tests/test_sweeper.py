import pytest
import subprocess
from unittest.mock import MagicMock, patch
from src.dust_bunny_sweeper import get_dangling_images, get_unused_volumes, get_exited_containers, generate_report

# Mock rationale: To ensure deterministic and offline testing, actual Docker commands are mocked.
# This allows verification of the script's parsing, filtering, and reporting logic without requiring a live Docker daemon or modifying the host system.

@pytest.fixture
def mock_subprocess_run():
    with patch('subprocess.run') as mock_run:
        yield mock_run

def test_get_dangling_images_no_images(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout='', stderr='', returncode=0)
    images = get_dangling_images()
    assert images == []
    mock_subprocess_run.assert_called_once_with(['docker', 'images', '-f', 'dangling=true', '--format', '{{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedSince}}\t{{.Size}}'], capture_output=True, text=True, check=True)

def test_get_dangling_images_with_images(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout='<none>\t<none>\ta1b2c3d4e5f6\t2 weeks ago\t123MB\n<none>\t<none>\tf6e5d4c3b2a1\t3 months ago\t456MB', stderr='', returncode=0)
    images = get_dangling_images()
    assert len(images) == 2
    assert images[0]['id'] == 'a1b2c3d4e5f6'
    assert images[0]['size'] == '123MB'
    assert images[1]['id'] == 'f6e5d4c3b2a1'
    assert images[1]['size'] == '456MB'
    mock_subprocess_run.assert_called_once_with(['docker', 'images', '-f', 'dangling=true', '--format', '{{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.CreatedSince}}\t{{.Size}}'], capture_output=True, text=True, check=True)

def test_get_unused_volumes_no_volumes(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout='', stderr='', returncode=0)
    volumes = get_unused_volumes()
    assert volumes == []
    mock_subprocess_run.assert_called_once_with(['docker', 'volume', 'ls', '-f', 'dangling=true', '--format', '{{.Name}}'], capture_output=True, text=True, check=True)

def test_get_unused_volumes_with_volumes(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout='my_old_data_volume\ntemp_logs_volume', stderr='', returncode=0)
    volumes = get_unused_volumes()
    assert volumes == ['my_old_data_volume', 'temp_logs_volume']

def test_get_exited_containers_no_containers(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout='', stderr='', returncode=0)
    containers = get_exited_containers()
    assert containers == []
    mock_subprocess_run.assert_called_once_with(['docker', 'ps', '-a', '-f', 'status=exited', '--format', '{{.Names}}\t{{.Status}}'], capture_output=True, text=True, check=True)

def test_get_exited_containers_with_containers(mock_subprocess_run):
    mock_subprocess_run.return_value = MagicMock(stdout='container_alpha\texited 0\ncontainer_beta\texited 137', stderr='', returncode=0)
    containers = get_exited_containers()
    assert len(containers) == 2
    assert containers[0]['name'] == 'container_alpha'
    assert containers[0]['status'] == 'exited 0'
    assert containers[1]['name'] == 'container_beta'
    assert containers[1]['status'] == 'exited 137'

def test_generate_report_all_clear():
    report = generate_report([], [], [])
    assert "All Clear! (No Dust Bunnies Found)" in report
    assert "Your Docker environment is sparkling clean!" in report

def test_generate_report_with_all_types():
    dangling_images = [
        {'repo': '<none>', 'tag': '<none>', 'id': 'img1', 'created_since': '2 weeks ago', 'size': '100MB'}
    ]
    unused_volumes = ['vol1']
    exited_containers = [
        {'name': 'cont1', 'status': 'exited 0'}
    ]
    report = generate_report(dangling_images, unused_volumes, exited_containers)

    assert "Dangling Images (Forgotten Phantoms)" in report
    assert "img1" in report
    assert "docker rmi img1" in report

    assert "Unused Volumes (Lost Luggage)" in report
    assert "vol1" in report
    assert "docker volume rm vol1" in report

    assert "Exited Containers (Lingering Spirits)" in report
    assert "cont1 (exited 0)" in report
    assert "docker rm cont1" in report

    assert "Grand Cleanup Suggestion" in report
    assert "docker system prune" in report

def test_generate_report_only_images():
    dangling_images = [
        {'repo': '<none>', 'tag': '<none>', 'id': 'img1', 'created_since': '2 weeks ago', 'size': '100MB'}
    ]
    report = generate_report(dangling_images, [], [])
    assert "Dangling Images (Forgotten Phantoms)" in report
    assert "No unused volumes found" in report
    assert "No exited containers found" in report
    assert "docker rmi img1" in report
    assert "docker image prune" in report # Specific prune for images
    assert "docker system prune" in report

def test_generate_report_only_volumes():
    unused_volumes = ['vol1']
    report = generate_report([], unused_volumes, [])
    assert "No dangling images found" in report
    assert "Unused Volumes (Lost Luggage)" in report
    assert "No exited containers found" in report
    assert "docker volume rm vol1" in report
    assert "docker volume prune" in report # Specific prune for volumes
    assert "docker system prune" in report

def test_generate_report_only_containers():
    exited_containers = [
        {'name': 'cont1', 'status': 'exited 0'}
    ]
    report = generate_report([], [], exited_containers)
    assert "No dangling images found" in report
    assert "No unused volumes found" in report
    assert "Exited Containers (Lingering Spirits)" in report
    assert "docker rm cont1" in report
    assert "docker container prune" in report # Specific prune for containers
    assert "docker system prune" in report
