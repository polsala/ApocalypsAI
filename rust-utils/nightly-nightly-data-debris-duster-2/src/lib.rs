use std::{collections::HashMap, path::PathBuf, io::{self, Read}};
use walkdir::WalkDir;
use sha2::{Sha256, Digest};

/// Calculates the SHA256 hash of a file.
pub fn calculate_hash(path: &PathBuf) -> io::Result<String> {
    let mut file = std::fs::File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 1024]; // Read in chunks
    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }
    Ok(format!("{:x}", hasher.finalize()))
}

/// Scans a directory for duplicate files based on their SHA256 hash.
/// Returns a HashMap where keys are hashes and values are vectors of paths
/// that share that hash. Only includes hashes with more than one path (duplicates).
pub fn find_duplicate_files(target_path: &PathBuf) -> io::Result<HashMap<String, Vec<PathBuf>>> {
    if !target_path.is_dir() {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, format!("Provided path '{}' is not a directory.", target_path.display())));
    }

    let mut file_hashes: HashMap<String, Vec<PathBuf>> = HashMap::new();

    for entry in WalkDir::new(target_path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path().to_path_buf();
        if path.is_file() {
            match calculate_hash(&path) {
                Ok(hash) => {
                    file_hashes.entry(hash).or_default().push(path);
                }
                Err(e) => {
                    eprintln!("Warning: Could not hash file '{}': {}", path.display(), e);
                }
            }
        }
    }

    // Filter out unique files, keeping only duplicates
    let duplicates: HashMap<String, Vec<PathBuf>> = file_hashes
        .into_iter()
        .filter(|(_, paths)| paths.len() > 1)
        .collect();

    Ok(duplicates)
}
