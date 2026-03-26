use std::env;
use cryptic_emoji_decoder::decode;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: cryptic-emoji-decoder <emoji1> <emoji2> ...");
        std::process::exit(1);
    }
    let input = args.join(" ");
    let result = decode(&input);
    println!("{}", result);
}
