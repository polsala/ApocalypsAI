use chrono::{DateTime, Utc, TimeZone};
use std::env;

fn print_usage() {
    eprintln!("Usage:");
    eprintln!("  --to-epoch <ISO8601>    Convert ISO‑8601 timestamp to epoch seconds");
    eprintln!("  --from-epoch <SECONDS>  Convert epoch seconds to ISO‑8601 timestamp");
}

fn to_epoch(input: &str) -> Result<i64, String> {
    // Parse as RFC3339 (ISO‑8601)
    match DateTime::parse_from_rfc3339(input) {
        Ok(dt) => Ok(dt.timestamp()),
        Err(e) => Err(format!("Failed to parse timestamp: {}", e)),
    }
}

fn from_epoch(input: &str) -> Result<String, String> {
    match input.parse::<i64>() {
        Ok(sec) => {
            let dt = Utc.timestamp_opt(sec, 0).single().ok_or_else(|| "Invalid epoch value".to_string())?;
            Ok(dt.to_rfc3339())
        }
        Err(e) => Err(format!("Failed to parse epoch: {}", e)),
    }
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.len() != 2 {
        print_usage();
        std::process::exit(1);
    }
    match args[0].as_str() {
        "--to-epoch" => match to_epoch(&args[1]) {
            Ok(ts) => println!("{}", ts),
            Err(e) => {
                eprintln!("{}", e);
                std::process::exit(1);
            }
        },
        "--from-epoch" => match from_epoch(&args[1]) {
            Ok(s) => println!("{}", s),
            Err(e) => {
                eprintln!("{}", e);
                std::process::exit(1);
            }
        },
        _ => {
            print_usage();
            std::process::exit(1);
        }
    }
}
