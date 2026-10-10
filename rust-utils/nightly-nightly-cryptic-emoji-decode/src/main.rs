use clap::Parser;
use std::collections::HashMap;

/// Simple emoji to word decoder
#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Emoji sequence (e.g., "🚀 🌕")
    input: String,
}

fn build_dict() -> HashMap<&'static str, &'static str> {
    let mut m = HashMap::new();
    m.insert("🚀", "launch");
    m.insert("🌕", "moon");
    m.insert("🔥", "fire");
    m.insert("💧", "water");
    m.insert("⚡", "electric");
    m.insert("🧊", "ice");
    m.insert("🌟", "star");
    m.insert("🪐", "planet");
    m.insert("👽", "alien");
    m.insert("🤖", "robot");
    m
}

fn decode(input: &str, dict: &HashMap<&str, &str>) -> String {
    let tokens: Vec<&str> = input.split_whitespace().collect();
    let mut words = Vec::new();
    for token in tokens {
        if let Some(&w) = dict.get(token) {
            words.push(w);
        } else {
            words.push("[unknown]");
        }
    }
    words.join(" ")
}

fn main() {
    let args = Args::parse();
    let dict = build_dict();
    let result = decode(&args.input, &dict);
    println!("{}", result);
}
