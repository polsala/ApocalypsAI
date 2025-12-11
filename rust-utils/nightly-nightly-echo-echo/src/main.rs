use std::env;
use nightly_echo_echo::{echo_double, echo_original, echo_reverse};

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: nightly-echo-echo <text>");
        std::process::exit(1);
    }
    let input = args.join(" ");
    println!("{}", echo_original(&input));
    println!("{}", echo_reverse(&input));
    println!("{}", echo_double(&input));
}
