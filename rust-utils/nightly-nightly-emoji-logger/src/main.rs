use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() > 2 {
        eprintln!("Usage: {} [file]", args[0]);
        std::process::exit(1);
    }
    let reader: Box<dyn BufRead> = if args.len() == 2 {
        let file = File::open(&args[1])?;
        Box::new(BufReader::new(file))
    } else {
        Box::new(BufReader::new(io::stdin()))
    };
    crate::process(reader, io::stdout())
}

