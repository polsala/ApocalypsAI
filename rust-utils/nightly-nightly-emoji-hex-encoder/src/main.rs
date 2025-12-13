use std::env;
use nightly_emoji_hex_encoder::{encode, decode};

fn print_usage() {
    eprintln!("Usage: nightly-emoji-hex-encoder <encode|decode> <text>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }
    let command = &args[1];
    let payload = &args[2];
    match command.as_str() {
        "encode" => {
            let out = encode(payload);
            println!("{}", out);
        }
        "decode" => match decode(payload) {
            Ok(s) => println!("{}", s),
            Err(e) => {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        },
        _ => {
            print_usage();
            std::process::exit(1);
        }
    }
}
