use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug)]
pub struct RiftEvent {
    pub timestamp: u64,
    pub severity: String,
    pub location: String,
}

impl RiftEvent {
    pub fn new(severity: &str, location: &str) -> Self {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards")
            .as_secs();
        RiftEvent {
            timestamp,
            severity: severity.to_string(),
            location: location.to_string(),
        }
    }

    pub fn log(&self) {
        println!(
            "{{\"timestamp\": {}, \"severity\": \"{}\", \"location\": \"{}\"}}",
            self.timestamp, self.severity, self.location
        );
    }
}

fn main() {
    let event = RiftEvent::new("HIGH", "Sector 7");
    event.log();
}
