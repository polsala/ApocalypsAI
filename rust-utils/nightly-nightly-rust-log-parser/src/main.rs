use clap::Parser;
use serde_json::Value;
use std::io::{self, BufRead};

/// A whimsical yet useful standalone utility for the ApocalypsAI community.
/// This tool is a high-performance Command Line Interface (CLI) application
/// written in Rust, designed to efficiently parse and filter structured log entries.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Filter logs based on a keyword or pattern.
    #[arg(short, long)]
    filter: Option<String>,

    /// Specify the log format (e.g., 'json', 'plain'). Defaults to plain text.
    #[arg(long, default_value = "plain")]
    format: String,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let stdin = io::stdin();
    let reader = stdin.lock();

    for line_result in reader.lines() {
        let line = line_result?;

        let mut should_print = true;

        if let Some(filter_term) = &args.filter {
            should_print = match args.format.as_str() {
                "json" => {
                    // Attempt to parse as JSON and check for a 'message' or 'log' field
                    // or any field that contains the filter term.
                    match serde_json::from_str::<Value>(&line) {
                        Ok(json_val) => {
                            let mut found = false;
                            if let Some(msg) = json_val.get("message").and_then(Value::as_str) {
                                if msg.contains(filter_term) { found = true; }
                            }
                            if let Some(log) = json_val.get("log").and_then(Value::as_str) {
                                if log.contains(filter_term) { found = true; }
                            }
                            // Also check all string values in the JSON
                            for (_key, val) in json_val.as_object().unwrap_or(&serde_json::Map::new()) {
                                if let Some(s) = val.as_str() {
                                    if s.contains(filter_term) { found = true; break; }
                                }
                            }
                            found
                        }
                        Err(_) => {
                            // If it's not valid JSON, fall back to plain text search
                            line.contains(filter_term)
                        }
                    }
                }
                _ => {
                    // Plain text filtering
                    line.contains(filter_term)
                }
            };
        }

        if should_print {
            println!("{}", line);
        }
    }

    Ok(())
}
