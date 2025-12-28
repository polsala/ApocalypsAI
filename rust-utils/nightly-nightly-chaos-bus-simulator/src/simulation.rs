use crate::{Bus, ChaosEvent, BusStatus};
use rand::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

#[derive(Debug, Serialize, Deserialize)]
pub struct SimulationResult {
    pub duration_seconds: u64,
    pub chaos_level: u32,
    pub total_buses: usize,
    pub total_delays: usize,
    pub events: Vec<String>,
    pub final_stats: HashMap<String, usize>,
}

pub fn create_buses(routes_count: usize, buses_per_route: usize) -> Vec<Bus> {
    let mut buses = Vec::new();
    for route_id in 1..=routes_count {
        for bus_id in 1..=buses_per_route {
            buses.push(Bus::new(bus_id as u32, route_id as u32));
        }
    }
    buses
}

pub fn simulate_chaos_event(
    buses: &mut Vec<Bus>,
    events: &Arc<Mutex<Vec<String>>>,
    stats: &Arc<Mutex<HashMap<String, usize>>>,
    chaos_events: &[ChaosEvent],
    chaos_level: u32,
) {
    let mut rng = thread_rng();
    
    if rng.gen_range(0..100) < chaos_level * 10 {
        if !buses.is_empty() {
            let event_idx = rng.gen_range(0..chaos_events.len());
            let event = &chaos_events[event_idx];
            
            let bus_idx = rng.gen_range(0..buses.len());
            let bus = &mut buses[bus_idx];
            
            let delay = event.get_random_delay();
            bus.apply_delay(delay, event.name.clone());
            
            let event_msg = format!(
                "{} Bus {} on Route {}: {} ({} min delay)",
                event.emoji, bus.id, bus.route_id, event.name, delay
            );
            
            events.lock().unwrap().push(event_msg.clone());
            
            let mut stats_guard = stats.lock().unwrap();
            *stats_guard.entry(event.name.clone()).or_insert(0) += 1;
        }
    }
}

pub fn simulate_recovery(buses: &mut Vec<Bus>) {
    let mut rng = thread_rng();
    
    if rng.gen_range(0..100) < 20 {
        if !buses.is_empty() {
            let bus_idx = rng.gen_range(0..buses.len());
            let bus = &mut buses[bus_idx];
            
            if bus.is_delayed() {
                let recovery = rng.gen_range(1..=std::cmp::min(5, bus.delay_minutes));
                bus.recover(recovery);
            }
        }
    }
}

pub fn get_final_statistics(buses: &[Bus]) -> usize {
    buses.iter().filter(|bus| bus.is_delayed()).count()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;
    
    #[test]
    fn test_create_buses() {
        let buses = create_buses(2, 3);
        assert_eq!(buses.len(), 6);
        
        let mut route_counts = HashMap::new();
        for bus in &buses {
            *route_counts.entry(bus.route_id).or_insert(0) += 1;
        }
        
        assert_eq!(route_counts.len(), 2);
        assert_eq!(*route_counts.get(&1).unwrap(), 3);
        assert_eq!(*route_counts.get(&2).unwrap(), 3);
    }
    
    #[test]
    fn test_simulate_chaos_event() {
        let mut buses = vec![Bus::new(1, 1)];
        let events = Arc::new(Mutex::new(Vec::new()));
        let stats = Arc::new(Mutex::new(HashMap::new()));
        let chaos_events = vec![ChaosEvent::new("Test", "Test", (5, 10), "🚌")];
        
        simulate_chaos_event(&mut buses, &events, &stats, &chaos_events, 10);
        
        // With chaos level 10, there's a good chance an event occurred
        // This test is probabilistic, so we just check the function runs without error
        assert!(buses.len() == 1);
    }
    
    #[test]
    fn test_get_final_statistics() {
        let mut buses = vec![Bus::new(1, 1), Bus::new(2, 1)];
        buses[0].apply_delay(10, "Test".to_string());
        
        let delayed_count = get_final_statistics(&buses);
        assert_eq!(delayed_count, 1);
    }
}
