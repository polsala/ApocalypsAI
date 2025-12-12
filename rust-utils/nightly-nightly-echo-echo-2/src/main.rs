use std::env;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: nightly-echo-echo <string>");
        std::process::exit(1);
    }
    let input = &args[0];
    let reversed: String = input.chars().rev().collect();
    let phrase = deterministic_phrase(input);
    println!("Original: {}", input);
    println!("Reversed: {}", reversed);
    println!("Whimsy: {}", phrase);
}

fn deterministic_phrase(input: &str) -> &'static str {
    const PHRASES: &[&str] = &[
        "The moon is made of cheese.",
        "Beware of the dancing squirrels.",
        "Your future is bright!",
        "A banana is a fruit.",
        "The sky is green.",
    ];
    let sum: usize = input.bytes().fold(0, |acc, b| acc + b as usize);
    let idx = sum % PHRASES.len();
    PHRASES[idx]
}
