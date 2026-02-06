use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use humantime::format_duration;

#[derive(Parser, Debug)]
#[clap(author, version, about = "A high-performance Rust CLI tool to identify and report on stale or unused files and directories, helping to clear digital clutter.", long_about = None)]
struct Args {
    /// The root directory to start scanning from.
    #[clap(name = "PATH")]
    path: PathBuf,

    /// Report files/directories not modified in the last DAYS days.
    #[clap(short = 'a', long, value_name = "DAYS")]
    age: Option<u64>,

    /// Report files/directories larger than MB megabytes.
    #[clap(short = 's', long, value_name = "MB")]
    size: Option<u64>,

    /// Show more detailed information about each dust bunny.
    #[clap(short = 'v', long)]
    verbose: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if args.age.is_none() && args.size.is_none() {
        eprintln!("Error: At least one of --age or --size must be specified.");
        std::process::exit(1);
    }

    let now = SystemTime::now();
    let age_threshold = args.age.map(|days| now - Duration::from_days(days));
    let size_threshold_bytes = args.size.map(|mb| mb * 1024 * 1024); // Convert MB to bytes

    println!("Scanning for digital dust bunnies in: {}", args.path.display());
    println!("Criteria: {}", {
        let mut criteria_str = String::new();
        if let Some(days) = args.age {
            criteria_str.push_str(&format!("Older than {} days", days));
        }
        if let Some(mb) = args.size {
            if !criteria_str.is_empty() {
                criteria_str.push_str(" AND ");
            }
            criteria_str.push_str(&format!("Larger than {} MB", mb));
        }
        criteria_str
    });
    println!("--------------------------------------------------");

    let mut dust_bunnies_found = 0;
    find_dust_bunnies(
        &args.path,
        age_threshold,
        size_threshold_bytes,
        now,
        args.verbose,
        &mut dust_bunnies_found,
    )?;

    println!("--------------------------------------------------");
    if dust_bunnies_found == 0 {
        println!("No digital dust bunnies found! Your digital space is sparkling clean.");
    } else {
        println!("Found {} digital dust bunnies. Time for a digital spring clean!", dust_bunnies_found);
    }

    Ok(())
}

fn find_dust_bunnies(
    path: &Path,
    age_threshold: Option<SystemTime>,
    size_threshold_bytes: Option<u64>,
    now: SystemTime,
    verbose: bool,
    count: &mut u32,
) -> Result<(), Box<dyn std::error::Error>> {
    if !path.exists() {
        eprintln!("Warning: Path does not exist: {}", path.display());
        return Ok(());
    }

    for entry in fs::read_dir(path)? {
        let entry = entry?;
        let metadata = entry.metadata()?;
        let file_type = metadata.file_type();
        let path = entry.path();

        let mut is_dust_bunny = false;
        let mut reasons = Vec::new();

        // Check age
        if let Some(threshold) = age_threshold {
            if let Ok(modified_time) = metadata.modified() {
                if modified_time < threshold {
                    is_dust_bunny = true;
                    let duration = now.duration_since(modified_time).unwrap_or_default();
                    reasons.push(format!("Modified {} ago", format_duration(duration).to_string()));
                }
            }
        }

        // Check size
        if let Some(threshold_bytes) = size_threshold_bytes {
            if metadata.len() > threshold_bytes {
                is_dust_bunny = true; // If size criteria is met, it's a dust bunny (OR condition with age)
                reasons.push(format!("Size: {:.2} MB", metadata.len() as f64 / (1024.0 * 1024.0)));
            }
        }

        if is_dust_bunny {
            *count += 1;
            print!("  [DUST BUNNY] {}", path.display());
            if verbose {
                print!(" ({})", reasons.join(", "));
            }
            println!();
        }

        // Recursively check directories
        if file_type.is_dir() {
            // Avoid following symlinks to prevent infinite loops or scanning outside the intended scope
            if !file_type.is_symlink() {
                find_dust_bunnies(&path, age_threshold, size_threshold_bytes, now, verbose, count)?;
            }
        }
    }
    Ok(())
}

// Helper for Duration::from_days, not available in std::time::Duration directly
trait DurationExt {
    fn from_days(days: u64) -> Duration;
}

impl DurationExt for Duration {
    fn from_days(days: u64) -> Duration {
        Duration::from_secs(days * 24 * 60 * 60)
    }
}
