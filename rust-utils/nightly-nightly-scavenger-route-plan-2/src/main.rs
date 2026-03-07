use rand::{seq::SliceRandom, Rng, SeedableRng};
use rand::rngs::StdRng;
use std::env;

/// Generates a deterministic scavenger route.
///
/// * `locations` – vector of location names.
/// * `seed` – seed for the random number generator, making the output repeatable.
///
/// Returns a vector of `(location, distance_from_previous)` tuples. The first entry has a distance of `0`.
pub fn generate_route(locations: Vec<String>, seed: u64) -> Vec<(String, u32)> {
    let mut rng = StdRng::seed_from_u64(seed);
    let mut shuffled = locations.clone();
    shuffled.shuffle(&mut rng);
    let mut route = Vec::new();
    for (i, loc) in shuffled.iter().enumerate() {
        let distance = if i == 0 { 0 } else { rng.gen_range(1..=10) };
        route.push((loc.clone(), distance));
    }
    route
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} \"loc1,loc2,loc3,...\"", args[0]);
        std::process::exit(1);
    }
    let input = &args[1];
    let locations: Vec<String> = input.split(',').map(|s| s.trim().to_string()).collect();
    let seed = rand::thread_rng().gen::<u64>();
    let route = generate_route(locations, seed);
    for (i, (loc, dist)) in route.iter().enumerate() {
        if i == 0 {
            println!("Start at: {}", loc);
        } else {
            println!("Travel {} km to {}", dist, loc);
        }
    }
}
