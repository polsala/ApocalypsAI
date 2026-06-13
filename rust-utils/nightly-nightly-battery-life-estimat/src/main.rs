use std::env;
use battery_life::estimate_hours;

fn print_usage() {
    eprintln!("Usage: battery-life <capacity_mAh> <consumption_mA>");
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
        println!("Estimated runtime: infinite (zero consumption)");
    } else {
        println!("Estimated runtime: {:.2} hours", hours);
    }
}
