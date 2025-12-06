use std::{
    fs,
    path::{Path, PathBuf},
    time::SystemTime,
};
use walkdir::WalkDir;
use chrono::{Duration, Utc, DateTime, TimeZone};
use clap::Parser;

#[derive(Parser, Debug)]
#[command(author, version, about = "Identifies and lists old, unused files as 'digital relics'.", long_about = None)]
struct Args {
    /// The directory to scan for relics.
    #[arg(short, long, default_value = ".")]
    path: PathBuf,

    /// The age threshold in days. Files older than this will be considered relics.
    #[arg(short, long, default_value_t = 90)]
    age_days: u64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let threshold_duration = Duration::days(args.age_days as i64);
    let now = Utc::now();

    println!("Scanning '{}' for files older than {} days...", args.path.display(), args.age_days);
    println!("--- Digital Relics Found ---");

    let mut found_relics = 0;

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_datetime: DateTime<Utc> = modified_time.into();
                    if now.signed_duration_since(modified_datetime) > threshold_duration {
                        println!("  {} (Modified: {})", path.display(), modified_datetime.format("%Y-%m-%d"));
                        found_relics += 1;
                    }
                }
            }
        }
    }

    println!("----------------------------");
    println!("Found {} digital relics.", found_relics);

    Ok(())
}
