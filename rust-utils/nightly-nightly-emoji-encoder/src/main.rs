use std::env;
use nightly_emoji_encoder::encode;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: emoji-encoder <text>");
        std::process::exit(1);
    }
    let input = args.join(" ");
    let output = encode(&input);
    println!("{}", output);
}
