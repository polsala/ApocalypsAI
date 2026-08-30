use std::env;
use chrono::{DateTime, Utc};
use emoji_chronometer::{hour_to_emoji, round_minute};
use chrono::Timelike;

fn print_usage_and_exit(program: &str) -> ! {
    eprintln!("Usage: {} <ISO8601 timestamp>", program);
    std::process::exit(1);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        print_usage_and_exit(&args[0]);
    }
    let ts = &args[1];
    let dt: DateTime<Utc> = match DateTime::parse_from_rfc3339(ts) {
        Ok(t) => t.with_timezone(&Utc),
        Err(_) => {
            eprintln!("Invalid timestamp format");
            std::process::exit(1);
        }
    };
    let hour = dt.hour();
    let minute = dt.minute();
    let emoji = hour_to_emoji(hour);
    let rounded = round_minute(minute);
    println!("{} {:02}", emoji, rounded);
}
