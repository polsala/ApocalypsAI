use clap::Parser;
use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;
use rand::RngCore;
use std::env;

/// Simple program to generate random strings
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Length of the random string
    #[arg(short, long, default_value_t = 16)]
    length: usize,

    /// Alphabet to use for characters
    #[arg(short, long, default_value = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")]
    alphabet: String,
}

fn main() {
    let args = Args::parse();

    // Determine RNG: deterministic if ENTROPY_SEED is set
    let mut rng: Box<dyn RngCore> = if let Ok(seed_str) = env::var("ENTROPY_SEED") {
        if let Ok(seed) = seed_str.parse::<u64>() {
            Box::new(StdRng::seed_from_u64(seed))
        } else {
            eprintln!("Invalid ENTROPY_SEED, falling back to random");
            Box::new(rand::thread_rng())
        }
    } else {
        Box::new(rand::thread_rng())
    };

    let result = generate_random_string(&args.alphabet, args.length, &mut *rng);
    println!("{}", result);
}

fn generate_random_string(alphabet: &str, length: usize, rng: &mut dyn RngCore) -> String {
    let chars: Vec<char> = alphabet.chars().collect();
    if chars.is_empty() {
        return String::new();
    }
    (0..length)
        .map(|_| {
            let idx = (rng.next_u32() as usize) % chars.len();
            chars[idx]
        })
        .collect()
}
