use std::env;

use ansi_gradient::gradient;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <text>", args[0]);
        std::process::exit(1);
    }
    let input = args[1..].join(" ");
    println!("{}", gradient(&input));
}
