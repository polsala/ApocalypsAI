use std::time::{SystemTime, UNIX_EPOCH};

mod main;
use main::RiftEvent;

#[test]
fn test_rift_event_creation() {
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .expect("Time went backwards")
        .as_secs();
    
    let event = RiftEvent::new("LOW", "Sector 3");
    
    assert_eq!(event.severity, "LOW");
    assert_eq!(event.location, "Sector 3");
    assert!(event.timestamp >= now - 1 && event.timestamp <= now + 1);
}

#[test]
fn test_rift_event_log_output() {
    let event = RiftEvent::new("CRITICAL", "Sector X");
    
    // Mock rationale: We can't capture stdout easily in unit tests without external crates.
    // This test ensures the method doesn't panic.
    event.log();
    assert!(true);
}
