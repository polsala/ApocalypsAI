use std::env;

#[cfg(feature = "shuffle")]
use rand::seq::SliceRandom;

/// Generates a route from the given locations.
///
/// * If `shuffle` is true and the `shuffle` feature is enabled, the order is randomized.
/// * Otherwise the locations are returned in reverse order (deterministic).
fn generate_route(mut locations: Vec<String>, shuffle: bool) -> Vec<String> {
    if shuffle {
        #[cfg(feature = "shuffle")]
        {
            let mut rng = rand::thread_rng();
            locations.shuffle(&mut rng);
            return locations;
        }
        // If the feature is not compiled, fall back to deterministic reverse.
    }
    locations.reverse();
    locations
}

fn print_usage() {
    eprintln!("Usage: scavenger-route-planner [--shuffle] \"loc1,loc2,loc3\"");
    eprintln!("  --shuffle   Randomize the order (requires the 'shuffle' feature compiled)");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage();
        std::process::exit(1);
    }

    let mut shuffle = false;
    let mut loc_arg_index = 1;
    if args[1] == "--shuffle" {
        shuffle = true;
        loc_arg_index = 2;
        if args.len() <= loc_arg_index {
            print_usage();
            std::process::exit(1);
        }
    }

    let loc_str = &args[loc_arg_index];
    let locations: Vec<String> = loc_str
        .split(',')
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty())
        .collect();

    if locations.is_empty() {
        eprintln!("No locations provided.");
        std::process::exit(1);
    }

    let route = generate_route(locations, shuffle);
    for loc in route {
        println!("{}", loc);
    }
}
