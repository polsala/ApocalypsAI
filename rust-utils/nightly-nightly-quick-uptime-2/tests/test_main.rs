use nightly_quick_uptime::format_uptime;

#[test]
fn test_format_uptime_zero() {
    assert_eq!(format_uptime(0), "0 days, 0 hours, 0 minutes, 0 seconds");
}

#[test]
fn test_format_uptime_example() {
    // 1 day, 2 hours, 3 minutes, 4 seconds = 1*86400 + 2*3600 + 3*60 + 4 = 93784
    let seconds = 1 * 86400 + 2 * 3600 + 3 * 60 + 4;
    assert_eq!(format_uptime(seconds), "1 days, 2 hours, 3 minutes, 4 seconds");
}
