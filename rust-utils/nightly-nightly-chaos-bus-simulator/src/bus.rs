use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Bus {
    pub id: u32,
    pub route_id: u32,
    pub status: BusStatus,
    pub delay_minutes: u32,
    pub last_event: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum BusStatus {
    OnTime,
    Delayed,
    BrokenDown,
    Stranded,
}

impl Bus {
    pub fn new(id: u32, route_id: u32) -> Self {
        Self {
            id,
            route_id,
            status: BusStatus::OnTime,
            delay_minutes: 0,
            last_event: None,
        }
    }
    
    pub fn apply_delay(&mut self, delay: u32, event_name: String) {
        self.delay_minutes += delay;
        self.status = BusStatus::Delayed;
        self.last_event = Some(event_name);
    }
    
    pub fn recover(&mut self, recovery_amount: u32) {
        if self.delay_minutes >= recovery_amount {
            self.delay_minutes -= recovery_amount;
            if self.delay_minutes == 0 {
                self.status = BusStatus::OnTime;
                self.last_event = Some("Recovered from delay".to_string());
            }
        }
    }
    
    pub fn is_delayed(&self) -> bool {
        self.delay_minutes > 0
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_bus_creation() {
        let bus = Bus::new(1, 1);
        assert_eq!(bus.id, 1);
        assert_eq!(bus.route_id, 1);
        assert!(matches!(bus.status, BusStatus::OnTime));
        assert_eq!(bus.delay_minutes, 0);
        assert!(bus.last_event.is_none());
    }
    
    #[test]
    fn test_bus_delay_application() {
        let mut bus = Bus::new(1, 1);
        bus.apply_delay(15, "Traffic jam".to_string());
        
        assert_eq!(bus.delay_minutes, 15);
        assert!(matches!(bus.status, BusStatus::Delayed));
        assert_eq!(bus.last_event, Some("Traffic jam".to_string()));
    }
    
    #[test]
    fn test_bus_recovery() {
        let mut bus = Bus::new(1, 1);
        bus.apply_delay(10, "Traffic jam".to_string());
        
        bus.recover(5);
        assert_eq!(bus.delay_minutes, 5);
        assert!(matches!(bus.status, BusStatus::Delayed));
        
        bus.recover(5);
        assert_eq!(bus.delay_minutes, 0);
        assert!(matches!(bus.status, BusStatus::OnTime));
        assert_eq!(bus.last_event, Some("Recovered from delay".to_string()));
    }
    
    #[test]
    fn test_bus_is_delayed() {
        let mut bus = Bus::new(1, 1);
        assert!(!bus.is_delayed());
        
        bus.apply_delay(5, "Test".to_string());
        assert!(bus.is_delayed());
        
        bus.recover(5);
        assert!(!bus.is_delayed());
    }
}
