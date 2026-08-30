use std::env;
use battery_life_estimator::compute_estimated_hours;

fn print_usage() {
    eprintln!("Usage: battery-life-estimator <capacity_mAh> <draw_mA> [efficiency]");
    eprintln!("  capacity_mAh: current battery capacity in mAh");
    eprintln!("  draw_mA: average power draw in mA");
    eprintln!("  efficiency (optional): efficiency factor (0.0-1.0), default 0.9");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 || args.len() > 4 {
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
    let draw: f64 = match args[2].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid draw value");
            std::process::exit(1);
        }
    };
    let efficiency: f64 = if args.len() == 4 {
        match args[3].parse() {
            Ok(v) => v,
            Err(_) => {
                eprintln!("Invalid efficiency value");
                std::process::exit(1);
            }
        }
    } else {
        0.9
    };
    let hours = compute_estimated_hours(capacity, draw, efficiency);
    if hours.is_infinite() {
        println!("Estimated battery life: infinite (draw is zero)");
    } else {
        println!("Estimated battery life: {:.2} hours", hours);
    }
}
