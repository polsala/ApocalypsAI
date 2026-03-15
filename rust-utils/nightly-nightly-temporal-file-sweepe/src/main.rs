use clap::Parser;
use chrono::{Duration, Utc, DateTime, Local};
use walkdir::WalkDir;
use std::fs;
use std::path::{Path, PathBuf};
use anyhow::{Result, Context};

#[derive(Parser, Debug)]
#[command(author, version, about = "Nightly Temporal File Sweeper: Cleanse your digital realm of temporal dust bunnies!", long_about = None)]
struct Args {
    /// The root directory to scan for temporal dust bunnies.
    #[arg(short, long, value_name = "PATH")]
    path: PathBuf,

    /// Minimum age for a file to be considered a temporal dust bunny (e.g., "30d", "1w", "6m", "1y").
    #[arg(short, long, value_name = "AGE_STRING")]
    age: String,

    /// Action to perform: 'list' (default), 'move', or 'delete'.
    #[arg(short, long, default_value = "list", value_name = "ACTION")]
    action: String,

    /// Directory to move files to if action is 'move'.
    #[arg(short = 'A', long, value_name = "ARCHIVE_PATH")]
    archive_dir: Option<PathBuf>,

    /// Scan subdirectories recursively.
    #[arg(short, long)]
    recursive: bool,

    /// Perform a dry run (don't make any changes).
    #[arg(short, long)]
    dry_run: bool,

    /// Be verbose, print more details.
    #[arg(short, long)]
    verbose: bool,
}

fn parse_age_string(age_str: &str) -> Result<Duration> {
    let num_str = age_str.trim_end_matches(|c: char| !c.is_ascii_digit());
    let unit_str = age_str.trim_start_matches(|c: char| c.is_ascii_digit());

    let num: i64 = num_str.parse().context("Invalid age number format")?;

    match unit_str {
        "d" => Ok(Duration::days(num)),
        "w" => Ok(Duration::weeks(num)),
        "m" => Ok(Duration::days(num * 30)), // Approximate month
        "y" => Ok(Duration::days(num * 365)), // Approximate year
        _ => Err(anyhow::anyhow!("Invalid age unit. Use 'd' (days), 'w' (weeks), 'm' (months), or 'y' (years).")),
    }
}

fn get_file_mtime(path: &Path) -> Result<DateTime<Utc>> {
    let metadata = fs::metadata(path).context(format!("Failed to get metadata for {:?}", path))?;
    let mtime = metadata.modified().context("Failed to get modification time")?;
    Ok(DateTime::<Utc>::from(mtime))
}

fn main() -> Result<()> {
    let args = Args::parse();

    if !args.path.exists() {
        return Err(anyhow::anyhow!("Error: Scan path does not exist: {:?}", args.path));
    }
    if !args.path.is_dir() {
        return Err(anyhow::anyhow!("Error: Scan path is not a directory: {:?}", args.path));
    }

    let min_age_duration = parse_age_string(&args.age)?;
    let cutoff_time = Utc::now() - min_age_duration;

    if args.verbose {
        println!("Scanning {:?} for files older than {} (cutoff: {})",
                 args.path, args.age, cutoff_time.with_timezone(&Local).format("%Y-%m-%d %H:%M:%S"));
        println!("Action: {}, Dry Run: {}", args.action, args.dry_run);
    }

    let mut dust_bunnies = Vec::new();
    let walker = if args.recursive {
        WalkDir::new(&args.path)
    } else {
        WalkDir::new(&args.path).max_depth(1)
    };

    for entry in walker.into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            match get_file_mtime(path) {
                Ok(mtime) => {
                    if mtime < cutoff_time {
                        dust_bunnies.push(path.to_path_buf());
                    }
                },
                Err(e) => {
                    if args.verbose {
                        eprintln!("Warning: Could not get modification time for {:?}: {}", path, e);
                    }
                }
            }
        }
    }

    if dust_bunnies.is_empty() {
        println!("No temporal dust bunnies found in {:?}", args.path);
        return Ok(());
    }

    println!("Found {} temporal dust bunnies:", dust_bunnies.len());
    for bunny_path in &dust_bunnies {
        println!("  - {:?}", bunny_path);
    }

    if args.dry_run {
        println!("\nDry run complete. No changes were made.");
        return Ok(());
    }

    match args.action.as_str() {
        "list" => { /* Already listed */ },
        "move" => {
            let archive_dir = args.archive_dir.context("Archive directory is required for 'move' action.")?;
            fs::create_dir_all(&archive_dir).context(format!("Failed to create archive directory {:?}", archive_dir))?;
            println!("\nMoving temporal dust bunnies to {:?}", archive_dir);
            for bunny_path in dust_bunnies {
                let file_name = bunny_path.file_name().context("File has no name?")?;
                let dest_path = archive_dir.join(file_name);
                match fs::rename(&bunny_path, &dest_path) {
                    Ok(_) => println!("  Moved {:?} to {:?}", bunny_path, dest_path),
                    Err(e) => eprintln!("  Error moving {:?}: {}", bunny_path, e),
                }
            }
        },
        "delete" => {
            println!("\nDeleting temporal dust bunnies...");
            for bunny_path in dust_bunnies {
                match fs::remove_file(&bunny_path) {
                    Ok(_) => println!("  Deleted {:?}", bunny_path),
                    Err(e) => eprintln!("  Error deleting {:?}: {}", bunny_path, e),
                }
            }
        },
        _ => return Err(anyhow::anyhow!("Invalid action: {}. Use 'list', 'move', or 'delete'.", args.action)),
    }

    println!("\nTemporal cleansing complete!");
    Ok(())
}
