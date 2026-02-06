use clap::Parser;
use nightly_fallout_time_cli::format_fallout;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// ISO8601 timestamp (e.g., 2023-08-15T14:23:00Z)
    timestamp: String,
}

fn main() {
    let args = Args::parse();
    match format_fallout(&args.timestamp) {
        Ok(s) => println!("{}", s),
        Err(e) => eprintln!("Error parsing timestamp: {}", e),
    }
}
