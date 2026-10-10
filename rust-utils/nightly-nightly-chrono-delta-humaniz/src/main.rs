use std::env;
use chrono::{DateTime, Utc, Duration};

fn parse_iso(s: &str) -> DateTime<Utc> {
    DateTime::parse_from_rfc3339(s)
        .expect("Invalid timestamp")
        .with_timezone(&Utc)
}

fn human_readable_duration(start: DateTime<Utc>, end: DateTime<Utc>) -> String {
    let mut delta = end - start;
    if delta < Duration::zero() {
        delta = -delta;
    }
    let days = delta.num_days();
    let hours = delta.num_hours() % 24;
    let minutes = delta.num_minutes() % 60;
    let seconds = delta.num_seconds() % 60;
    let mut parts = Vec::new();
    if days != 0 {
        parts.push(format!("{} day{}", days, if days != 1 { "s" } else { "" }));
    }
    if hours != 0 {
        parts.push(format!("{} hour{}", hours, if hours != 1 { "s" } else { "" }));
    }
    if minutes != 0 {
        parts.push(format!("{} minute{}", minutes, if minutes != 1 { "s" } else { "" }));
    }
    if seconds != 0 || parts.is_empty() {
        parts.push(format!("{} second{}", seconds, if seconds != 1 { "s" } else { "" }));
    }
    parts.join(", ")
}

pub fn compute_delta(start: &str, end: &str) -> String {
    let s = parse_iso(start);
    let e = parse_iso(end);
    human_readable_duration(s, e)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <START_ISO> <END_ISO>", args[0]);
        std::process::exit(1);
    }
    let result = compute_delta(&args[1], &args[2]);
    println!("{}", result);
}
