use clap::Parser;
use rand::seq::SliceRandom;
use rand::Rng;
use chrono::Utc;
use sha2::{Sha256, Digest};
use hex;

#[derive(Parser, Debug)]
#[command(author, version, about = "Detects and 'tunes' minor temporal echoes, providing whimsical suggestions for reality harmonization.", long_about = None)]
struct Args {
    /// An optional string to seed the temporal echo detection. If not provided, current timestamp is used.
    #[arg(short, long)]
    seed: Option<String>,

    /// Output only the raw temporal frequency.
    #[arg(short, long)]
    frequency_only: bool,
}

// Function to generate a deterministic "echo report" based on a seed
fn generate_echo_report(seed_str: &str) -> (String, String) {
    let mut hasher = Sha256::new();
    hasher.update(seed_str.as_bytes());
    let result = hasher.finalize();
    let hash_hex = hex::encode(result);

    // Use a portion of the hash to derive a "frequency" and pick a suggestion
    let frequency_val = u64::from_str_radix(&hash_hex[0..16], 16).unwrap_or(0xDEADBEEF);
    
    // Whimsical frequency calculation, ensuring it's always positive and has a decimal
    // Use modulo 10000 to get a value between 0 and 9999, then divide by 100 for two decimal places.
    // Add a base whimsical 42.0 Hz to ensure it's always above 42.0.
    let frequency = format!("{:.2} Hz", (frequency_val % 10000) as f64 / 100.0 + 42.0);

    let suggestions = vec![
        "Adjust your internal clock by humming a forgotten tune.",
        "Re-align your socks. Misaligned socks are a common temporal irritant.",
        "Offer a sincere compliment to a houseplant.",
        "Contemplate the true nature of toast. Is it bread, or something more?",
        "Gently pat a nearby wall and whisper 'It's okay, you're doing great.'",
        "Perform a small, unexpected act of kindness for a stranger.",
        "Drink a glass of water, but imagine it's liquid starlight.",
        "Hum the 'Imperial March' backwards.",
        "Check if your reflection is truly yours, or just a very good mimic.",
        "Blink three times slowly, then once very fast.",
        "Consider if you've left any paradoxes untended in the pantry.",
        "Ensure all your ducks are in a row, even the imaginary ones.",
        "Tell a joke to a inanimate object. Observe its reaction (or lack thereof).",
        "Write down a secret, then immediately burn the paper (safely!).",
        "Stare at a cloud until it changes shape (or you imagine it does).",
    ];

    // Use a portion of the hash as a pseudo-random index
    let index = (frequency_val % suggestions.len() as u64) as usize;
    let suggestion = suggestions[index].to_string();

    (frequency, suggestion)
}

fn main() {
    let args = Args::parse();

    let seed_str = args.seed.unwrap_or_else(|| Utc::now().timestamp().to_string());

    let (frequency, suggestion) = generate_echo_report(&seed_str);

    if args.frequency_only {
        println!("{}", frequency);
    } else {
        println!("Temporal Echo Detected!");
        println!("  Resonance Frequency: {}", frequency);
        println!("  Harmonizing Suggestion: {}", suggestion);
        println!("\nStay vigilant, fellow temporal traveler!");
    }
}
