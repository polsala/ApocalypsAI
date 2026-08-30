use std::env;
use std::io::{self, Read};
use radiation_safe::filter_safe_locations;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <max_safe_radiation>", args[0]);
        std::process::exit(1);
    }
    let max: u32 = match args[1].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid max radiation level: {}", args[1]);
            std::process::exit(1);
        }
    };
    let mut input = String::new();
    io::stdin()
        .read_to_string(&mut input)
        .expect("Failed to read stdin");
    let safe = filter_safe_locations(max, &input);
    for loc in safe {
        println!("{}", loc);
    }
}
