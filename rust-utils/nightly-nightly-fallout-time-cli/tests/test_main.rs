use nightly_fallout_time_cli::format_fallout;

#[test]
fn test_known_timestamp() {
    // 1970‑01‑02T03:04:00Z => day 1, 03:04
    let ts = "1970-01-02T03:04:00Z";
    let result = format_fallout(ts).unwrap();
    assert_eq!(result, "Day 1, 03:04 after the fallout");
}

#[test]
fn test_invalid_timestamp() {
    let ts = "invalid-timestamp";
    assert!(format_fallout(ts).is_err());
}
