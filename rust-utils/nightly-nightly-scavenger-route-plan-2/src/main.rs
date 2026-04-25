use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <path-to-locations.json>", args[0]);
        process::exit(1);
    }
    let path = &args[1];
    let data = match fs::read_to_string(path) {
        Ok(d) => d,
        Err(e) => {
            eprintln!("Failed to read {}: {}", path, e);
            process::exit(1);
        }
    };
    match scavenger_route_planner::plan_route(&data) {
        Ok(route) => {
            println!("{}", route.join(", "));
        }
        Err(e) => {
            eprintln!("Error processing JSON: {}", e);
            process::exit(1);
        }
    }
}
