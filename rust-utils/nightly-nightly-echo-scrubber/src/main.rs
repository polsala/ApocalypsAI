use clap::Parser;
use std::collections::{HashSet, VecDeque};
use std::io::{self, BufRead, Write};

#[derive(Parser, Debug)]
#[command(author, version, about = "Silence the Whispers of Repetition", long_about = None)]
struct Args {
    /// Input file to process. Reads from stdin if not provided.
    #[arg(name = "FILE")]
    input_file: Option<String>,

    /// Enable fuzzy matching (case-insensitive, whitespace-trimmed).
    #[arg(short, long)]
    fuzzy: bool,

    /// When fuzzy matching, sets the size of the 'temporal window' (history buffer) for detecting echoes.
    /// A window of 0 means all previously seen unique fuzzy lines are considered (unlimited history).
    #[arg(short, long, default_value_t = 0)]
    window: usize,

    /// Report detected echoes to stderr instead of just suppressing them.
    #[arg(short, long)]
    report_echoes: bool,
}

/// Normalizes a string for fuzzy comparison: converts to lowercase and trims whitespace.
fn normalize_line(line: &str) -> String {
    line.to_lowercase().trim().to_string()
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let reader: Box<dyn BufRead> = match args.input_file {
        Some(file_path) => {
            let file = std::fs::File::open(file_path)?;
            Box::new(io::BufReader::new(file))
        }
        None => Box::new(io::BufReader::new(io::stdin())),
    };

    let mut seen_exact_lines: HashSet<String> = HashSet::new();
    let mut seen_fuzzy_lines_unlimited: HashSet<String> = HashSet::new(); // Used when window == 0
    let mut fuzzy_history_window: VecDeque<String> = VecDeque::new(); // Used when window > 0

    for line_result in reader.lines() {
        let line = line_result?;

        let mut is_echo = false;

        if args.fuzzy {
            let normalized_line = normalize_line(&line);
            if args.window > 0 {
                // Check against the limited history window
                if fuzzy_history_window.contains(&normalized_line) {
                    is_echo = true;
                }
            } else {
                // Check against all previously seen fuzzy lines (unlimited history)
                if seen_fuzzy_lines_unlimited.contains(&normalized_line) {
                    is_echo = true;
                }
            }

            if !is_echo {
                // This is a unique fuzzy line, print it.
                println!("{}", line);
                
                // Update the appropriate history structure
                if args.window > 0 {
                    fuzzy_history_window.push_back(normalized_line);
                    if fuzzy_history_window.len() > args.window {
                        fuzzy_history_window.pop_front();
                    }
                } else {
                    seen_fuzzy_lines_unlimited.insert(normalized_line);
                }
            } else if args.report_echoes {
                eprintln!("Echo detected: '{}'", line);
            }
        } else { // Exact matching
            if !seen_exact_lines.contains(&line) {
                println!("{}", line);
                seen_exact_lines.insert(line);
            } else if args.report_echoes {
                eprintln!("Echo detected: '{}'", line);
            }
        }
    }

    Ok(())
}
