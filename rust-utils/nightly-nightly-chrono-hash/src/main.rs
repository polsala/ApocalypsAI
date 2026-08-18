use clap::Parser;
use sha2::{Digest, Sha256};
use std::fs;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

/// Calculates a content hash combined with a temporal signature for files.
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the file to chrono-hash
    #[clap(value_parser)]
    file_path: PathBuf,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let path = &args.file_path;

    if !path.exists() {
        eprintln!("Error: File not found: {}", path.display());
        std::process::exit(1);
    }
    if !path.is_file() {
        eprintln!("Error: Path is not a file: {}", path.display());
        std::process::exit(1);
    }

    // Read file content
    let content = fs::read(path)?;

    // Calculate SHA256 hash of content
    let mut content_hasher = Sha256::new();
    content_hasher.update(&content);
    let content_hash_bytes = content_hasher.finalize();

    // Get file modification time
    let metadata = fs::metadata(path)?;
    let modified_time = metadata.modified()?;
    let duration_since_epoch = modified_time.duration_since(UNIX_EPOCH)?;
    let timestamp_nanos = duration_since_epoch.as_nanos();

    // Combine content hash and timestamp into a new hash
    let mut chrono_hasher = Sha256::new();
    chrono_hasher.update(&content_hash_bytes);
    chrono_hasher.update(&timestamp_nanos.to_be_bytes()); // Use big-endian bytes for consistency

    let chrono_hash = chrono_hasher.finalize();

    println!("{:x}", chrono_hash);

    Ok(())
}
