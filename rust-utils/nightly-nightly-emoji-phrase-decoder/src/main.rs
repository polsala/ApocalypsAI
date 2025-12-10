use std::env;
use emoji_phrase_decoder::decode;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: emoji-phrase-decoder <emoji1> <emoji2> ...");
        std::process::exit(1);
    }
    let input = args.join(" ");
    let phrases = decode(&input);
    for phrase in phrases {
        println!("{}", phrase);
    }
}
