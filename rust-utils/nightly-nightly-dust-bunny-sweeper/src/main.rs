use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::fs;
use std::path::PathBuf;
use std::error::Error;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
pub struct Args {
    /// The directory to sweep for digital dust bunnies
    #[clap(short, long, value_parser, default_value = ".")]
    pub path: PathBuf,

    /// The age in days after which a file is considered a dust bunny
    #[clap(short, long, value_parser, default_value_t = 90)]
    pub age_days: u64,

    /// Perform a dry run without actually deleting or archiving files
    #[clap(short, long)]
    pub dry_run: bool,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();
    run_sweeper(args)
}

pub fn run_sweeper(args: Args) -> Result<(), Box<dyn Error>> {
    println!("Sweeping for digital dust bunnies in: {}", args.path.display());
    println!("Looking for files older than {} days...", args.age_days);
    if args.dry_run {
        println!("(Dry run mode: no files will be touched)");
    }

    let threshold_time = Utc::now() - Duration::days(args.age_days as i64);
    let mut dust_bunnies_found = 0;

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_utc: DateTime<Utc> = modified_time.into();
                    if modified_utc < threshold_time {
                        dust_bunnies_found += 1;
                        println!("  Dust Bunny found: {} (Last modified: {})", path.display(), modified_utc.format("%Y-%m-%d %H:%M:%S"));
                    }
                }
            }
        }
    }

    if dust_bunnies_found == 0 {
        println!("\nNo digital dust bunnies found! Your digital space is sparkling clean.");
    } else {
        println!("\nSweeping complete! Found {} digital dust bunnies.", dust_bunnies_found);
        if args.dry_run {
            println!("(Remember, this was a dry run. To sweep them away, run without --dry-run)");
        } else {
            println!("(This version only reports. A future version might sweep them away!)");
        }
    }

    Ok(())
}
