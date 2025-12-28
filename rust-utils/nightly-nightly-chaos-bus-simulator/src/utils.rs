use crate::{Bus, ChaosEvent};
use colored::*;

pub fn display_status(buses: &[Bus], chaos_level: u32) {
    println!("\n{}", "Current Bus Status:".bright_blue().bold());
    
    // Group buses by route
    let mut routes: std::collections::HashMap<u32, Vec<&Bus>> = std::collections::HashMap::new();
    for bus in buses {
        routes.entry(bus.route_id).or_insert_with(Vec::new).push(bus);
    }
    
    for route_id in 1..=routes.len() as u32 {
        if let Some(route_buses) = routes.get(&route_id) {
            println!("\n{} Route {}:", "🚌".bright_yellow(), route_id);
            
            for bus in route_buses {
                let status_str = match &bus.status {
                    BusStatus::OnTime => "On time".green(),
                    BusStatus::Delayed => format!("Delayed ({} min)", bus.delay_minutes).red(),
                    BusStatus::BrokenDown => "Broken down".bright_red(),
                    BusStatus::Stranded => "Stranded".bright_red(),
                };
                
                let event_str = bus.last_event
                    .as_ref()
                    .map(|e| format!(" (Last: {})", e))
                    .unwrap_or_default();
                
                println!("  {} Bus {}: {}{}", "🚍".cyan(), bus.id, status_str, event_str);
            }
        }
    }
    
    println!("\n{}", format!("Chaos Level: {}/10 | Active Buses: {}", chaos_level, buses.len()).dimmed());
    println!("{}", "─".repeat(50).dimmed());
}

pub fn print_simulation_header(chaos_level: u32) {
    println!("{}", "🚌 Chaos Bus Simulator Starting...".bright_cyan().bold());
    println!("{}
", format!("Chaos Level: {}/10", chaos_level).yellow().bold());
}

pub fn print_simulation_complete(total_delays: usize, total_events: usize) {
    println!("\n{}", "🏁 Simulation Complete!".bright_magenta().bold());
    println!("{}", format!("Total delays: {}", total_delays).cyan());
    println!("{}", format!("Total events: {}", total_events).cyan());
}

pub fn print_event_breakdown(final_stats: &std::collections::HashMap<String, usize>) {
    if !final_stats.is_empty() {
        println!("\n{}", "Event Breakdown:".yellow().bold());
        for (event, count) in final_stats.iter() {
            println!("  {}: {} occurrences", event, count);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{Bus, BusStatus};
    
    #[test]
    fn test_display_status_does_not_panic() {
        let buses = vec![
            Bus::new(1, 1),
            Bus::new(2, 1),
        ];
        
        // This test just ensures the function doesn't panic
        // We can't easily test the output, but we can verify it runs
        assert!(std::panic::catch_unwind(|| {
            display_status(&buses, 5);
        }).is_ok());
    }
    
    #[test]
    fn test_print_simulation_header() {
        assert!(std::panic::catch_unwind(|| {
            print_simulation_header(5);
        }).is_ok());
    }
    
    #[test]
    fn test_print_simulation_complete() {
        assert!(std::panic::catch_unwind(|| {
            print_simulation_complete(2, 5);
        }).is_ok());
    }
}
