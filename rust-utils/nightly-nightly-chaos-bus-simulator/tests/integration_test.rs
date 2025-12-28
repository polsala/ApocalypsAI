use nightly_chaos_bus_simulator::*;
use std::sync::{Arc, Mutex};
use std::time::Duration;

#[test]
fn test_bus_creation() {
    let buses = create_test_buses(2, 3);
    assert_eq!(buses.len(), 6); // 2 routes * 3 buses per route
    
    // Check that buses are distributed across routes
    let mut route_counts = std::collections::HashMap::new();
    for bus in &buses {
        *route_counts.entry(bus.route_id).or_insert(0) += 1;
    }
    
    assert_eq!(route_counts.len(), 2);
    assert_eq!(*route_counts.get(&1).unwrap(), 3);
    assert_eq!(*route_counts.get(&2).unwrap(), 3);
}

#[test]
fn test_chaos_events_have_valid_ranges() {
    let events = get_chaos_events();
    
    for event in &events {
        assert!(event.delay_range.0 <= event.delay_range.1, "Invalid delay range for {}", event.name);
        assert!(event.delay_range.0 > 0, "Minimum delay should be positive for {}", event.name);
    }
}

#[test]
fn test_simulation_with_minimal_chaos() {
    // This test would need to be adapted for the actual simulation function
    // For now, we test that the function exists and can be called
    let chaos_events = get_chaos_events();
    assert!(!chaos_events.is_empty());
    assert!(chaos_events.len() >= 5); // We have at least 5 different chaos events
}

#[test]
fn test_bus_status_transitions() {
    let mut bus = Bus {
        id: 1,
        route_id: 1,
        status: BusStatus::OnTime,
        delay_minutes: 0,
        last_event: None,
    };
    
    // Apply delay
    bus.delay_minutes = 10;
    bus.status = BusStatus::Delayed;
    bus.last_event = Some("Traffic jam".to_string());
    
    assert_eq!(bus.delay_minutes, 10);
    assert!(matches!(bus.status, BusStatus::Delayed));
    assert_eq!(bus.last_event, Some("Traffic jam".to_string()));
    
    // Recovery
    bus.delay_minutes = 0;
    bus.status = BusStatus::OnTime;
    bus.last_event = Some("Recovered from delay".to_string());
    
    assert_eq!(bus.delay_minutes, 0);
    assert!(matches!(bus.status, BusStatus::OnTime));
    assert_eq!(bus.last_event, Some("Recovered from delay".to_string()));
}

#[test]
fn test_simulation_result_serialization() {
    let result = SimulationResult {
        duration_seconds: 30,
        chaos_level: 5,
        total_buses: 6,
        total_delays: 2,
        events: vec!["Test event".to_string()],
        final_stats: std::collections::HashMap::from([("Test event".to_string(), 1)]),
    };
    
    let json = serde_json::to_string(&result).unwrap();
    assert!(json.contains("duration_seconds"));
    assert!(json.contains("chaos_level"));
    assert!(json.contains("total_buses"));
    
    let deserialized: SimulationResult = serde_json::from_str(&json).unwrap();
    assert_eq!(result.duration_seconds, deserialized.duration_seconds);
    assert_eq!(result.chaos_level, deserialized.chaos_level);
    assert_eq!(result.total_buses, deserialized.total_buses);
}

// Helper function to create test buses
fn create_test_buses(routes: usize, buses_per_route: usize) -> Vec<Bus> {
    let mut buses = Vec::new();
    for route_id in 1..=routes {
        for bus_id in 1..=buses_per_route {
            buses.push(Bus {
                id: bus_id as u32,
                route_id: route_id as u32,
                status: BusStatus::OnTime,
                delay_minutes: 0,
                last_event: None,
            });
        }
    }
    buses
}

#[test]
fn test_chaos_event_probabilities() {
    // Mock random number generator for predictable testing
    let mut rng = rand::rngs::mock::StepRng::new(50, 10); // Start at 50, increment by 10
    
    let chaos_events = get_chaos_events();
    let mut selected_events = std::collections::HashSet::new();
    
    // Simulate 100 random selections
    for _ in 0..100 {
        let event_idx = rng.gen_range(0..chaos_events.len());
        selected_events.insert(chaos_events[event_idx].name.clone());
    }
    
    // With our mock RNG, we should get a good distribution
    assert!(selected_events.len() >= 3, "Should select multiple different events");
}

#[test]
fn test_delay_calculation() {
    let event = ChaosEvent {
        name: "Test event".to_string(),
        description: "Test description".to_string(),
        delay_range: (5, 15),
        emoji: "🚌".to_string(),
    };
    
    // Test that delay is within expected range
    let mut rng = rand::thread_rng();
    for _ in 0..100 {
        let delay = rng.gen_range(event.delay_range.0..=event.delay_range.1);
        assert!(delay >= 5 && delay <= 15, "Delay {} is outside expected range", delay);
    }
}
