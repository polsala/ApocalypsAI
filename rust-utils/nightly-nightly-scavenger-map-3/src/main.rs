use std::env;
use nightly_scavenger_map::generate_map;

fn print_usage() {
    eprintln!("Usage: nightly-scavenger-map <width> <height> [--seed <u64>]");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        print_usage();
        std::process::exit(1);
    }

    let width: usize = match args[1].parse() {
        Ok(w) => w,
        Err(_) => {
            eprintln!("Invalid width");
            std::process::exit(1);
        }
    };
    let height: usize = match args[2].parse() {
        Ok(h) => h,
        Err(_) => {
            eprintln!("Invalid height");
            std::process::exit(1);
        }
    };

    // Default seed – random each run
    let mut seed: u64 = rand::random();
    let mut i = 3;
    while i < args.len() {
        if args[i] == "--seed" && i + 1 < args.len() {
            seed = match args[i + 1].parse() {
                Ok(s) => s,
                Err(_) => {
                    eprintln!("Invalid seed");
                    std::process::exit(1);
                }
            };
            i += 2;
        } else {
            i += 1;
        }
    }

    let map = generate_map(width, height, seed);
    println!("{}", map);
}
