use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime, TimeZone};
use std::fs;
use std::path::{Path, PathBuf};
use std::time::UNIX_EPOCH;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Temporal Dust Sweeper: Identify and remove old, unused files.", long_about = None)]
struct Args {
    /// Path to the directory to sweep
    #[clap(short, long, default_value = ".")]
    path: PathBuf,

    /// Files older than this many days will be considered 'dust'
    #[clap(short, long, default_value_t = 30)]
    age_days: u64,

    /// Perform a dry run: list files that would be swept, but don't delete them
    #[clap(short, long)]
    dry_run: bool,

    /// Actually sweep (delete) the identified temporal dust
    #[clap(short, long)]
    sweep: bool,

    /// Use last access time instead of last modification time for age calculation
    #[clap(short, long)]
    access_time: bool,

    /// Only consider files matching this regex pattern (e.g., ".*\\.log$")
    #[clap(short, long)]
    pattern: Option<String>,

    /// Only consider files with this extension (e.g., "log", "tmp")
    #[clap(short, long)]
    extension: Option<String>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if args.sweep && args.dry_run {
        eprintln!("Error: Cannot use --sweep and --dry-run simultaneously. Choose one.");
        std::process::exit(1);
    }

    let is_dry_run = args.dry_run || !args.sweep;

    if !args.sweep && !args.dry_run {
        println!("No action specified. Performing a dry run by default. Use --sweep to delete files.");
    }

    let cutoff_time = Utc::now() - Duration::days(args.age_days as i64);
    let mut files_to_process = Vec::new();

    let regex_pattern = args.pattern.as_ref().map(|p| regex::Regex::new(p).map_err(|e| format!("Invalid regex pattern: {}", e))).transpose()?;

    println!("Scanning directory: {}", args.path.display());
    println!("Looking for files older than {} days (cutoff: {})", args.age_days, cutoff_time.to_rfc2822());

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path();
            let metadata = fs::metadata(path)?;

            let file_time_system = if args.access_time {
                metadata.accessed()?
            } else {
                metadata.modified()?
            };

            let file_time: DateTime<Utc> = file_time_system
                .duration_since(UNIX_EPOCH)
                .map_err(|e| format!("File time is before UNIX_EPOCH: {}", e))
                .and_then(|d| Utc.timestamp_opt(d.as_secs() as i64, d.subsec_nanos()).single().ok_or_else(|| "Invalid timestamp".to_string()))?;

            if file_time < cutoff_time {
                let mut include_file = true;

                if let Some(ref re) = regex_pattern {
                    if !re.is_match(&path.to_string_lossy()) {
                        include_file = false;
                    }
                }

                if include_file {
                    if let Some(ref ext) = args.extension {
                        if path.extension().map_or(true, |e| e.to_string_lossy().to_lowercase() != ext.to_lowercase()) {
                            include_file = false;
                        }
                    }
                }

                if include_file {
                    files_to_process.push(path.to_path_buf());
                }
            }
        }
    }

    if files_to_process.is_empty() {
        println!("No temporal dust found in '{}'. The wasteland is clean!", args.path.display());
        return Ok(());
    }

    println!("\nIdentified {} pieces of temporal dust:", files_to_process.len());
    for file_path in &files_to_process {
        println!("  - {}", file_path.display());
    }

    if args.sweep {
        println!("\nSweeping away the temporal dust...");
        for file_path in &files_to_process {
            match fs::remove_file(file_path) {
                Ok(_) => println!("  [SWEPT] {}", file_path.display()),
                Err(e) => eprintln!("  [ERROR] Failed to sweep {}: {}", file_path.display(), e),
            }
        }
        println!("\nTemporal dust sweeping complete. The wasteland is a bit cleaner now!");
    } else if is_dry_run {
        println!("\nThis was a dry run. No files were swept. Use --sweep to remove them.");
    }

    Ok(())
}
