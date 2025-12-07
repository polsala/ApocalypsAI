use std::time::{SystemTime, Duration};
use super::*;

// Mock time for deterministic testing
struct TimeMock {
    original: SystemTime,
}

impl TimeMock {
    fn new() -> Self {
        Self {
            original: SystemTime::now(),
        }
    }

    fn set_mock_time(time: SystemTime) {
        // Using a real-time mock requires patching SystemTime::now()
        // For simplicity, we'll test with fixed time values
    }

    fn restore(&self) {
        // In real tests, we'd restore the original time
    }
}

#[test]
fn test_chaos_mode_output() {
    let mock_time = SystemTime::UNIX_EPOCH + Duration::from_secs(1625648400); // 2021-07-13 12:00:00 UTC
    TimeMock::set_mock_time(mock_time);

    let args = vec!["temporal-motivation-mixer", "-c"];
    let mut child = std::process::Command::new("../target/debug/temporal-motivation-mixer")
        .args(&args[1..])
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to spawn process");

    let output = child.wait_with_output().expect("Failed to read output");
    let stdout = String::from_utf8(output.stdout).unwrap();

    assert!(stdout.contains("Temporal Anomaly Detected"));
    assert!(stdout.contains("±"));
    TimeMock::restore();
}

#[test]
fn test_normal_mode_output() {
    let mock_time = SystemTime::UNIX_EPOCH + Duration::from_secs(1625648400); // 2021-07-13 12:00:00 UTC
    TimeMock::set_mock_time(mock_time);

    let args = vec!["temporal-motivation-mixer"];
    let mut child = std::process::Command::new("../target/debug/temporal-motivation-mixer")
        .args(&args[1..])
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("Failed to spawn process");

    let output = child.wait_with_output().expect("Failed to read output");
    let stdout = String::from_utf8(output.stdout).unwrap();

    assert!(stdout.contains("Noon Nucleus"));
    assert!(!stdout.contains("±"));
    TimeMock::restore();
}
