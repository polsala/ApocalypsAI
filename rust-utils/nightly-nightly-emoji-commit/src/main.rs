use std::env;
use std::fs;
use std::io::{self, Read};

fn main() {
    let args: Vec<String> = env::args().collect();
    let input = if args.len() > 1 {
        fs::read_to_string(&args[1]).unwrap_or_else(|_| {
            eprintln!("Failed to read file {}", &args[1]);
            std::process::exit(1);
        })
    } else {
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer).unwrap();
        buffer
    };

    let output = crate::add_emoji_to_commit(&input);
    println!("{}", output);
}
