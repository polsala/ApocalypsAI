// Integration tests for nightly-future-timestamp
// These tests invoke the public `add_duration` function directly,
// ensuring deterministic behavior without needing to mock system time.

use nightly_future_timestamp::add_duration;
use chrono::{TimeZone, Utc};

#[test]
fn integration_future_timestamp() {
    let base = Utc.ymd(2022, 12, 31).and_hms(23, 0, 0);
    let result = add_duration(base, "1h30m").expect("should compute future time");
    let expected = Utc.ymd(2023, 1, 1).and_hms(0, 30, 0);
    assert_eq!(result, expected);
}
