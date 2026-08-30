use std::io::{self, Read};
use chrono::{DateTime, Utc};
use clap::Parser;
use csv::ReaderBuilder;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to the observation data file. If not provided, reads from stdin.
    #[arg(short, long)]
    file: Option<String>,
}

// Custom deserializer for ISO8601 string to DateTime<Utc>
mod datetime_parser {
    use chrono::{DateTime, Utc};
    use serde::{self, Deserialize, Deserializer};

    pub fn deserialize<'de, D>(deserializer: D) -> Result<DateTime<Utc>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let s = String::deserialize(deserializer)?;
        s.parse::<DateTime<Utc>>().map_err(serde::de::Error::custom)
    }
}

#[derive(Debug, serde::Deserialize)]
struct Observation {
    #[serde(with = "datetime_parser")]
    timestamp: DateTime<Utc>,
    offset_seconds: f64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let reader: Box<dyn Read> = match args.file {
        Some(path) => Box::new(std::fs::File::open(path)?),
        None => Box::new(io::stdin()),
    };

    let mut rdr = ReaderBuilder::new()
        .has_headers(false) // Assuming no header row
        .delimiter(b',')
        .from_reader(reader);

    let mut total_offset = 0.0;
    let mut count = 0;
    let mut min_timestamp: Option<DateTime<Utc>> = None;
    let mut max_timestamp: Option<DateTime<Utc>> = None;

    for result in rdr.deserialize::<Observation>() {
        let record = result?;
        total_offset += record.offset_seconds;
        count += 1;

        if min_timestamp.is_none() || record.timestamp < min_timestamp.unwrap() {
            min_timestamp = Some(record.timestamp);
        }
        if max_timestamp.is_none() || record.timestamp > max_timestamp.unwrap() {
            max_timestamp = Some(record.timestamp);
        }
    }

    if count == 0 {
        println!("No observations found. Cannot calibrate chrono-compass.");
        return Ok(());
    }

    let average_offset = total_offset / count as f64;

    println!("--- Chrono-Compass Calibration Report ---");
    println!("Total observations processed: {}", count);
    if let (Some(min_ts), Some(max_ts)) = (min_timestamp, max_timestamp) {
        println!("Observation period: {} to {}", min_ts.to_rfc3339(), max_ts.to_rfc3339());
    }
    println!("Average observed clock offset: {:.2} seconds", average_offset);

    if average_offset > 0.0 {
        println!("Your local clock appears to be behind true time.");
        println!("Suggested immediate correction: Advance local clock by {:.2} seconds.", average_offset);
    } else if average_offset < 0.0 {
        println!("Your local clock appears to be ahead of true time.");
        println!("Suggested immediate correction: Retard local clock by {:.2} seconds.", average_offset.abs());
    } else {
        println!("Your local clock appears to be perfectly synchronized. No correction needed.");
    }

    Ok(())
}
