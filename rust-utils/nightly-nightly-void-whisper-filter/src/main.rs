use clap::Parser;
use regex::Regex;
use std::fs::File;
use std::io::{self, BufReader, BufRead};
use std::path::PathBuf;
use std::collections::VecDeque;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Filter text streams for 'void whispers' (patterns) and report frequency and context.", long_about = None)]
struct Args {
    /// The regex pattern to search for (the 'void whisper').
    #[clap(short, long)]
    pattern: String,

    /// Path to the input file. If not provided, reads from stdin.
    #[clap(short, long)]
    file: Option<PathBuf>,

    /// Number of context lines to show *before* each match.
    #[clap(short, long, default_value_t = 0)]
    context: usize,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let reader: Box<dyn BufRead> = match &args.file {
        Some(path) => {
            let file = File::open(path)?;
            Box::new(BufReader::new(file))
        }
        None => Box::new(BufReader::new(io::stdin())),
    };

    let re = Regex::new(&args.pattern)
        .map_err(|e| io::Error::new(io::ErrorKind::InvalidInput, format!("Invalid regex pattern: {}", e)))?;

    let mut line_buffer: VecDeque<(usize, String)> = VecDeque::new(); // Store (line_num, line_content)
    let mut matches_found = 0;

    for (current_line_idx, line_result) in reader.lines().enumerate() {
        let line_num = current_line_idx + 1; // 1-based line number
        let line = line_result?;

        // Maintain buffer for 'before' context
        line_buffer.push_back((line_num, line.clone()));
        if line_buffer.len() > args.context + 1 { // +1 because buffer includes current line
            line_buffer.pop_front();
        }

        if re.is_match(&line) {
            matches_found += 1;

            // Print 'before' context from the buffer
            // Iterate up to, but not including, the current line (which is the last in buffer)
            for i in 0..line_buffer.len() - 1 {
                let (buf_line_num, buf_line_content) = &line_buffer[i];
                println!("{}: {}", buf_line_num, buf_line_content);
            }

            // Print the matching line (highlighted)
            println!("{}: \x1b[33m{}\x1b[0m", line_num, line); // Yellow for match
            println!("---"); // Separator for clarity between matches

            // Clear buffer after a match to prevent context overlap for distant matches
            // and ensure context is always fresh for the next match.
            line_buffer.clear();
        }
    }

    eprintln!("Found {} void whispers.", matches_found);

    Ok(())
}
