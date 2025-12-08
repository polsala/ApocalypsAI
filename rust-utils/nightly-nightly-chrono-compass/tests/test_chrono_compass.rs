use std::time::Duration;
use nightly_chrono_compass::get_temporal_status; // Import the public function from the library

// Mock rationale: We mock the system uptime retrieval by directly providing
// std::time::Duration values to the core logic function `get_temporal_status`.
// This ensures tests are deterministic and do not rely on actual system state or platform-specific calls.

#[test]
fn test_temporal_status_perfectly_aligned() {
    let uptime = Duration::from_secs(30 * 60); // 30 minutes
    let status = get_temporal_status(uptime);
    assert!(status.contains("Uptime: 0h 30m 0s"));
    assert!(status.contains("Perfectly Aligned with the Chrono-Flow."));
}

#[test]
fn test_temporal_status_slightly_drifting() {
    let uptime = Duration::from_secs(12 * 3600 + 30 * 60); // 12 hours 30 minutes
    let status = get_temporal_status(uptime);
    assert!(status.contains("Uptime: 12h 30m 0s"));
    assert!(status.contains("Slightly Drifting, but within acceptable parameters."));
}

#[test]
fn test_temporal_status_temporal_anomaly() {
    let uptime = Duration::from_secs(30 * 3600 + 15 * 60); // 30 hours 15 minutes
    let status = get_temporal_status(uptime);
    assert!(status.contains("Uptime: 30h 15m 0s"));
    assert!(status.contains("Temporal Anomaly Detected! Consider a system reboot for realignment."));
}

#[test]
fn test_temporal_status_critical_instability() {
    let uptime = Duration::from_secs(80 * 3600 + 5 * 60); // 80 hours 5 minutes
    let status = get_temporal_status(uptime);
    assert!(status.contains("Uptime: 80h 5m 0s"));
    assert!(status.contains("Critical Temporal Instability! Seek immediate system recalibration!"));
}

#[test]
fn test_temporal_status_zero_uptime() {
    let uptime = Duration::from_secs(0);
    let status = get_temporal_status(uptime);
    assert!(status.contains("Uptime: 0h 0m 0s"));
    assert!(status.contains("Perfectly Aligned with the Chrono-Flow."));
}
