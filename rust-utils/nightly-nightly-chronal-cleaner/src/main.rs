use clap::Parser;
use chrono::{Duration, Utc, DateTime};
use walkdir::WalkDir;
use std::fs;
use std::path::PathBuf;
use std::io::{self, Write};

#[derive(Parser, Debug)]
#[command(author, version, about = "Detects and purges 'temporal echoes' (stale or unaccessed files) from your filesystem.", long_about = None)]
struct Args {
    /// Path to the directory to scan
    #[arg(short, long)]
    path: PathBuf,

    /// Files modified or created more than N days ago
    #[arg(long)]
    older_than: Option<u64>,

    /// Files not accessed in N days
    #[arg(long)]
    not_accessed_in: Option<u64>,

    /// Perform a dry run, only report files, do not delete
    #[arg(short, long, default_value_t = true)]
    dry_run: bool,

    /// Actually delete the detected files. Requires --older-than or --not-accessed-in.
    #[arg(short, long, default_value_t = false)]
    delete: bool,

    /// Show more detailed output
    #[arg(short, long)]
    verbose: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    env_logger::init(); // Initialize logger

    let args = Args::parse();

    if args.delete && args.dry_run {
        eprintln!("Error: Cannot use --delete with --dry-run. Please choose one.");
        std::process::exit(1);
    }

    if args.delete && args.older_than.is_none() && args.not_accessed_in.is_none() {
        eprintln!("Error: --delete requires either --older-than or --not-accessed-in to be specified.");
        std::process::exit(1);
    }

    let now = Utc::now();
    let mut files_to_process = Vec::new();

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                let mut should_process = false;

                if let Some(days) = args.older_than {
                    let threshold = now - Duration::days(days as i64);
                    if let Ok(modified_time) = metadata.modified() {
                        let modified_dt: DateTime<Utc> = modified_time.into();
                        if modified_dt < threshold {
                            should_process = true;
                        }
                    }
                    if let Ok(created_time) = metadata.created() {
                        let created_dt: DateTime<Utc> = created_time.into();
                        if created_dt < threshold {
                            should_process = true;
                        }
                    }
                }

                if let Some(days) = args.not_accessed_in {
                    let threshold = now - Duration::days(days as i64);
                    if let Ok(accessed_time) = metadata.accessed() {
                        let accessed_dt: DateTime<Utc> = accessed_time.into();
                        if accessed_dt < threshold {
                            should_process = true;
                        }
                    }
                }

                if should_process {
                    files_to_process.push(path.to_path_buf());
                }
            } else if args.verbose {
                eprintln!("Warning: Could not get metadata for {:?}", path);
            }
        }
    }

    if files_to_process.is_empty() {
        println!("No temporal echoes detected in '{}'. Your filesystem is stable.", args.path.display());
        return Ok(());
    }

    println!("Temporal echoes detected ({} files):", files_to_process.len());
    for file_path in &files_to_process {
        println!("  - {}", file_path.display());
    }

    if args.dry_run {
        println!("\nThis was a dry run. No files were deleted.");
        println!("To purge these echoes, run again with --delete (and without --dry-run).");
    } else if args.delete {
        print!("\nAre you sure you want to purge these {} temporal echoes? (y/N): ", files_to_process.len());
        io::stdout().flush()?;
        let mut confirmation = String::new();
        io::stdin().read_line(&mut confirmation)?;
        if confirmation.trim().to_lowercase() == "y" {
            let mut deleted_count = 0;
            for file_path in files_to_process {
                match fs::remove_file(&file_path) {
                    Ok(_) => {
                        if args.verbose {
                            println!("Purged: {}", file_path.display());
                        }
                        deleted_count += 1;
                    },
                    Err(e) => eprintln!("Failed to purge {}: {}", file_path.display(), e),
                }
            }
            println!("\nSuccessfully purged {} temporal echoes.", deleted_count);
        } else {
            println!("\nPurge aborted. Temporal echoes remain.");
        }
    }

    Ok(())
}
