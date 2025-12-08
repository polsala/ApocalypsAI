use clap::Parser;
use std::collections::{HashMap, HashSet};
use std::fs;
use std::io::{self, Read};
use std::path::{Path, PathBuf};
use walkdir::WalkDir;
use sha2::{Sha256, Digest};

/// A high-performance Rust CLI tool to detect temporal data drifts by identifying
/// exact duplicate files and files with identical names but differing content.
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// The path to the directory to scan
    #[clap(name = "PATH")]
    path: PathBuf,
}

#[derive(Debug, PartialEq, Eq, Hash)]
struct FileInfo {
    path: PathBuf,
    hash: Vec<u8>,
}

fn calculate_hash(path: &Path) -> io::Result<Vec<u8>> {
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
    Ok(hasher.finalize().to_vec())
}

fn main() -> io::Result<()> {
    let args = Args::parse();
    let root_path = args.path;

    if !root_path.is_dir() {
        eprintln!("Error: Provided path is not a directory: {:?}", root_path);
        std::process::exit(1);
    }

    println!("Temporal Drift Scrutinizer Report:\n");

    let mut exact_duplicates: HashMap<Vec<u8>, Vec<PathBuf>> = HashMap::new();
    let mut files_by_name: HashMap<String, Vec<FileInfo>> = HashMap::new();

    for entry in WalkDir::new(&root_path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            match calculate_hash(path) {
                Ok(hash) => {
                    // Track exact duplicates
                    exact_duplicates.entry(hash.clone()).or_default().push(path.to_path_buf());

                    // Track files by name for same-name-different-content detection
                    if let Some(file_name) = path.file_name().and_then(|s| s.to_str()) {
                        files_by_name.entry(file_name.to_string()).or_default().push(FileInfo {
                            path: path.to_path_buf(),
                            hash,
                        });
                    }
                }
                Err(e) => eprintln!("Warning: Could not hash file {:?}: {}", path, e),
            }
        }
    }

    // --- Report Exact Duplicates ---
    let mut found_exact_duplicates = false;
    println!("--- Exact Duplicates Detected ---");
    for (hash, paths) in exact_duplicates {
        if paths.len() > 1 {
            found_exact_duplicates = true;
            println!("Hash: {}", hex::encode(&hash));
            for p in paths {
                println!("  - {}", p.display());
            }
            println!();
        }
    }
    if !found_exact_duplicates {
        println!("No exact duplicates found.\n");
    }

    // --- Report Same Name, Different Content ---
    let mut found_same_name_drift = false;
    println!("--- Same Name, Different Content Detected ---");
    for (file_name, file_infos) in files_by_name {
        if file_infos.len() > 1 {
            let mut unique_hashes = HashSet::new();
            for info in &file_infos {
                unique_hashes.insert(info.hash.clone());
            }

            if unique_hashes.len() > 1 { // More than one unique hash for the same filename
                found_same_name_drift = true;
                println!("Filename: {}", file_name);
                for info in file_infos {
                    println!("  - {} (Hash: {})", info.path.display(), hex::encode(&info.hash));
                }
                println!();
            }
        }
    }
    if !found_same_name_drift {
        println!("No same-name, different-content drifts found.\n");
    }

    Ok(())
}
