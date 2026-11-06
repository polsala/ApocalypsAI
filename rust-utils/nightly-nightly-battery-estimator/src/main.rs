use std::env;
use nightly_battery_estimator::{compute_estimated_hours, whimsical_message};

fn print_usage() {
    eprintln!("Usage: battery-estimator <current_percent> <consumption_per_hour>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
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
    let hours = compute_estimated_hours(current, consumption);
    println!("Estimated hours left: {:.2}", hours);
    println!("{}", whimsical_message(hours));
}
