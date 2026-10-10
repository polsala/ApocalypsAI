use std::env;
use nightly_battery_life_estimator::estimate_hours;

fn print_usage() {
    eprintln!("Usage: nightly-battery-life-estimator <capacity_mAh> <consumption_mA>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }
    let capacity: f64 = match args[1].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid capacity value");
            std::process::exit(1);
        }
    };
    let consumption: f64 = match args[2].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid consumption value");
            std::process::exit(1);
        }
    };
    let hours = estimate_hours(capacity, consumption);
    if hours.is_infinite() {
        println!("Estimated remaining time: ∞ hours (no consumption)");
    } else {
        println!("Estimated remaining time: {:.2} hours", hours);
    }
}
