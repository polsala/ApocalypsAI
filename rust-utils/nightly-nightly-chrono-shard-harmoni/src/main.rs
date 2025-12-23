use clap::Parser;
use chrono::{DateTime, FixedOffset, Utc, Duration};
use std::collections::HashMap;
use std::io::{self, BufRead};
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Harmonize fragmented chronological data shards, detecting temporal rifts and echoes.", long_about = None)]
struct Args {
    /// Path to the input file. If not provided, reads from stdin.
    #[clap(name = "FILE")]
    file: Option<PathBuf>,

    /// Define the maximum allowed time difference (in seconds) between consecutive entries before it's considered a "Temporal Rift".
    #[clap(short = 't', long, default_value = "60")]
    gap_threshold: i64,

    /// Output the harmonized (sorted and de-duplicated by timestamp) data to stdout. By default, only the anomaly report is printed.
    #[clap(short = 'o', long)]
    output_harmonized: bool,
    
    /// Specify the timestamp format. Uses RFC3339 by default.
    /// Example: "%Y-%m-%dT%H:%M:%SZ" for "2023-01-01T10:00:00Z"
    /// Currently only RFC3339 is fully supported for robust parsing.
    #[clap(short = 'f', long, default_value = "rfc3339")]
    timestamp_format: String,
}

#[derive(Debug)]
struct DataShard {
    timestamp: DateTime<FixedOffset>,
    original_line: String,
}

fn parse_timestamp(line: &str, format: &str) -> Option<DateTime<FixedOffset>> {
    // For simplicity, we'll primarily support RFC3339.
    // Extending this to custom formats would require more complex logic or a different chrono parsing function.
    // For this utility, let's assume the timestamp is at the beginning and is RFC3339 compliant.
    // A more robust solution would use regex or look for specific patterns.
    let parts: Vec<&str> = line.splitn(2, ' ').collect();
    if parts.is_empty() {
        return None;
    }

    match format {
        "rfc3339" => DateTime::parse_from_rfc3339(parts[0]).ok(),
        // Add more formats here if needed, e.g.,
        // "rfc2822" => DateTime::parse_from_rfc2822(parts[0]).ok(),
        // custom_format => DateTime::parse_from_str(parts[0], custom_format).ok(),
        _ => {
            eprintln!("Warning: Only 'rfc3339' format is fully supported. Attempting RFC3339 parsing.");
            DateTime::parse_from_rfc3339(parts[0]).ok()
        }
    }
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let reader: Box<dyn BufRead> = if let Some(file_path) = &args.file {
        let file = std::fs::File::open(file_path)?;
        Box::new(io::BufReader::new(file))
    } else {
        Box::new(io::BufReader::new(io::stdin()))
    };

    let mut shards: Vec<DataShard> = Vec::new();
    let mut original_lines_count = 0;
    let mut out_of_order_count = 0;
    let mut last_timestamp_in_input: Option<DateTime<FixedOffset>> = None;

    for line_result in reader.lines() {
        let line = line_result?;
        original_lines_count += 1;

        if let Some(timestamp) = parse_timestamp(&line, &args.timestamp_format) {
            shards.push(DataShard {
                timestamp,
                original_line: line.clone(),
            });

            if let Some(last_ts) = last_timestamp_in_input {
                if timestamp < last_ts {
                    out_of_order_count += 1;
                }
            }
            last_timestamp_in_input = Some(timestamp);
        } else {
            eprintln!("Warning: Could not parse timestamp from line: \"{}\"
", line);
        }
    }

    if shards.is_empty() {
        println!("No valid timestamped data shards found to harmonize.");
        return Ok(());
    }

    // Sort shards by timestamp
    shards.sort_by_key(|s| s.timestamp);

    let mut echoes_of_time: HashMap<DateTime<FixedOffset>, usize> = HashMap::new();
    let mut temporal_rifts: Vec<(DateTime<FixedOffset>, DateTime<FixedOffset>, Duration)> = Vec::new();
    let mut harmonized_shards: Vec<DataShard> = Vec::new();

    let mut prev_shard: Option<&DataShard> = None;

    for shard in shards.iter() {
        if let Some(prev) = prev_shard {
            // Check for Echoes of Time
            if shard.timestamp == prev.timestamp {
                *echoes_of_time.entry(shard.timestamp).or_insert(0) += 1;
            }

            // Check for Temporal Rifts
            let duration = shard.timestamp - prev.timestamp;
            if duration > Duration::seconds(args.gap_threshold) {
                temporal_rifts.push((prev.timestamp, shard.timestamp, duration));
            }
        }
        
        // Add to harmonized_shards, de-duplicating by timestamp if output_harmonized is true
        if args.output_harmonized {
            if harmonized_shards.last().map_or(true, |last| last.timestamp != shard.timestamp) {
                harmonized_shards.push(DataShard {
                    timestamp: shard.timestamp,
                    original_line: shard.original_line.clone(),
                });
            }
        }

        prev_shard = Some(shard);
    }

    println!("Harmonization Report:");
    println!("---------------------");
    println!("Input lines processed: {}", original_lines_count);
    println!("Valid data shards found: {}", shards.len());
    
    if out_of_order_count > 0 {
        println!("Original order: Chronological Drift Detected ({} out-of-order instances)", out_of_order_count);
    } else {
        println!("Original order: Perfectly aligned.");
    }

    if !echoes_of_time.is_empty() {
        println!("Echoes of Time (Duplicate Timestamps): {}", echoes_of_time.len());
        for (ts, count) in echoes_of_time.iter() {
            println!("  - {} ({} occurrences)", ts.to_rfc3339(), count + 1); // +1 because the first instance isn't counted as a duplicate
        }
    } else {
        println!("Echoes of Time: None detected.");
    }

    if !temporal_rifts.is_empty() {
        println!("Temporal Rifts (Gaps > {}s): {}", args.gap_threshold, temporal_rifts.len());
        for (start, end, duration) in temporal_rifts.iter() {
            println!("  - Rift detected between {} and {} (Duration: {}s)",
                     start.to_rfc3339(), end.to_rfc3339(), duration.num_seconds());
        }
    } else {
        println!("Temporal Rifts: None detected.");
    }

    if args.output_harmonized {
        println!("\n--- Harmonized Data Shards ---");
        for shard in harmonized_shards {
            println!("{}", shard.original_line);
        }
    }

    Ok(())
}
