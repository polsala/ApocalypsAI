use clap::Parser;
use regex::Regex;
use std::io::{self, BufRead, BufReader, Read};
use std::fs::File;

#[derive(Parser, Debug)]
#[clap(author, version, about = "A high-performance Rust CLI to filter repetitive 'noise' and patterns from text streams, revealing significant 'echoes'.", long_about = None)]
struct Args {
    /// Path to the input file. If not provided, reads from stdin.
    #[clap(name = "FILE")]
    input_file: Option<String>,

    /// One or more regular expressions to treat as 'noise'. Lines matching any of these patterns will be filtered out.
    #[clap(short = 'p', long = "pattern", value_name = "REGEX")]
    patterns: Vec<String>,

    /// Enable filtering of consecutive duplicate lines.
    #[clap(short = 'd', long = "deduplicate")]
    deduplicate: bool,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let reader: Box<dyn Read> = match &args.input_file {
        Some(file_path) => Box::new(File::open(file_path)?),
        None => Box::new(io::stdin()),
    };

    let mut reader = BufReader::new(reader);
    let mut compiled_patterns: Vec<Regex> = Vec::new();

    for pattern_str in args.patterns {
        match Regex::new(&pattern_str) {
            Ok(re) => compiled_patterns.push(re),
            Err(e) => {
                eprintln!("Error compiling regex '{}': {}", pattern_str, e);
                std::process::exit(1);
            }
        }
    }

    let mut last_line: Option<String> = None;
    let mut line = String::new();

    loop {
        line.clear();
        let bytes_read = reader.read_line(&mut line)?;
        if bytes_read == 0 {
            break; // EOF
        }

        let trimmed_line = line.trim_end_matches('\n').trim_end_matches('\r');

        // Check for noise patterns
        let is_noise = compiled_patterns.iter().any(|re| re.is_match(trimmed_line));
        if is_noise {
            continue;
        }

        // Check for consecutive duplicates
        if args.deduplicate {
            if let Some(prev_line) = &last_line {
                if prev_line == trimmed_line {
                    continue;
                }
            }
        }

        println!("{}", trimmed_line);
        last_line = Some(trimmed_line.to_string());
    }

    Ok(())
}
