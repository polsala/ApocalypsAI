use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::path::PathBuf;
use std::fs;
use human_bytes::human_bytes;

#[derive(Parser, Debug)]
#[command(author, version, about = "A whimsical CLI tool to find old, unused files (digital dust bunnies) in your file system.", long_about = None)]
struct Args {
    /// The directory to scan for digital dust bunnies.
    #[arg(name = "PATH")]
    path: PathBuf,

    /// The minimum age in days for a file to be considered a 'dust bunny'.
    #[arg(short = 'a', long, default_value_t = 90)]
    age: u64,

    /// Enable verbose output, showing more details about each file.
    #[arg(short = 'v', long)]
    verbose: bool,
}

struct DigitalDustBunny {
    path: PathBuf,
    size: u664,
    age_days: i64,
    fluffiness_score: f64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let target_dir = &args.path;
    let min_age_days = args.age;

    if !target_dir.is_dir() {
        eprintln!("Error: Provided path is not a directory: {}", target_dir.display());
        std::process::exit(1);
    }

    let now = Utc::now();
    let mut dust_bunnies: Vec<DigitalDustBunny> = Vec::new();

    println!("Scanning '{}' for digital dust bunnies older than {} days...\n", target_dir.display(), min_age_days);

    for entry in WalkDir::new(target_dir).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path().to_path_buf();
            if let Ok(metadata) = fs::metadata(&path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_dt: DateTime<Utc> = modified_time.into();
                    let duration = now.signed_duration_since(modified_dt);
                    let age_days = duration.num_days();

                    if age_days >= min_age_days as i64 {
                        let size = metadata.len();
                        let size_kb = size as f64 / 1024.0;
                        let fluffiness_score = (age_days as f64 * size_kb) / 1000.0;

                        dust_bunnies.push(DigitalDustBunny {
                            path,
                            size,
                            age_days,
                            fluffiness_score,
                        });
                    }
                }
            }
        }
    }

    if dust_bunnies.is_empty() {
        println!("No digital dust bunnies found. Your digital space is sparkling clean!");
    } else {
        println!("Digital Dust Bunnies found in '{}':", target_dir.display());
        println!("---------------------------------------");
        for bunny in dust_bunnies {
            let size_human = human_bytes(bunny.size as f64);
            println!("Path: {}, Size: {}, Age: {} days, Fluffiness: {:.1}",
                     bunny.path.display(), size_human, bunny.age_days, bunny.fluffiness_score);
        }
        println!("---------------------------------------");
        println!("Total Dust Bunnies: {}", dust_bunnies.len());
    }

    Ok(())
}
