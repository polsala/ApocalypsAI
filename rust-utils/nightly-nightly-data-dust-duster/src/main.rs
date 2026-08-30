use clap::Parser;
use walkdir::WalkDir;
use sha2::{Sha256, Digest};
use std::{
    collections::HashMap,
    fs,
    path::{Path, PathBuf},
    io::{self, Read},
};

#[derive(Parser, Debug)]
#[command(author, version, about = "Identify and prioritize digital 'dust bunnies' (redundant, empty, or low-value files) in a given directory.", long_about = None)]
struct Args {
    /// The root directory to scan for dust bunnies.
    #[arg(short, long, default_value = ".")]
    path: PathBuf,

    /// Report empty files.
    #[arg(short, long)]
    empty: bool,

    /// Report duplicate files based on content hash.
    #[arg(short, long)]
    duplicates: bool,

    /// Do not traverse subdirectories.
    #[arg(short, long)]
    no_recursive: bool,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    if !args.path.exists() {
        eprintln!("Error: Path '{}' does not exist.", args.path.display());
        return Ok(());
    }
    if !args.path.is_dir() {
        eprintln!("Error: Path '{}' is not a directory.", args.path.display());
        return Ok(());
    }

    if !args.empty && !args.duplicates {
        eprintln!("Error: Please specify at least one detection option: --empty or --duplicates.");
        return Ok(());
    }

    println!("Scanning '{}' for digital dust bunnies...", args.path.display());

    let mut empty_files: Vec<PathBuf> = Vec::new();
    let mut file_hashes: HashMap<String, Vec<PathBuf>> = HashMap::new();

    let walker = if args.no_recursive {
        WalkDir::new(&args.path).max_depth(1)
    } else {
        WalkDir::new(&args.path)
    };

    for entry in walker.into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            // Check for empty files
            if args.empty {
                if let Ok(metadata) = fs::metadata(path) {
                    if metadata.len() == 0 {
                        empty_files.push(path.to_path_buf());
                    }
                }
            }

            // Check for duplicate files
            if args.duplicates {
                if let Ok(hash) = hash_file(path) {
                    file_hashes.entry(hash).or_default().push(path.to_path_buf());
                } else {
                    eprintln!("Warning: Could not hash file '{}'", path.display());
                }
            }
        }
    }

    if args.empty {
        println!("\n--- Empty Files (Digital Lint) ---");
        if empty_files.is_empty() {
            println!("No empty files found.");
        } else {
            for file in empty_files {
                println!("  - {}", file.display());
            }
        }
    }

    if args.duplicates {
        println!("\n--- Duplicate Files (Cloned Critters) ---");
        let mut found_duplicates = false;
        for (hash, paths) in file_hashes {
            if paths.len() > 1 {
                found_duplicates = true;
                println!("Hash: {}", hash);
                for path in paths {
                    println!("  - {}", path.display());
                }
                println!();
            }
        }
        if !found_duplicates {
            println!("No duplicate files found.");
        }
    }

    println!("\nScan complete. May your digital space be ever clean!");
    Ok(())
}

fn hash_file(path: &Path) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 4096]; // Read in 4KB chunks

    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }

    Ok(hex::encode(hasher.finalize()))
}
