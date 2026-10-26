// Mock rationale: These tests are unit tests for the core logic function `tag_anomaly`.
// They do not require external resources or I/O, making them deterministic and offline.
// The `main` function's CLI parsing is implicitly tested by `clap` itself, and its
// output is a direct result of `tag_anomaly`, which is tested here.

use nightly_temporal_anomaly_tagger::{tag_anomaly, AnomalyType, Severity};

#[test]
fn test_tag_anomaly_basic() {
    let description = "My coffee cup briefly turned into a squirrel.";
    let anomaly_type = AnomalyType::Echo;
    let severity = Severity::Minor;
    let expected = "[ANOMALY:Echo|Minor] My coffee cup briefly turned into a squirrel.";
    assert_eq!(tag_anomaly(description, anomaly_type, severity), expected);
}

#[test]
fn test_tag_anomaly_different_types_and_severity() {
    let description = "The cat spoke Latin for a moment.";
    let anomaly_type = AnomalyType::Warp;
    let severity = Severity::Severe;
    let expected = "[ANOMALY:Warp|Severe] The cat spoke Latin for a moment.";
    assert_eq!(tag_anomaly(description, anomaly_type, severity), expected);
}

#[test]
fn test_tag_anomaly_empty_description() {
    let description = "";
    let anomaly_type = AnomalyType::Glitch;
    let severity = Severity::Trivial;
    let expected = "[ANOMALY:Glitch|Trivial] ";
    assert_eq!(tag_anomaly(description, anomaly_type, severity), expected);
}

#[test]
fn test_tag_anomaly_long_description() {
    let description = "The fabric of reality shimmered, revealing a fleeting glimpse of a dimension where all cars were made of cheese, and the sky was a perpetual disco ball, before snapping back to normal.";
    let anomaly_type = AnomalyType::Shift;
    let severity = Severity::Critical;
    let expected = "[ANOMALY:Shift|Critical] The fabric of reality shimmered, revealing a fleeting glimpse of a dimension where all cars were made of cheese, and the sky was a perpetual disco ball, before snapping back to normal.";
    assert_eq!(tag_anomaly(description, anomaly_type, severity), expected);
}
