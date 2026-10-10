use nightly_chrono_compass::{calculate_and_format_distance, parse_timestamp};
use chrono::TimeZone;

// Mock rationale: These tests directly call the public functions from the `nightly_chrono_compass`
// library with predefined string inputs, ensuring deterministic and offline execution.
// No external systems, network calls, or actual CLI execution are involved.

#[test]
fn test_same_time() {
    let start = "2023-01-01T12:00:00Z";
    let end = "2023-01-01T12:00:00Z";
    let expected = "Temporal Distance: 0 days, 0 hours, 0 minutes\n\
                    Which is approximately 0 Flickers of Eternity (1 Flicker = 1 minute)";
    assert_eq!(calculate_and_format_distance(start, end).unwrap(), expected);
}

#[test]
fn test_one_hour_difference() {
    let start = "2023-01-01T12:00:00Z";
    let end = "2023-01-01T13:00:00Z";
    let expected = "Temporal Distance: 0 days, 1 hours, 0 minutes\n\
                    Which is approximately 60 Flickers of Eternity (1 Flicker = 1 minute)";
    assert_eq!(calculate_and_format_distance(start, end).unwrap(), expected);
}

#[test]
fn test_one_day_one_hour_thirty_minutes() {
    let start = "2023-01-01T10:00:00Z";
    let end = "2023-01-02T11:30:00Z";
    let expected = "Temporal Distance: 1 days, 1 hours, 30 minutes\n\
                    Which is approximately 1530 Flickers of Eternity (1 Flicker = 1 minute)";
    assert_eq!(calculate_and_format_distance(start, end).unwrap(), expected);
}

#[test]
fn test_multiple_days_and_hours() {
    let start = "2023-01-01T00:00:00Z";
    let end = "2023-01-03T06:45:00Z";
    let expected = "Temporal Distance: 2 days, 6 hours, 45 minutes\n\
                    Which is approximately 3285 Flickers of Eternity (1 Flicker = 1 minute)";
    assert_eq!(calculate_and_format_distance(start, end).unwrap(), expected);
}

#[test]
fn test_end_before_start_error() {
    let start = "2023-01-02T12:00:00Z";
    let end = "2023-01-01T12:00:00Z";
    assert_eq!(calculate_and_format_distance(start, end).unwrap_err(), "End time cannot be before start time.".to_string());
}

#[test]
fn test_invalid_start_time_format() {
    let start = "not-a-time";
    let end = "2023-01-01T12:00:00Z";
    assert!(calculate_and_format_distance(start, end).is_err());
    assert_eq!(calculate_and_format_distance(start, end).unwrap_err(), String::from("Failed to parse timestamp: 'not-a-time'. Expected formats like 'YYYY-MM-DDTHH:MM:SSZ', 'YYYY-MM-DD HH:MM:SS UTC', or 'YYYY-MM-DD HH:MM:SS'."));
}

#[test]
fn test_invalid_end_time_format() {
    let start = "2023-01-01T12:00:00Z";
    let end = "another-bad-time";
    assert!(calculate_and_format_distance(start, end).is_err());
    assert_eq!(calculate_and_format_distance(start, end).unwrap_err(), String::from("Failed to parse timestamp: 'another-bad-time'. Expected formats like 'YYYY-MM-DDTHH:MM:SSZ', 'YYYY-MM-DD HH:MM:SS UTC', or 'YYYY-MM-DD HH:MM:SS'."));
}

#[test]
fn test_different_valid_formats() {
    let start = "2023-01-01 10:00:00 UTC";
    let end = "2023-01-01T11:00:00Z";
    let expected = "Temporal Distance: 0 days, 1 hours, 0 minutes\n\
                    Which is approximately 60 Flickers of Eternity (1 Flicker = 1 minute)";
    assert_eq!(calculate_and_format_distance(start, end).unwrap(), expected);

    let start_no_tz = "2023-01-01 10:00:00"; // Assumed UTC
    let end_no_tz = "2023-01-01 11:00:00"; // Assumed UTC
    assert_eq!(calculate_and_format_distance(start_no_tz, end_no_tz).unwrap(), expected);
}
