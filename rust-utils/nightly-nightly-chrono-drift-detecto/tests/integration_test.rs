use super::{run_detector, TimeProvider}; // Import run_detector and TimeProvider from main.rs
use chrono::{Utc, Duration};
use std::error::Error;
use std::io::Cursor;

// Mock implementation of TimeProvider for deterministic testing
struct MockTimeProvider {
    local_time: chrono::DateTime<Utc>,
    ntp_time: Result<chrono::DateTime<Utc>, Box<dyn Error>>,
}

impl TimeProvider for MockTimeProvider {
    fn get_local_time(&self) -> chrono::DateTime<Utc> {
        self.local_time
    }

    fn get_ntp_time(&self, _server: &str, _timeout_secs: u64) -> Result<chrono::DateTime<Utc>, Box<dyn Error>> {
        // Mock rationale: We are simulating NTP server responses for deterministic testing
        // without actual network calls. This allows us to control the "network time"
        // for various test scenarios (no drift, positive drift, negative drift, error).
        self.ntp_time.clone().map_err(|e| format!("{}", e).into())
    }
}

#[test]
fn test_no_drift() {
    let fixed_time = Utc::now();
    let provider = MockTimeProvider {
        local_time: fixed_time,
        ntp_time: Ok(fixed_time),
    };

    let mut buffer = Cursor::new(Vec::new());
    // Mock rationale: Redirect stdout to a buffer to capture output for assertion.
    // This allows testing the CLI output without actual console interaction.
    run_detector(&provider, "mock.ntp.org", 1, &mut buffer).unwrap();
    let output = String::from_utf8(buffer.into_inner()).unwrap();

    assert!(output.contains("Status: Stable. The fabric of spacetime holds firm."));
    assert!(output.contains("Observed Temporal Offset: 0 milliseconds"));
    assert!(output.contains("perfectly aligned"));
}

#[test]
fn test_positive_drift() {
    let local_time = Utc::now();
    let ntp_time = local_time + Duration::seconds(2); // NTP is 2 seconds ahead
    let provider = MockTimeProvider {
        local_time,
        ntp_time: Ok(ntp_time),
    };

    let mut buffer = Cursor::new(Vec::new());
    // Mock rationale: Redirect stdout to a buffer to capture output for assertion.
    run_detector(&provider, "mock.ntp.org", 1, &mut buffer).unwrap();
    let output = String::from_utf8(buffer.into_inner()).unwrap();

    assert!(output.contains("Status: Minor Drift. A slight tremor in the chronal flow."));
    assert!(output.contains("Observed Temporal Offset: 2000 milliseconds"));
    assert!(output.contains("lagging behind the cosmic pulse."));
}

#[test]
fn test_negative_drift() {
    let local_time = Utc::now();
    let ntp_time = local_time - Duration::minutes(5); // NTP is 5 minutes behind
    let provider = MockTimeProvider {
        local_time,
        ntp_time: Ok(ntp_time),
    };

    let mut buffer = Cursor::new(Vec::new());
    // Mock rationale: Redirect stdout to a buffer to capture output for assertion.
    run_detector(&provider, "mock.ntp.org", 1, &mut buffer).unwrap();
    let output = String::from_utf8(buffer.into_inner()).unwrap();

    assert!(output.contains("Status: SIGNIFICANT DRIFT DETECTED! The chronal currents are turbulent."));
    assert!(output.contains("Observed Temporal Offset: -300000 milliseconds")); // 5 minutes = 300,000 ms
    assert!(output.contains("ahead of the cosmic pulse."));
}

#[test]
fn test_ntp_error() {
    let local_time = Utc::now();
    let provider = MockTimeProvider {
        local_time,
        ntp_time: Err("Network unreachable".into()), // Simulate network error
    };

    let mut buffer = Cursor::new(Vec::new());
    // Mock rationale: Redirect stdout to a buffer to capture output for assertion.
    // The `run_detector` function is designed to handle errors gracefully and print to the writer.
    run_detector(&provider, "mock.ntp.org", 1, &mut buffer).unwrap();
    let output = String::from_utf8(buffer.into_inner()).unwrap();

    assert!(output.contains("Status: Chronal Flux Disruption! Unable to connect to the Cosmic Chronometer at mock.ntp.org."));
    assert!(output.contains("Error: Network unreachable"));
}
