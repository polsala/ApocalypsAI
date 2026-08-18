use std::env;
use nightly_radiation_forecast_cli::compute_radiation;

fn print_usage() {
    eprintln!("Usage: <program> <latitude> <longitude>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }
    let lat: f64 = match args[1].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid latitude");
            std::process::exit(1);
        }
    };
    let lon: f64 = match args[2].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid longitude");
            std::process::exit(1);
        }
    };
    let level = compute_radiation(lat, lon);
    println!("Radiation level at ({}, {}): {} mSv", lat, lon, level);
}
