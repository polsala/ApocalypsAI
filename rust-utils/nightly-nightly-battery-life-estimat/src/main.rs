use std::env;

use battery_life_estimator::estimate_hours;

fn print_usage() {
    eprintln!("Usage: battery-life-estimator <capacity_mAh> <draw_mA> [efficiency]");
    eprintln!("  capacity_mAh: current battery capacity in mAh");
    eprintln!("  draw_mA: average current draw in mA");
    eprintln!("  efficiency (optional): efficiency factor (0.0-1.0), default 0.9");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 || args.len() > 4 {
        print_usage();
        std::process::exit(1);
    }
    let capacity: f64 = args[1].parse().unwrap_or_else(|_| {
        eprintln!("Invalid capacity");
        std::process::exit(1);
    });
    let draw: f64 = args[2].parse().unwrap_or_else(|_| {
        eprintln!("Invalid draw");
        std::process::exit(1);
    });
    let efficiency: f64 = if args.len() == 4 {
        args[3].parse().unwrap_or_else(|_| {
            eprintln!("Invalid efficiency");
            std::process::exit(1);
        })
    } else {
        0.9
    };
    let hours = estimate_hours(capacity, draw, efficiency);
    if hours.is_infinite() {
        println!("Estimated remaining time: ∞ hours (no draw)");
    } else {
        println!("Estimated remaining time: {:.2} hours", hours);
    }
}
