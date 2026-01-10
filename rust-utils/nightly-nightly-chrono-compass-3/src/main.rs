use clap::{Parser, Subcommand};
use chrono::{DateTime, Utc, Duration, Local, TimeZone};
use humantime::format_duration;
use std::str::FromStr;

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance CLI tool for calculating temporal differences and tracking apocalyptic deadlines with whimsical flair.", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Calculate time remaining until a future point.
    Until {
        /// The target datetime (e.g., "2024-12-31T23:59:59Z" or "2024-12-31 23:59:59")
        #[arg(value_parser = parse_datetime)]
        target: DateTime<Utc>,
    },
    /// Calculate time elapsed since a past point.
    Since {
        /// The starting datetime (e.g., "2024-01-01T00:00:00Z" or "2024-01-01 00:00:00")
        #[arg(value_parser = parse_datetime)]
        start: DateTime<Utc>,
    },
    /// Calculate duration between two datetimes.
    Between {
        /// The first datetime
        #[arg(value_parser = parse_datetime)]
        start: DateTime<Utc>,
        /// The second datetime
        #[arg(value_parser = parse_datetime)]
        end: DateTime<Utc>,
    },
    /// Countdown to a pre-defined apocalyptic event.
    Countdown {
        /// Name of the event to countdown to (e.g., "GreatGlitch", "ResourceResupply")
        event: String,
    },
}

// Helper function to parse various datetime formats
fn parse_datetime(arg: &str) -> Result<DateTime<Utc>, String> {
    // Try RFC3339 first (e.g., "2024-12-31T23:59:59Z")
    if let Ok(dt) = DateTime::from_str(arg) {
        return Ok(dt);
    }
    // Try a common local format (e.g., "2024-12-31 23:59:59") and assume local timezone
    if let Ok(dt_local) = Local.datetime_from_str(arg, "%Y-%m-%d %H:%M:%S") {
        return Ok(dt_local.to_utc());
    }
    // Try date only (e.g., "2024-12-31") and assume start of day in local timezone
    if let Ok(dt_local) = Local.datetime_from_str(arg, "%Y-%m-%d") {
        return Ok(dt_local.to_utc());
    }
    Err(format!("Could not parse datetime: {}. Expected formats like '2024-12-31T23:59:59Z', '2024-12-31 23:59:59', or '2024-12-31'.", arg))
}

// Mock rationale: In a real-world scenario, `Utc::now()` would be used.
// For deterministic tests, we need a way to control the "current" time.
// This `get_current_time` function allows us to inject a mock time for testing.
#[cfg(test)]
fn get_current_time() -> DateTime<Utc> {
    // For tests, we use a fixed "now"
    Utc.with_ymd_and_hms(2024, 7, 15, 12, 0, 0).unwrap()
}

#[cfg(not(test))]
fn get_current_time() -> DateTime<Utc> {
    Utc::now()
}

fn main() {
    let cli = Cli::parse();
    let now = get_current_time();

    match &cli.command {
        Commands::Until { target } => {
            if *target < now {
                println!("The target time has already passed, survivor! It was {} ago.", format_duration(now.signed_duration_since(*target).to_std().unwrap()));
            } else {
                let duration = target.signed_duration_since(now);
                println!("Only {} until the next temporal anomaly! Stay vigilant!", format_duration(duration.to_std().unwrap()));
            }
        }
        Commands::Since { start } => {
            if *start > now {
                println!("That event is in the future, wanderer. It will be {} from now.", format_duration(start.signed_duration_since(now).to_std().unwrap()));
            } else {
                let duration = now.signed_duration_since(*start);
                println!("It has been {} since that moment. Time flies, even in the apocalypse.", format_duration(duration.to_std().unwrap()));
            }
        }
        Commands::Between { start, end } => {
            let duration = if *start <= *end {
                end.signed_duration_since(*start)
            } else {
                start.signed_duration_since(*end)
            };
            println!("The temporal span between those points is {}. A blink in the void.", format_duration(duration.to_std().unwrap()));
        }
        Commands::Countdown { event } => {
            // Pre-defined apocalyptic events (for whimsy and determinism)
            let events: std::collections::HashMap<&str, DateTime<Utc>> = [
                ("GreatGlitch", Utc.with_ymd_and_hms(2025, 1, 1, 0, 0, 0).unwrap()),
                ("ResourceResupply", Utc.with_ymd_and_hms(2024, 7, 20, 8, 0, 0).unwrap()),
                ("VoidWhisperPeak", Utc.with_ymd_and_hms(2024, 8, 1, 22, 30, 0).unwrap()),
                ("FirstAnomaly", Utc.with_ymd_and_hms(2024, 7, 10, 0, 0, 0).unwrap()), // Added a past event for testing
            ].iter().cloned().collect();

            if let Some(event_time) = events.get(event.as_str()) {
                if *event_time < now {
                    println!("The '{}' event has already transpired, traveler. It was {} ago.", event, format_duration(now.signed_duration_since(*event_time).to_std().unwrap()));
                } else {
                    let duration = event_time.signed_duration_since(now);
                    println!("Countdown to {}: {} remaining! Prepare for the inevitable.", event, format_duration(duration.to_std().unwrap()));
                }
            } else {
                println!("Unknown apocalyptic event: '{}'. Perhaps it's a secret timeline?", event);
            }
        }
    }
}
