use std::env;
use std::process;

mod lib;

fn print_usage() {
    eprintln!("Usage: nightly-scavenger-map [options]");
    eprintln!("Options:");
    eprintln!("  -w <width>   Map width (default 10)");
    eprintln!("  -h <height>  Map height (default 5)");
    eprintln!("  -r <list>    Comma‑separated resource symbols (default F,W,M)");
    eprintln!("  -s <seed>    Optional numeric seed for deterministic maps");
    eprintln!("  -h, --help   Show this help message");
}

fn parse_args() -> (usize, usize, Vec<char>, u64) {
    let args: Vec<String> = env::args().collect();
    let mut width = 10usize;
    let mut height = 5usize;
    let mut resources: Vec<char> = vec!['F', 'W', 'M'];
    let mut seed: u64 = rand::random(); // random seed if not provided
    let mut i = 1usize;
    while i < args.len() {
        match args[i].as_str() {
            "-w" => {
                i += 1;
                if i >= args.len() { print_usage(); process::exit(1); }
                width = args[i].parse().unwrap_or_else(|_| { eprintln!("Invalid width"); process::exit(1); });
            }
            "-h" => {
                // could be height flag or help; check next arg
                if i + 1 < args.len() && !args[i + 1].starts_with('-') {
                    i += 1;
                    height = args[i].parse().unwrap_or_else(|_| { eprintln!("Invalid height"); process::exit(1); });
                } else {
                    print_usage();
                    process::exit(0);
                }
            }
            "--help" => {
                print_usage();
                process::exit(0);
            }
            "-r" => {
                i += 1;
                if i >= args.len() { print_usage(); process::exit(1); }
                resources = args[i]
                    .split(',')
                    .filter_map(|s| s.chars().next())
                    .collect();
            }
            "-s" => {
                i += 1;
                if i >= args.len() { print_usage(); process::exit(1); }
                seed = args[i].parse().unwrap_or_else(|_| { eprintln!("Invalid seed"); process::exit(1); });
            }
            _ => {
                eprintln!("Unknown argument: {}", args[i]);
                print_usage();
                process::exit(1);
            }
        }
        i += 1;
    }
    (width, height, resources, seed)
}

fn main() {
    let (width, height, resources, seed) = parse_args();
    let map = lib::generate_map(width, height, &resources, seed);
    for line in map {
        println!("{}", line);
    }
}
