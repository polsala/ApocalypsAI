use clap::{Arg, Command};
use rand::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::{self, Write};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};
use colored::*;

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Bus {
    id: u32,
    route_id: u32,
    status: BusStatus,
    delay_minutes: u32,
    last_event: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
enum BusStatus {
    OnTime,
    Delayed,
    BrokenDown,
    Stranded,
}

#[derive(Debug, Serialize, Deserialize)]
struct SimulationResult {
    duration_seconds: u64,
    chaos_level: u32,
    total_buses: usize,
    total_delays: usize,
    events: Vec<String>,
    final_stats: HashMap<String, usize>,
}

#[derive(Debug, Clone)]
struct ChaosEvent {
    name: String,
    description: String,
    delay_range: (u32, u32),
    emoji: String,
}

fn main() -> io::Result<()> {
    let matches = Command::new("Nightly Chaos Bus Simulator")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("A whimsical CLI tool that simulates a chaotic bus system")
        .arg(
            Arg::new("chaos-level")
                .short('c')
                .long("chaos-level")
                .value_name("LEVEL")
                .help("Chaos intensity (1-10)")
                .default_value("5")
        )
        .arg(
            Arg::new("duration")
                .short('d')
                .long("duration")
                .value_name("SECONDS")
                .help("Simulation duration in seconds")
                .default_value("30")
        )
        .arg(
            Arg::new("routes")
                .short('r')
                .long("routes")
                .value_name("COUNT")
                .help("Number of bus routes")
                .default_value("3")
        )
        .arg(
            Arg::new("buses-per-route")
                .short('b')
                .long("buses-per-route")
                .value_name("COUNT")
                .help("Number of buses per route")
                .default_value("2")
        )
        .arg(
            Arg::new("export")
                .short('e')
                .long("export")
                .value_name("FILE")
                .help("Export results to JSON file")
        )
        .get_matches();

    let chaos_level: u32 = matches
        .get_one::<String>("chaos-level")
        .unwrap()
        .parse()
        .expect("Chaos level must be a number between 1 and 10");

    let duration: u64 = matches
        .get_one::<String>("duration")
        .unwrap()
        .parse()
        .expect("Duration must be a valid number");

    let routes_count: usize = matches
        .get_one::<String>("routes")
        .unwrap()
        .parse()
        .expect("Routes must be a valid number");

    let buses_per_route: usize = matches
        .get_one::<String>("buses-per-route")
        .unwrap()
        .parse()
        .expect("Buses per route must be a valid number");

    let export_path = matches.get_one::<String>("export");

    if chaos_level < 1 || chaos_level > 10 {
        eprintln!("{}", "Chaos level must be between 1 and 10!".red());
        std::process::exit(1);
    }

    println!("{}", "🚌 Chaos Bus Simulator Starting...".bright_cyan().bold());
    println!("{}
", format!("Chaos Level: {}/10", chaos_level).yellow().bold());

    let result = run_simulation(chaos_level, duration, routes_count, buses_per_route)?;

    if let Some(path) = export_path {
        let json = serde_json::to_string_pretty(&result)?;
        let mut file = File::create(path)?;
        file.write_all(json.as_bytes())?;
        println!("\n{} {}", "Results exported to:".green(), path.bold());
    }

    Ok(())
}

fn run_simulation(
    chaos_level: u32,
    duration: u64,
    routes_count: usize,
    buses_per_route: usize,
) -> io::Result<SimulationResult> {
    let mut rng = thread_rng();
    let start_time = Instant::now();
    let end_time = start_time + Duration::from_secs(duration);

    // Initialize buses
    let mut buses = Vec::new();
    for route_id in 1..=routes_count {
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

    let events = Arc::new(Mutex::new(Vec::new()));
    let stats = Arc::new(Mutex::new(HashMap::new()));

    // Chaos events with increasing probability based on chaos level
    let chaos_events = get_chaos_events();

    println!("{}
", format!("Starting simulation with {} buses across {} routes...", buses.len(), routes_count).cyan());

    while Instant::now() < end_time {
        // Random chaos event
        if rng.gen_range(0..100) < chaos_level * 10 {
            let event_idx = rng.gen_range(0..chaos_events.len());
            let event = &chaos_events[event_idx];
            
            // Select random bus
            if !buses.is_empty() {
                let bus_idx = rng.gen_range(0..buses.len());
                let bus = &mut buses[bus_idx];
                
                let delay = rng.gen_range(event.delay_range.0..=event.delay_range.1);
                bus.delay_minutes += delay;
                bus.status = BusStatus::Delayed;
                bus.last_event = Some(event.name.clone());
                
                let event_msg = format!(
                    "{} Bus {} on Route {}: {} ({} min delay)",
                    event.emoji, bus.id, bus.route_id, event.name, delay
                );
                
                events.lock().unwrap().push(event_msg.clone());
                
                // Update stats
                let mut stats_guard = stats.lock().unwrap();
                *stats_guard.entry(event.name.clone()).or_insert(0) += 1;
                
                println!("{}", event_msg.yellow());
            }
        }

        // Random recovery
        if rng.gen_range(0..100) < 20 {
            if !buses.is_empty() {
                let bus_idx = rng.gen_range(0..buses.len());
                let bus = &mut buses[bus_idx];
                
                if bus.delay_minutes > 0 {
                    let recovery = rng.gen_range(1..=std::cmp::min(5, bus.delay_minutes));
                    bus.delay_minutes -= recovery;
                    
                    if bus.delay_minutes == 0 {
                        bus.status = BusStatus::OnTime;
                        bus.last_event = Some("Recovered from delay".to_string());
                        println!("{}", format!("✅ Bus {} on Route {}: Recovered from delay!", bus.id, bus.route_id).green());
                    }
                }
            }
        }

        // Display current status
        display_status(&buses, chaos_level);
        
        thread::sleep(Duration::from_secs(2));
    }

    // Final statistics
    let total_delays = buses.iter().filter(|bus| bus.delay_minutes > 0).count();
    let final_stats = stats.lock().unwrap().clone();
    
    println!("\n{}", "🏁 Simulation Complete!".bright_magenta().bold());
    println!("{}", format!("Total delays: {}", total_delays).cyan());
    println!("{}", format!("Total events: {}", events.lock().unwrap().len()).cyan());
    
    if !final_stats.is_empty() {
        println!("\n{}", "Event Breakdown:".yellow().bold());
        for (event, count) in final_stats.iter() {
            println!("  {}: {} occurrences", event, count);
        }
    }

    Ok(SimulationResult {
        duration_seconds: duration,
        chaos_level,
        total_buses: buses.len(),
        total_delays,
        events: events.lock().unwrap().clone(),
        final_stats,
    })
}

fn display_status(buses: &[Bus], chaos_level: u32) {
    println!("\n{}", "Current Bus Status:".bright_blue().bold());
    
    // Group buses by route
    let mut routes: HashMap<u32, Vec<&Bus>> = HashMap::new();
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

fn get_chaos_events() -> Vec<ChaosEvent> {
    vec![
        ChaosEvent {
            name: "Traffic jam".to_string(),
            description: "Heavy traffic slows everything down".to_string(),
            delay_range: (5, 20),
            emoji: "🚗".to_string(),
        },
        ChaosEvent {
            name: "Rain storm".to_string(),
            description: "Wet roads cause delays".to_string(),
            delay_range: (3, 15),
            emoji: "🌧️".to_string(),
        },
        ChaosEvent {
            name: "Student protest".to_string(),
            description: "Students blocking the route".to_string(),
            delay_range: (10, 30),
            emoji: "🎓".to_string(),
        },
        ChaosEvent {
            name: "Mechanical failure".to_string(),
            description: "Bus breaks down".to_string(),
            delay_range: (15, 45),
            emoji: "🔧".to_string(),
        },
        ChaosEvent {
            name: "Construction detour".to_string(),
            description: "Road work forces alternate route".to_string(),
            delay_range: (8, 25),
            emoji: "🚧".to_string(),
        },
        ChaosEvent {
            name: "Driver strike".to_string(),
            description: "Drivers demanding better pay".to_string(),
            delay_range: (30, 120),
            emoji: "✊".to_string(),
        },
        ChaosEvent {
            name: "Fuel shortage".to_string(),
            description: "Can't find gas stations".to_string(),
            delay_range: (20, 60),
            emoji: "⛽".to_string(),
        },
        ChaosEvent {
            name: "Foggy conditions".to_string(),
            description: "Low visibility slows traffic".to_string(),
            delay_range: (5, 18),
            emoji: "🌫️".to_string(),
        },
        ChaosEvent {
            name: "Accident cleanup".to_string(),
            description: "Police blocking the road".to_string(),
            delay_range: (12, 35),
            emoji: "🚓".to_string(),
        },
        ChaosEvent {
            name: "Tourist confusion".to_string(),
            description: "Lost tourists asking for directions".to_string(),
            delay_range: (2, 8),
            emoji: "🗺️".to_string(),
        },
    ]
}
