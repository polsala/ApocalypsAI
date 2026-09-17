use std::collections::HashMap;
use std::fs::File;
use std::io::{self, Read};
use std::path::{Path, PathBuf};

use clap::Parser;
use walkdir::WalkDir;
use sha2::{Sha256, Digest};

#[derive(Parser, Debug)]
#[clap(
    author = "ApocalypsAI Nightly Integrator",
    version = "1.0",
    about = "Detects 'temporal echoes' (duplicate files) by content hash."
)]
struct Args {
    /// One or more paths to directories to scan for temporal echoes.
    #[clap(required = true)]
    paths: Vec<PathBuf>,
}

/// Calculates the SHA256 hash of a file.
fn hash_file<P: AsRef<Path>>(path: P) -> io::Result<Vec<u8>> {
    let mut file = File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 1024];

    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }
    Ok(hasher.finalize().to_vec())
}

/// Finds duplicate files in the given paths.
fn find_temporal_echoes(paths: &[PathBuf]) -> HashMap<Vec<u8>, Vec<PathBuf>> {
    let mut file_hashes: HashMap<Vec<u8>, Vec<PathBuf>> = HashMap::new();

    for root_path in paths {
        for entry in WalkDir::new(root_path).into_iter().filter_map(|e| e.ok()) {
            let path = entry.path();
            if path.is_file() {
                match hash_file(path) {
                    Ok(hash) => {
                        file_hashes.entry(hash).or_default().push(path.to_path_buf());
                    }
                    Err(e) => {
                        eprintln!("Warning: Could not hash file {:?}: {}", path, e);
                    }
                }
            }
        }
    }

    // Filter out unique files (those with only one path entry)
    file_hashes.into_iter().filter(|(_, paths)| paths.len() > 1).collect()
}

fn main() {
    let args = Args::parse();

    println!("Temporal Echoes Detected! Initiating Resonance Scan...");

    let echoes = find_temporal_echoes(&args.paths);

    if echoes.is_empty() {
        println!("\nNo temporal echoes detected. All clear!");
    } else {
        let mut group_count = 1;
        for (hash, paths) in echoes {
            println!("\n--- Echo Group {} ---", group_count);
            println!("Resonance Field (SHA256): {}", hex::encode(hash));
            for path in paths {
                println!("  - {}", path.display());
            }
            group_count += 1;
        }
        println!("\nResonance scan complete. Temporal echoes identified.");
    }
}
