use clap::Parser;
use std::collections::{HashMap, HashSet};
use std::fs;
use std::io::{self, Read};
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use walkdir::WalkDir;
use sha2::{Sha256, Digest};

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance CLI tool to identify and clean up old, unused, or duplicate files across specified directories, treating them as 'temporal detritus'.", long_about = None)]
struct Args {
    /// The root directory to scan for temporal detritus
    #[arg(short, long)]
    path: PathBuf,

    /// Identify files not accessed or modified in the last N days
    #[arg(short, long)]
    age: Option<u64>,

    /// Identify duplicate files by content hash
    #[arg(short, long)]
    duplicates: bool,

    /// Minimum file size (in bytes) to consider for age/duplicate checks
    #[arg(short = 's', long, default_value_t = 1)]
    min_size: u64,

    /// Enable verbose output
    #[arg(short, long)]
    verbose: bool,

    /// Actually delete the identified files (requires confirmation)
    #[arg(long)]
    delete: bool,

    /// Perform a dry run, showing what would be deleted without actual deletion (default)
    #[arg(long, default_value_t = true, action = clap::ArgAction::SetFalse, conflicts_with = "delete")]
    dry_run: bool,
}

fn get_file_hash(path: &Path) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 1024];

    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }
    Ok(format!("{:x}", hasher.finalize()))
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    if !args.path.is_dir() {
        eprintln!("Error: Provided path is not a directory: {}", args.path.display());
        return Ok(());
    }

    let now = SystemTime::now();
    let mut files_to_delete: HashSet<PathBuf> = HashSet::new();
    let mut duplicate_groups: HashMap<String, Vec<PathBuf>> = HashMap::new();

    println!("\nScanning '{}' for temporal detritus...\n", args.path.display());

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            let metadata = match fs::metadata(path) {
                Ok(m) => m,
                Err(e) => {
                    if args.verbose {
                        eprintln!("Warning: Could not get metadata for {}: {}", path.display(), e);
                    }
                    continue;
                }
            };

            if metadata.len() < args.min_size {
                if args.verbose {
                    println!("Skipping small file: {} ({} bytes)", path.display(), metadata.len());
                }
                continue;
            }

            // Check for age
            if let Some(days) = args.age {
                let cutoff = now - Duration::from_secs(days * 24 * 60 * 60);
                let modified_time = metadata.modified().unwrap_or(SystemTime::UNIX_EPOCH);
                let accessed_time = metadata.accessed().unwrap_or(SystemTime::UNIX_EPOCH);

                if modified_time < cutoff || accessed_time < cutoff {
                    println!("  [OLD] {}\n        (Modified: {:?}, Accessed: {:?})", path.display(), modified_time, accessed_time);
                    files_to_delete.insert(path.to_path_buf());
                }
            }

            // Check for duplicates
            if args.duplicates {
                match get_file_hash(path) {
                    Ok(hash) => {
                        duplicate_groups.entry(hash).or_default().push(path.to_path_buf());
                    },
                    Err(e) => {
                        if args.verbose {
                            eprintln!("Warning: Could not hash file {}: {}", path.display(), e);
                        }
                    }
                }
            }
        }
    }

    // Process duplicates
    if args.duplicates {
        println!("\n--- Duplicate Temporal Echoes ---");
        let mut found_duplicates = false;
        for (hash, paths) in duplicate_groups {
            if paths.len() > 1 {
                found_duplicates = true;
                println!("  Hash: {}", hash);
                for (i, p) in paths.iter().enumerate() {
                    println!("    - {}", p.display());
                    if i > 0 { // Keep the first instance, mark others for deletion
                        files_to_delete.insert(p.clone());
                    }
                }
                println!();
            }
        }
        if !found_duplicates {
            println!("  No duplicate temporal echoes detected.");
        }
    }

    if files_to_delete.is_empty() {
        println!("\nNo temporal detritus found matching criteria. Your digital realm is pristine.");
        return Ok(());
    }

    println!("\n--- Summary of Temporal Detritus ---");
    for file in &files_to_delete {
        println!("  - {}", file.display());
    }
    println!("Total files identified for scrubbing: {}", files_to_delete.len());

    if args.dry_run {
        println!("\nThis was a DRY RUN. No files were deleted. To proceed with deletion, use the '--delete' flag.");
    } else if args.delete {
        println!("\nWARNING: You are about to permanently delete {} files.", files_to_delete.len());
        print!("Are you sure you want to proceed? (yes/no): ");
        io::stdout().flush()?;

        let mut confirmation = String::new();
        io::stdin().read_line(&mut confirmation)?;

        if confirmation.trim().to_lowercase() == "yes" {
            println!("Initiating Chrono-Scrub protocol...");
            let mut deleted_count = 0;
            for file in files_to_delete {
                match fs::remove_file(&file) {
                    Ok(_) => {
                        println!("  [SCRUBBED] {}", file.display());
                        deleted_count += 1;
                    },
                    Err(e) => {
                        eprintln!("  [ERROR] Failed to scrub {}: {}", file.display(), e);
                    }
                }
            }
            println!("\nChrono-Scrub complete. {} files purged from the timeline.", deleted_count);
        } else {
            println!("Chrono-Scrub aborted. Files remain untouched.");
        }
    }

    Ok(())
}
