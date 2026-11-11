use std::env;
use nightly_apocalypse_quote_cli::get_quote;

fn parse_seed(args: &[String]) -> Option<u64> {
    // Look for "--seed=NUM" pattern
    for arg in args.iter() {
        if let Some(num) = arg.strip_prefix("--seed=") {
            return num.parse::<u64>().ok();
        }
    }
    // Look for "--seed NUM" pattern
    let mut iter = args.iter();
    while let Some(arg) = iter.next() {
        if arg == "--seed" {
            if let Some(val) = iter.next() {
                return val.parse::<u64>().ok();
            }
        }
    }
    None
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    let seed = parse_seed(&args);
    let quote = get_quote(seed);
    println!("{}", quote);
}
