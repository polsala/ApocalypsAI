use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::fs;
use std::path::PathBuf;
use std::error::Error;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to start sweeping for digital dust bunnies
    #[arg(short, long, default_value = ".")]
    path: PathBuf,

    /// Files older than this many days will be considered dust bunnies
    #[arg(short, long, default_value_t = 30)]
    age_days: u64,

    /// Perform a dry run without deleting any files
    #[arg(short, long)]
    dry_run: bool,

    /// Delete the identified dust bunnies (use with caution!)
    #[arg(short = 'D', long)] // Use 'D' to avoid conflict with dry_run 'd' if both were short
    delete: bool,
}

/// Core logic for sweeping digital dust bunnies.
/// Returns the count of dust bunnies found.
fn run_sweeper_logic(args: &Args) -> Result<usize, Box<dyn Error>> {
    let cutoff_time = Utc::now() - Duration::days(args.age_days as i64);
    let mut found_dust_bunnies = 0;

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_utc: DateTime<Utc> = modified_time.into();
                    if modified_utc < cutoff_time {
                        found_dust_bunnies += 1;
                        println!("  Found dust bunny: {} (modified: {})", path.display(), modified_utc.format("%Y-%m-%d %H:%M:%S"));
                        if args.delete && !args.dry_run {
                            match fs::remove_file(path) {
                                Ok(_) => println!("    -> Swept away!"),
                                Err(e) => eprintln!("    -> Failed to sweep {}: {}", path.display(), e),
                            }
                        }
                    }
                }
            }
        }
    }
    Ok(found_dust_bunnies)
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    if args.delete && args.dry_run {
        eprintln!("Error: Cannot use --delete and --dry-run together. Choose one.");
        std::process::exit(1);
    }

    println!("Sweeping for digital dust bunnies older than {} days in: {}", args.age_days, args.path.display());
    if args.dry_run {
        println!("(Dry run: no files will be deleted)");
    } else if args.delete {
        println!("(Deletion mode: files WILL be deleted!)");
    }

    let total_found = run_sweeper_logic(&args)?;
    println!("\nSweep complete. Found {} digital dust bunnies.", total_found);

    Ok(())
}
