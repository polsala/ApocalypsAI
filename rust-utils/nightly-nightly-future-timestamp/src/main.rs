use chrono::{DateTime, Duration, Utc};
use regex::Regex;
use std::env;

fn parse_duration(input: &str) -> Result<Duration, String> {
    // Regex captures optional groups for days, hours, minutes, seconds
    let re = Regex::new(r"(?i)^(?:(?P<days>\d+)d)?(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?$")
        .map_err(|e| format!("Invalid regex: {}", e))?;
    let caps = re.captures(input).ok_or_else(|| format!("Could not parse duration '{}'. Expected format like '2d5h30m'", input))?;

    let days = caps.name("days").map_or(0, |m| m.as_str().parse::<i64>().unwrap_or(0));
    let hours = caps.name("hours").map_or(0, |m| m.as_str().parse::<i64>().unwrap_or(0));
    let minutes = caps.name("minutes").map_or(0, |m| m.as_str().parse::<i64>().unwrap_or(0));
    let seconds = caps.name("seconds").map_or(0, |m| m.as_str().parse::<i64>().unwrap_or(0));

    if days == 0 && hours == 0 && minutes == 0 && seconds == 0 {
        return Err(format!("Duration '{}' does not contain any recognizable component", input));
    }

    Ok(Duration::seconds(seconds)
        + Duration::minutes(minutes)
        + Duration::hours(hours)
        + Duration::days(days))
}

/// Adds a parsed duration to a given base datetime.
/// This function is pure and therefore easy to test.
pub fn add_duration(base: DateTime<Utc>, dur_str: &str) -> Result<DateTime<Utc>, String> {
    let dur = parse_duration(dur_str)?;
    Ok(base + dur)
}

fn print_usage() {
    eprintln!("Usage: nightly-future-timestamp <duration>");
    eprintln!("Duration format: combination of <number>d, <number>h, <number>m, <number>s (e.g., '2d5h30m')");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        print_usage();
        std::process::exit(1);
    }
    let dur_str = &args[1];
    match add_duration(Utc::now(), dur_str) {
        Ok(future) => println!("{}", future.to_rfc3339()),
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::TimeZone;

    #[test]
    fn test_parse_simple() {
        let dur = parse_duration("1h").expect("should parse");
        assert_eq!(dur, Duration::hours(1));
    }

    #[test]
    fn test_parse_complex() {
        let dur = parse_duration("2d5h30m").expect("should parse");
        let expected = Duration::days(2) + Duration::hours(5) + Duration::minutes(30);
        assert_eq!(dur, expected);
    }

    #[test]
    fn test_add_duration() {
        // Fixed base time: 2023-01-01T00:00:00Z
        let base = Utc.ymd(2023, 1, 1).and_hms(0, 0, 0);
        let future = add_duration(base, "1d2h").expect("add should succeed");
        let expected = Utc.ymd(2023, 1, 2).and_hms(2, 0, 0);
        assert_eq!(future, expected);
    }

    #[test]
    fn test_invalid_duration() {
        let err = parse_duration("abc").unwrap_err();
        assert!(err.contains("Could not parse duration"));
    }
}
