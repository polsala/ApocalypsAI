use std::env;
use std::process;

fn print_usage() {
    eprintln!("Usage: nightly-strong-passphrase-generator [--words N] [--include-numbers] [--include-symbols]");
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    let mut words = 4usize;
    let mut include_numbers = false;
    let mut include_symbols = false;

    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "--words" => {
                if i + 1 >= args.len() {
                    eprintln!("Error: --words requires a number");
                    print_usage();
                    process::exit(1);
                }
                words = args[i + 1].parse::<usize>().unwrap_or_else(|_| {
                    eprintln!("Error: invalid number for --words");
                    print_usage();
                    process::exit(1);
                });
                i += 2;
            }
            "--include-numbers" => {
                include_numbers = true;
                i += 1;
            }
            "--include-symbols" => {
                include_symbols = true;
                i += 1;
            }
            _ => {
                eprintln!("Unknown option: {}", args[i]);
                print_usage();
                process::exit(1);
            }
        }
    }

    let opts = crate::PassphraseOptions {
        words,
        include_numbers,
        include_symbols,
    };

    let pass = crate::generate_passphrase(&opts);
    println!("{}", pass);
}
