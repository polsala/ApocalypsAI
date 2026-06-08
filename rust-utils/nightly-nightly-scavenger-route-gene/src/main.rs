use rand::{seq::SliceRandom, Rng, SeedableRng};
use rand::rngs::StdRng;
use std::env;
use std::time::{SystemTime, UNIX_EPOCH};

fn main() {
    // Optional seed from command‑line arguments
    let args: Vec<String> = env::args().collect();
    let seed: u64 = if args.len() > 1 {
        args[1].parse().unwrap_or_else(|_| current_timestamp())
    } else {
        current_timestamp()
    };
    let mut rng = StdRng::seed_from_u64(seed);

    let locations = vec![
        "Abandoned Mall",
        "Crumbling Library",
        "Rusty Bridge",
        "Forgotten Subway",
        "Radiated Farm",
        "Deserted Power Plant",
        "Overgrown Park",
        "Collapsed Stadium",
        "Silent Hospital",
        "Dusty Warehouse",
    ];

    // Number of stops between 3 and 7 (inclusive)
    let stops = rng.gen_range(3..=7) as usize;
    let mut chosen = locations.clone();
    chosen.shuffle(&mut rng);

    for (i, loc) in chosen.iter().take(stops).enumerate() {
        println!("{}. {}", i + 1, loc);
    }
}

fn current_timestamp() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs()
}
