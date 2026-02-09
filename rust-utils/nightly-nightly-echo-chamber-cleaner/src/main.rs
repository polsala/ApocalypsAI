use clap::{Parser, ValueEnum};
use std::collections::HashMap;
use std::fs;
use std::io::{self, Read};
use std::path::{Path, PathBuf};
use sha2::{Sha256, Digest};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[command(author, version, about = "Nightly Echo-Chamber Cleaner: Harmonizes duplicate files.", long_about = None)]
struct Args {
    /// The path to the directory to scan for duplicate files.
    directory: PathBuf,

    /// Specify the action to take on duplicates.
    #[arg(short = 'a', long, default_value_t = Action::Delete, value_enum)]
    action: Action,

    /// Perform a dry run, printing what actions would be taken without modifying the file system.
    #[arg(short = 'd', long)]
    dry_run: bool,

    /// Enable verbose output.
    #[arg(short = 'v', long)]
    verbose: bool,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum, Debug)]
enum Action {
    /// Delete all but one instance of each duplicate group.
    Delete,
    /// Replace all but one instance of each duplicate group with hard links to the original file.
    Link,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    if !args.directory.is_dir() {
        eprintln!("Error: Provided path is not a directory: {}", args.directory.display());
        return Ok(());
    }

    if args.verbose {
        println!("Scanning directory: {} for echoes...", args.directory.display());
    }

    let duplicates = find_duplicates(&args.directory, args.verbose)?;

    if duplicates.is_empty() {
        println!("No echoes detected. Your directory is already in harmony!");
        return Ok(());
    }

    println!("\nFound {} groups of echoes.", duplicates.len());

    harmonize_duplicates(duplicates, args.action, args.dry_run, args.verbose)?;

    if args.dry_run {
        println!("\nDry run complete. No files were modified.");
    } else {
        println!("\nHarmonization complete. Echoes silenced.");
    }

    Ok(())
}

/// Finds duplicate files in the given directory based on SHA256 hash.
fn find_duplicates(dir: &Path, verbose: bool) -> io::Result<HashMap<Vec<u8>, Vec<PathBuf>>> {
    let mut file_hashes: HashMap<Vec<u8>, Vec<PathBuf>> = HashMap::new();
    let mut total_files = 0;

    for entry in WalkDir::new(dir).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            total_files += 1;
            let path = entry.path().to_path_buf();
            if verbose {
                println!("  Hashing: {}", path.display());
            }
            match calculate_sha256(&path) {
                Ok(hash) => {
                    file_hashes.entry(hash).or_default().push(path);
                }
                Err(e) => {
                    eprintln!("Warning: Could not hash file {}: {}", path.display(), e);
                }
            }
        }
    }

    if verbose {
        println!("Scanned {} files.", total_files);
    }

    // Filter out unique files, keeping only groups with more than one entry (duplicates)
    let duplicates = file_hashes.into_iter()
        .filter(|(_, paths)| paths.len() > 1)
        .collect();

    Ok(duplicates)
}

/// Calculates the SHA256 hash of a file.
fn calculate_sha256(path: &Path) -> io::Result<Vec<u8>> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 4096];

    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }

    Ok(hasher.finalize().to_vec())
}

/// Harmonizes duplicate files based on the specified action.
fn harmonize_duplicates(
    duplicates: HashMap<Vec<u8>, Vec<PathBuf>>,
    action: Action,
    dry_run: bool,
    verbose: bool,
) -> io::Result<()> {
    for (hash, paths) in duplicates {
        let original_path = &paths[0];
        println!("\n  Echo group (hash: {}...):
    Original: {}", hex::encode(&hash[0..4]), original_path.display());

        for i in 1..paths.len() {
            let duplicate_path = &paths[i];
            let action_desc = match action {
                Action::Delete => "Deleting",
                Action::Link => "Replacing with hard link",
            };

            if dry_run {
                println!("    [DRY RUN] {} duplicate: {}", action_desc, duplicate_path.display());
            } else {
                match action {
                    Action::Delete => {
                        if verbose {
                            println!("    {} duplicate: {}", action_desc, duplicate_path.display());
                        }
                        fs::remove_file(duplicate_path)?;
                    }
                    Action::Link => {
                        if verbose {
                            println!("    {} duplicate: {}", action_desc, duplicate_path.display());
                        }
                        // Remove the duplicate first before creating a hard link
                        fs::remove_file(duplicate_path)?;
                        fs::hard_link(original_path, duplicate_path)?;
                    }
                }
            }
        }
    }
    Ok(())
}
