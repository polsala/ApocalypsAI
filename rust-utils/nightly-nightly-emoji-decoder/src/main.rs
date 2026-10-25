use emoji_decoder::decode_emoji;
use std::env;
use std::io::Read;

fn main() {
    let args: Vec<String> = env::args().collect();
    let input = if args.len() > 1 {
        args[1..].join(" ")
    } else {
        // Read from STDIN if no arguments provided
        let mut buf = String::new();
        std::io::stdin().read_to_string(&mut buf).unwrap_or_default();
        buf.trim().to_string()
    };

    let results = decode_emoji(&input);
    if results.is_empty() {
        eprintln!("No known emojis found.");
        std::process::exit(1);
    }
    for (emoji, desc) in results {
        println!("{} -> {}", emoji, desc);
    }
}
