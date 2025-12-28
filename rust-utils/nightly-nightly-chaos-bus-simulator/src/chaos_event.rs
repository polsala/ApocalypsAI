use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChaosEvent {
    pub name: String,
    pub description: String,
    pub delay_range: (u32, u32),
    pub emoji: String,
}

impl ChaosEvent {
    pub fn new(name: &str, description: &str, delay_range: (u32, u32), emoji: &str) -> Self {
        Self {
            name: name.to_string(),
            description: description.to_string(),
            delay_range,
            emoji: emoji.to_string(),
        }
    }
    
    pub fn get_random_delay(&self) -> u32 {
        use rand::Rng;
        let mut rng = rand::thread_rng();
        rng.gen_range(self.delay_range.0..=self.delay_range.1)
    }
}

pub fn get_chaos_events() -> Vec<ChaosEvent> {
    vec![
        ChaosEvent::new("Traffic jam", "Heavy traffic slows everything down", (5, 20), "🚗"),
        ChaosEvent::new("Rain storm", "Wet roads cause delays", (3, 15), "🌧️"),
        ChaosEvent::new("Student protest", "Students blocking the route", (10, 30), "🎓"),
        ChaosEvent::new("Mechanical failure", "Bus breaks down", (15, 45), "🔧"),
        ChaosEvent::new("Construction detour", "Road work forces alternate route", (8, 25), "🚧"),
        ChaosEvent::new("Driver strike", "Drivers demanding better pay", (30, 120), "✊"),
        ChaosEvent::new("Fuel shortage", "Can't find gas stations", (20, 60), "⛽"),
        ChaosEvent::new("Foggy conditions", "Low visibility slows traffic", (5, 18), "🌫️"),
        ChaosEvent::new("Accident cleanup", "Police blocking the road", (12, 35), "🚓"),
        ChaosEvent::new("Tourist confusion", "Lost tourists asking for directions", (2, 8), "🗺️"),
    ]
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_chaos_event_creation() {
        let event = ChaosEvent::new("Test", "Description", (5, 10), "🚌");
        assert_eq!(event.name, "Test");
        assert_eq!(event.description, "Description");
        assert_eq!(event.delay_range, (5, 10));
        assert_eq!(event.emoji, "🚌");
    }
    
    #[test]
    fn test_random_delay_generation() {
        let event = ChaosEvent::new("Test", "Description", (5, 10), "🚌");
        for _ in 0..100 {
            let delay = event.get_random_delay();
            assert!(delay >= 5 && delay <= 10, "Delay {} is outside range", delay);
        }
    }
}
