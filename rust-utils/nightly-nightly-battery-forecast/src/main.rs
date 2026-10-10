use std::env;
use battery_forecast::{estimate_hours, warning_message};

fn print_usage() {
    eprintln!("Usage: battery-forecast <current_percent> <consumption_rate_mAh_per_hour> <battery_capacity_mAh>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        print_usage();
        std::process::exit(1);
    }
    let percent: f64 = args[1].parse().unwrap_or_else(|_| {
        eprintln!("Invalid percent");
        std::process::exit(1);
    });
    let rate: f64 = args[2].parse().unwrap_or_else(|_| {
        eprintln!("Invalid consumption rate");
        std::process::exit(1);
    });
    let capacity: f64 = args[3].parse().unwrap_or_else(|_| {
        eprintln!("Invalid capacity");
        std::process::exit(1);
    });

    let hours = estimate_hours(capacity, percent, rate);
    if hours.is_infinite() {
        println!("Infinite runtime (no consumption).");
    } else {
        println!("Estimated remaining time: {:.2} hours", hours);
        println!("{}", warning_message(hours));
    }
}
