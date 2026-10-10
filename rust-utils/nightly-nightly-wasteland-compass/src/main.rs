use clap::Parser;
use std::time::{SystemTime, UNIX_EPOCH};

mod lib;
use lib::{drift_bearing, Lcg};

/// Simple CLI to simulate a radiation‑drifted compass bearing.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Current bearing in degrees (0‑359). Default is 0.
    #[arg(short, long, default_value_t = 0u16)]
    bearing: u16,

    /// Maximum drift in degrees (0‑180). Default is 30.
    #[arg(short = 'd', long, default_value_t = 30u16)]
    max_drift: u16,
}

fn main() {
    let args = Args::parse();
    // Simple validation
    if args.bearing >= 360 {
        eprintln!("Error: bearing must be between 0 and 359.");
        std::process::exit(1);
    }
    if args.max_drift > 180 {
        eprintln!("Error: max_drift must be between 0 and 180.");
        std::process::exit(1);
    }

    // Use current UNIX time as a seed for non‑deterministic runs.
    let seed = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();

    // For demonstration we also show the deterministic path with a fixed seed.
    let deterministic_seed = 42u64;
    let new_bearing = drift_bearing(args.bearing, args.max_drift, deterministic_seed);

    // Compute a non‑deterministic bearing for real usage.
    let mut rng = Lcg::new(seed);
    let drift = (rng.next() % (args.max_drift as u64 + 1)) as i16;
    let direction = if rng.next() % 2 == 0 { 1 } else { -1 };
    let real_bearing = (args.bearing as i16 + direction * drift).rem_euclid(360) as u16;

    println!("Current bearing: {}°", args.bearing);
    println!("Deterministic drift (seed=42): {}°", if direction == 1 { drift } else { -drift });
    println!("New deterministic bearing: {}°", new_bearing);
    println!("Random drift applied: {}°", if direction == 1 { drift } else { -drift });
    println!("New random bearing: {}°", real_bearing);
}
