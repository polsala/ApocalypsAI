use clap::Parser;
use walkdir::WalkDir;
use chrono::{DateTime, Utc, Duration};
use std::path::PathBuf;
use std::fs;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to scan for digital relics
    #[arg(short, long, value_name = "PATH")]
    path: PathBuf,

    /// Minimum age in days for a file to be considered a relic
    #[arg(short, long, default_value_to = "90", value_name = "DAYS")]
    min_age_days: i64,
}

struct Relic {
    path: PathBuf,
    modified: DateTime<Utc>,
    size: u64,
    age_days: i64,
}

fn find_relics(path: &PathBuf, min_age_days: i64, now: DateTime<Utc>) -> Vec<Relic> {
    let mut relics = Vec::new();
    let min_age_duration = Duration::days(min_age_days);

    for entry in WalkDir::new(path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            if let Ok(metadata) = entry.metadata() {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_utc: DateTime<Utc> = modified_time.into();
                    let age = now.signed_duration_since(modified_utc);

                    if age >= min_age_duration {
                        relics.push(Relic {
                            path: entry.path().to_path_buf(),
                            modified: modified_utc,
                            size: metadata.len(),
                            age_days: age.num_days(),
                        });
                    }
                }
            }
        }
    }
    relics
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let now = Utc::now(); // Use actual current time for main execution

    if !args.path.exists() {
        eprintln!("Error: Path '{}' does not exist.", args.path.display());
        std::process::exit(1);
    }
    if !args.path.is_dir() {
        eprintln!("Error: Path '{}' is not a directory.", args.path.display());
        std::process::exit(1);
    }

    let relics = find_relics(&args.path, args.min_age_days, now);

    if relics.is_empty() {
        println!("No digital relics found older than {} days in '{}'. Your digital space is pristine!", args.min_age_days, args.path.display());
    } else {
        println!("Discovered {} digital relics older than {} days in '{}':", relics.len(), args.min_age_days, args.path.display());
        println!("{:<70} {:<25} {:<15} {:<10}", "PATH", "LAST MODIFIED (UTC)", "SIZE (bytes)", "AGE (days)");
        println!("{}", "-".repeat(120));
        for relic in relics {
            println!("{:<70} {:<25} {:<15} {:<10}",
                     relic.path.display(),
                     relic.modified.format("%Y-%m-%d %H:%M:%S"),
                     relic.size,
                     relic.age_days);
        }
    }

    Ok(())
}
