use std::env;
use nightly_radiation_dose_cli::compute_dose;

fn print_usage() {
    eprintln!("Usage: nightly-radiation-dose-cli <distance_m> <time_min> <source_sieverts_per_hr_at_1m>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        print_usage();
        std::process::exit(1);
    }
    let distance: f64 = match args[1].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid distance: {}", args[1]);
            std::process::exit(1);
        }
    };
    let time: f64 = match args[2].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid time: {}", args[2]);
            std::process::exit(1);
        }
    };
    let source: f64 = match args[3].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid source strength: {}", args[3]);
            std::process::exit(1);
        }
    };
    let dose = compute_dose(distance, time, source);
    println!("Estimated dose: {:.6} Sv", dose);
}
