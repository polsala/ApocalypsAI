use clap::Parser;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

#[derive(Parser)]
#[clap(author, version, about)]
struct Args {
    /// Pattern to search for in log lines
    #[clap(short, long)]
    pattern: String,

    /// Input file (stdin if not provided)
    #[clap(short, long)]
    input: Option<String>,

    /// Invert logic: alert if pattern is NOT found
    #[clap(long)]
    invert: bool,
}

fn main() {
    let args = Args::parse();
    let reader: Box<dyn BufRead> = match &args.input {
        Some(path) => {
            let file = File::open(path).expect("Failed to open file");
            Box::new(BufReader::new(file))
        }
        None => Box::new(BufReader::new(io::stdin())),
    };

    let mut found = false;
    for line in reader.lines() {
        let line = line.expect("Failed to read line");
        if line.contains(&args.pattern) {
            found = true;
            if args.invert {
                println!("[VOID-WHISTLE] Unexpected pattern found: {}", args.pattern);
            }
        }
    }

    if !args.invert && !found {
        println!("[VOID-WHISTLE] Silent failure detected: pattern '{}' not found", args.pattern);
    } else if args.invert && found {
        println!("[VOID-WHISTLE] Inverted check passed: pattern '{}' was found", args.pattern);
    }
}
