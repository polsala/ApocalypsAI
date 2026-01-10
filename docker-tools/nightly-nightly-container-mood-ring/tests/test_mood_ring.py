import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
import docker # Import docker to mock its exceptions

# Import the functions to be tested
from mood_ring import determine_mood, get_container_stats, get_container_logs, \
                      CPU_HIGH_THRESHOLD, MEM_HIGH_THRESHOLD, \
                      LOG_WARNING_KEYWORDS, LOG_ERROR_KEYWORDS

# Mock rationale: We need to simulate various container states and outputs without
# actually running Docker containers or interacting with a Docker daemon.
# This ensures tests are deterministic, fast, and offline.

@pytest.fixture
def mock_container_attrs_running():
    """Mock container attributes for a running container."""
    return {
        'Id': 'abc123def456',
        'Name': '/test-container',
        'State': {
            'Status': 'running',
            'Running': True,
            'Paused': False,
            'Restarting': False,
            'OOMKilled': False,
            'Dead': False,
            'Pid': 12345,
            'ExitCode': 0,
            'Error': '',
            'StartedAt': (datetime.now() - timedelta(hours=1)).isoformat() + 'Z',
            'FinishedAt': '0001-01-01T00:00:00Z',
            'RestartCount': 0
        },
        'Status': 'Up 1 hour'
    }

@pytest.fixture
def mock_container_attrs_stopped():
    """Mock container attributes for a gracefully stopped container."""
    attrs = mock_container_attrs_running()
    attrs['State']['Status'] = 'exited'
    attrs['State']['Running'] = False
    attrs['State']['ExitCode'] = 0
    attrs['Status'] = 'Exited (0) 10 minutes ago'
    return attrs

@pytest.fixture
def mock_container_attrs_failed():
    """Mock container attributes for a failed container."""
    attrs = mock_container_attrs_running()
    attrs['State']['Status'] = 'exited'
    attrs['State']['Running'] = False
    attrs['State']['ExitCode'] = 1
    attrs['Status'] = 'Exited (1) 5 minutes ago'
    return attrs

@pytest.fixture
def mock_container_attrs_restarted():
    """Mock container attributes for a container that has restarted."""
    attrs = mock_container_attrs_running()
    attrs['State']['RestartCount'] = 2
    attrs['State']['StartedAt'] = (datetime.now() - timedelta(minutes=1)).isoformat() + 'Z' # Recently started
    return attrs

# --- Test determine_mood function ---

def test_determine_mood_jubilant(mock_container_attrs_running):
    # Mock rationale: Simulate a healthy container with recent log activity.
    mood, reason = determine_mood(mock_container_attrs_running, 10.0, 20.0, [], [], True)
    assert mood == "Jubilant"
    assert "recent activity" in reason

def test_determine_mood_serene(mock_container_attrs_running):
    # Mock rationale: Simulate a healthy container with normal usage and no recent log activity.
    mood, reason = determine_mood(mock_container_attrs_running, 10.0, 20.0, [], [], False)
    assert mood == "Serene"
    assert "Normal operation" in reason

def test_determine_mood_bored(mock_container_attrs_running):
    # Mock rationale: Simulate a container with very low usage and no log activity.
    mood, reason = determine_mood(mock_container_attrs_running, 1.0, 2.0, [], [], False)
    assert mood == "Bored"
    assert "Very low resource usage" in reason

def test_determine_mood_anxious_cpu(mock_container_attrs_running):
    # Mock rationale: Simulate high CPU usage.
    mood, reason = determine_mood(mock_container_attrs_running, CPU_HIGH_THRESHOLD + 5, 20.0, [], [], True)
    assert mood == "Anxious"
    assert "High CPU usage" in reason

def test_determine_mood_anxious_mem(mock_container_attrs_running):
    # Mock rationale: Simulate high memory usage.
    mood, reason = determine_mood(mock_container_attrs_running, 10.0, MEM_HIGH_THRESHOLD + 5, [], [], True)
    assert mood == "Anxious"
    assert "High Memory usage" in reason

def test_determine_mood_anxious_both(mock_container_attrs_running):
    # Mock rationale: Simulate high CPU and memory usage.
    mood, reason = determine_mood(mock_container_attrs_running, CPU_HIGH_THRESHOLD + 5, MEM_HIGH_THRESHOLD + 5, [], [], True)
    assert mood == "Anxious"
    assert "High CPU" in reason and "High Memory" in reason

def test_determine_mood_grumpy(mock_container_attrs_running):
    # Mock rationale: Simulate warnings in logs.
    mood, reason = determine_mood(mock_container_attrs_running, 10.0, 20.0, ["Warning: something happened"], [], True)
    assert mood == "Grumpy"
    assert "Warnings detected" in reason

def test_determine_mood_distressed(mock_container_attrs_running):
    # Mock rationale: Simulate errors in logs.
    mood, reason = determine_mood(mock_container_attrs_running, 10.0, 20.0, [], ["Error: critical failure"], True)
    assert mood == "Distressed"
    assert "Errors detected" in reason

def test_determine_mood_fickle(mock_container_attrs_restarted):
    # Mock rationale: Simulate a container that has restarted.
    mood, reason = determine_mood(mock_container_attrs_restarted, 10.0, 20.0, [], [], True)
    assert mood == "Fickle"
    assert "Has restarted 2 times" in reason

def test_determine_mood_asleep(mock_container_attrs_stopped):
    # Mock rationale: Simulate a gracefully stopped container.
    mood, reason = determine_mood(mock_container_attrs_stopped, 0.0, 0.0, [], [], False)
    assert mood == "Asleep"
    assert "Exited gracefully" in reason

def test_determine_mood_deceased(mock_container_attrs_failed):
    # Mock rationale: Simulate a failed container.
    mood, reason = determine_mood(mock_container_attrs_failed, 0.0, 0.0, [], [], False)
    assert mood == "Deceased"
    assert "Exited with status 1" in reason

# --- Test get_container_stats function ---

def test_get_container_stats_no_stats():
    # Mock rationale: Simulate a container with no stats available.
    mock_container = Mock()
    mock_container.stats.return_value = {}
    cpu, mem = get_container_stats(mock_container)
    assert cpu == 0.0
    assert mem == 0.0

def test_get_container_stats_valid_data():
    # Mock rationale: Simulate realistic CPU and memory stats.
    mock_container = Mock()
    mock_container.stats.return_value = {
        'cpu_stats': {
            'cpu_usage': {'total_usage': 100000000, 'percpu_usage': [50000000, 50000000]},
            'system_cpu_usage': 200000000
        },
        'precpu_stats': {
            'cpu_usage': {'total_usage': 0, 'percpu_usage': [0, 0]},
            'system_cpu_usage': 0
        },
        'memory_stats': {
            'usage': 500000000, # 500MB
            'limit': 1000000000 # 1GB
        }
    }
    cpu, mem = get_container_stats(mock_container)
    # CPU: (100M / 200M) * 2 cores * 100 = 100%
    assert cpu == pytest.approx(100.0)
    assert mem == pytest.approx(50.0) # 500MB / 1GB = 0.5 * 100 = 50%

def test_get_container_stats_zero_limit():
    # Mock rationale: Simulate a container with memory limit as zero (unlimited).
    mock_container = Mock()
    mock_container.stats.return_value = {
        'cpu_stats': {
            'cpu_usage': {'total_usage': 100000000, 'percpu_usage': [50000000, 50000000]},
            'system_cpu_usage': 200000000
        },
        'precpu_stats': {
            'cpu_usage': {'total_usage': 0, 'percpu_usage': [0, 0]},
            'system_cpu_usage': 0
        },
        'memory_stats': {
            'usage': 500000000,
            'limit': 0 # Unlimited memory
        }
    }
    cpu, mem = get_container_stats(mock_container)
    assert cpu == pytest.approx(100.0)
    assert mem == 0.0 # Should be 0 if limit is 0

# --- Test get_container_logs function ---

def test_get_container_logs_no_logs():
    # Mock rationale: Simulate a container with no recent logs.
    mock_container = Mock()
    mock_container.logs.return_value = b''
    warnings, errors, activity = get_container_logs(mock_container)
    assert not warnings
    assert not errors
    assert not activity

def test_get_container_logs_with_warnings():
    # Mock rationale: Simulate logs containing warning keywords.
    mock_container = Mock()
    mock_container.logs.return_value = b'INFO: All good\nWARNING: This is a warning\nDEBUG: More info'
    warnings, errors, activity = get_container_logs(mock_container)
    assert len(warnings) == 1
    assert "WARNING: This is a warning" in warnings
    assert not errors
    assert activity

def test_get_container_logs_with_errors():
    # Mock rationale: Simulate logs containing error keywords.
    mock_container = Mock()
    mock_container.logs.return_value = b'INFO: All good\nERROR: Something failed\nDEBUG: More info'
    warnings, errors, activity = get_container_logs(mock_container)
    assert not warnings
    assert len(errors) == 1
    assert "ERROR: Something failed" in errors
    assert activity

def test_get_container_logs_with_mixed():
    # Mock rationale: Simulate logs containing both warnings and errors.
    mock_container = Mock()
    mock_container.logs.return_value = b'WARN: Issue here\nCRITICAL: System down\nINFO: OK'
    warnings, errors, activity = get_container_logs(mock_container)
    assert len(warnings) == 1
    assert "WARN: Issue here" in warnings
    assert len(errors) == 1
    assert "CRITICAL: System down" in errors
    assert activity

def test_get_container_logs_exception_handling():
    # Mock rationale: Simulate an error when trying to fetch logs (e.g., container not running or permissions).
    mock_container = Mock()
    mock_container.logs.side_effect = docker.errors.APIError("Cannot fetch logs")
    warnings, errors, activity = get_container_logs(mock_container)
    assert not warnings
    assert not errors
    assert not activity # No activity if logs can't be fetched
