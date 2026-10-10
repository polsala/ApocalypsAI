use clap::Parser;
use nightly_chrono_compass::{calculate_and_format_distance};

/// A whimsical CLI tool to calculate the "temporal distance" between two timestamps.
/// Expresses the duration in standard units and "flickers of eternity".
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The starting timestamp (e.g., "2023-01-01T12:00:00Z", "2023-01-01 12:00:00 UTC", or "2023-01-01 12:00:00")
    #[arg(short, long)]
    start_time: String,

    /// The ending timestamp (e.g., "2023-01-02T13:30:00Z", "2023-01-02 13:30:00 UTC", or "2023-01-02 13:30:00")
    #[arg(short, long)]
    end_time: String,
}

fn main() {
    let args = Args::parse();

    match calculate_and_format_distance(&args.start_time, &args.end_time) {
        Ok(output) => println!("{}", output),
        Err(e) => eprintln!("Error: {}", e),
    }
}
