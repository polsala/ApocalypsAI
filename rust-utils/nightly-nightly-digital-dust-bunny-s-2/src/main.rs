use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::path::{Path, PathBuf};
use std::fs;
use std::io::{self, Write};
use humantime::parse_duration;

#[derive(Parser, Debug)]
#[command(author, version, about = "A whimsical yet powerful command-line utility to unearth and categorize old, unused files.", long_about = None)]
struct Args {
    /// The directory to scan for digital dust bunnies
    #[arg(short, long)]
    path: PathBuf,

    /// Minimum age for a file to be considered (e.g., "30d", "1y", "2w"). Defaults to 90 days.
    #[arg(short, long, default_value = "90d")]
    age: String,

    /// Perform a dry run without suggesting actual deletion commands
    #[arg(short, long)]
    dry_run: bool,

    /// Enable verbose output
    #[arg(short, long)]
    verbose: bool,
}

#[derive(Debug)]
struct DustBunny {
    path: PathBuf,
    size: u64,
    last_accessed: Option<DateTime<Utc>>,
    last_modified: Option<DateTime<Utc>>,
    category: String,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    if !args.path.exists() {
        eprintln!("Error: Path '{}' does not exist.", args.path.display());
        std::process::exit(1);
    }
    if !args.path.is_dir() {
        eprintln!("Error: Path '{}' is not a directory.", args.path.display());
        std::process::exit(1);
    }

    let min_age_duration = match parse_duration(&args.age) {
        Ok(d) => Duration::from_std(d).expect("Failed to convert std::time::Duration to chrono::Duration"),
        Err(_) => {
            eprintln!("Error: Invalid age format. Please use formats like '30d', '1y', '2w'.");
            std::process::exit(1);
        }
    };

    let cutoff_time = Utc::now() - min_age_duration;

    println!("Scanning '{}' for digital dust bunnies older than {}...", args.path.display(), args.age);
    if args.dry_run {
        println!("(Dry run mode: no files will be deleted or modified.)");
    }

    let mut dust_bunnies: Vec<DustBunny> = Vec::new();

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        let metadata = match fs::metadata(path) {
            Ok(m) => m,
            Err(e) => {
                if args.verbose {
                    eprintln!("Warning: Could not get metadata for {}: {}", path.display(), e);
                }
                continue;
            }
        };

        let is_dir = metadata.is_dir();
        let file_size = metadata.len();

        let last_accessed = metadata.accessed().ok().map(DateTime::<Utc>::from);
        let last_modified = metadata.modified().ok().map(DateTime::<Utc>::from);

        let is_old = if is_dir {
            // For directories, consider them old if they are empty and haven't been modified recently
            // This is a simplification; a more robust check would involve recursive emptiness and child file ages
            if let Ok(mut entries) = fs::read_dir(path) {
                entries.next().is_none() && last_modified.map_or(false, |t| t < cutoff_time)
            } else {
                false
            }
        } else {
            // For files, check both access and modification times
            (last_accessed.map_or(false, |t| t < cutoff_time)) ||
            (last_modified.map_or(false, |t| t < cutoff_time))
        };

        if is_old {
            let category = if is_dir && file_size == 0 {
                "Vacant Memory Cavern".to_string()
            } else if file_size < 1024 * 10 { // < 10KB
                "Petrified Pixie Dust".to_string()
            } else if file_size < 1024 * 1024 * 100 { // < 100MB
                "Forgotten Digital Relic".to_string()
            } else { // >= 100MB
                "Slumbering Data Golem".to_string()
            };

            dust_bunnies.push(DustBunny {
                path: path.to_path_buf(),
                size: file_size,
                last_accessed,
                last_modified,
                category,
            });
        }
    }

    if dust_bunnies.is_empty() {
        println!("\nNo digital dust bunnies found! Your digital realm is sparkling clean. \u{2728}");
    } else {
        println!("\nFound {} digital dust bunnies:", dust_bunnies.len());
        for bunny in dust_bunnies {
            let size_str = if bunny.size > 0 {
                format!(" ({} bytes)", bunny.size)
            } else {
                "".to_string()
            };
            println!("  - [{}] {}{}", bunny.category, bunny.path.display(), size_str);
            if args.verbose {
                if let Some(accessed) = bunny.last_accessed {
                    println!("    Last Accessed: {}", accessed.to_rfc2822());
                }
                if let Some(modified) = bunny.last_modified {
                    println!("    Last Modified: {}", modified.to_rfc2822());
                }
            }
            if !args.dry_run {
                if bunny.path.is_dir() {
                    println!("    Suggestion: `rmdir \"{}\"` or `rm -r \"{}\"`", bunny.path.display(), bunny.path.display());
                } else {
                    println!("    Suggestion: `rm \"{}\"`", bunny.path.display());
                }
            }
        }
        if !args.dry_run {
            println!("\nConsider sweeping these away to free up some digital space!");
        } else {
            println!("\nRun without `--dry-run` to get cleanup suggestions.");
        }
    }

    Ok(())
}
