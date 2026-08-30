use std::env;

fn main() {
    // Collect command‑line arguments, skipping the binary name.
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: nightly-scavenger-route-planner <location1> <location2> ...");
        std::process::exit(1);
    }

    // Convert Vec<String> to Vec<&str> for the library function.
    let locations: Vec<&str> = args.iter().map(|s| s.as_str()).collect();
    // Fixed seed for the CLI; developers can use the library directly for custom seeds.
    let route = nightly_scavenger_route_planner::generate_route(&locations, 42);

    for (i, loc) in route.iter().enumerate() {
        println!("{}. {}", i + 1, loc);
    }
}
