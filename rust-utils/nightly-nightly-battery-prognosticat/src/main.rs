use std::env;

use nightly_battery_prognosticator::estimate_hours;

fn print_usage() {
    eprintln!("Usage: nightly-battery-prognosticator <current_percent> <consumption_per_hour> [radiation_factor]");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 || args.len() > 4 {
        print_usage();
        std::process::exit(1);
    }

    let current: f64 = args[1].parse().unwrap_or_else(|_| {
        eprintln!("Invalid current_percent");
        std::process::exit(1);
    });
    let consumption: f64 = args[2].parse().unwrap_or_else(|_| {
        eprintln!("Invalid consumption_per_hour");
        std::process::exit(1);
    });
    let radiation: f64 = if args.len() == 4 {
        args[3].parse().unwrap_or_else(|_| {
            eprintln!("Invalid radiation_factor");
            std::process::exit(1);
        })
    } else {
        1.0
    };

    let hours = estimate_hours(current, consumption, radiation);
    if hours.is_infinite() {
        println!("Estimated remaining hours: ∞ (no consumption)");
    } else {
        println!("Estimated remaining hours: {:.2}", hours);
    }
}
