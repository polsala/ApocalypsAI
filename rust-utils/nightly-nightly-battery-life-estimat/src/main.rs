use std::env;
use std::process;
use battery_life_estimator::estimate_hours;

fn print_usage() {
    eprintln!("Usage: battery-life-estimator <current_mAh> <consumption_mA>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        process::exit(1);
    }
    let current: f64 = match args[1].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Error: current_mAh must be a number");
            process::exit(1);
        }
    };
    let consumption: f64 = match args[2].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Error: consumption_mA must be a number");
            process::exit(1);
        }
    };
    let hours = estimate_hours(current, consumption);
    if hours.is_infinite() {
        println!("Estimated remaining time: infinite hours");
    } else {
        println!("Estimated remaining time: {:.2} hours", hours);
    }
}
