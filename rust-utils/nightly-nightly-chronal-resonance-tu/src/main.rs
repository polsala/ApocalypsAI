use clap::Parser;
use sha2::{Digest, Sha256};

#[derive(Parser, Debug)]
#[command(author, version, about = "Generate a Chronal Resonance Signature for any text.", long_about = None)]
struct Args {
    /// The text input to generate a chronal resonance signature for.
    #[arg(short, long)]
    input: String,
}

fn generate_signature(input: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input.as_bytes());
    let result = hasher.finalize();
    let hash_bytes = result.as_slice();

    // Convert first 8 bytes to u64 for various calculations
    let mut u64_bytes = [0u8; 8];
    u64_bytes.copy_from_slice(&hash_bytes[0..8]);
    let hash_val = u64::from_be_bytes(u64_bytes);

    // Whimsical frequency (0.00 to 99.99 Hz)
    let frequency = (hash_val % 10000) as f64 / 100.0;

    // Stability emoji
    let stability_emojis = ["✨", "🌀", "⏳", "⚡", "🌌", "💫", "🌠", "⚛️"];
    let stability_index = (hash_val / 10000) % stability_emojis.len() as u64;
    let stability_emoji = stability_emojis[stability_index as usize];

    // Temporal glyph (a character from A-Z or a-z)
    let glyph_char_code = ((hash_val / 1000000) % 52) as u8; // 0-51
    let temporal_glyph = if glyph_char_code < 26 {
        char::from_u32('A' as u32 + glyph_char_code as u32).unwrap()
    } else {
        char::from_u32('a' as u32 + (glyph_char_code - 26) as u32).unwrap()
    };

    // A "phase shift" indicator (a short, random-looking hex string)
    let phase_shift = hex::encode(&hash_bytes[8..12]); // Use next 4 bytes for this

    format!("{:.2} Hz {} {} (Phase: {})", frequency, stability_emoji, temporal_glyph, phase_shift)
}

fn main() {
    let args = Args::parse();
    let signature = generate_signature(&args.input);
    println!("Chronal Resonance Signature for \"{}\":", args.input);
    println!("{}", signature);
}
