use std::env;
use nightly_water_purifier_cli::recommended_steps;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <source> <contamination_ppm>", args[0]);
        std::process::exit(1);
    }
    let source = &args[1];
    let contamination: u32 = match args[2].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Contamination must be a nonânegative integer");
            std::process::exit(1);
        }
    };
    let steps = recommended_steps(source, contamination);
    for (i, step) in steps.iter().enumerate() {
        println!("{}. {}", i + 1, step);
    }
}

