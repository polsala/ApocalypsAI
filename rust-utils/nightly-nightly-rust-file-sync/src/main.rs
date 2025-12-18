use std::fs;
use std::io::{self, Read, Write};
use std::path::{Path, PathBuf};
use std::env;
use std::process;
use std::collections::HashMap;

// For checksum verification
use sha2::{Sha256, Digest};

fn calculate_sha256<P: AsRef<Path>>(file_path: P) -> io::Result<String> {
    let mut hasher = Sha256::new();
    let mut file = fs::File::open(file_path)?;
    let mut buffer = [0u8; 1024]; // Read in chunks

    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }

    Ok(format!("{:x}", hasher.finalize()))
}

fn sync_files(source_dir: &Path, dest_dir: &Path, verify_checksum: bool) -> io::Result<()>
{
    // Ensure destination directory exists
    fs::create_dir_all(dest_dir)?;

    let mut source_files = HashMap::new();
    if verify_checksum {
        for entry in fs::read_dir(source_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_file() {
                if let Some(filename) = path.file_name().and_then(|n| n.to_str()) {
                    match calculate_sha256(&path) {
                        Ok(checksum) => {
                            source_files.insert(filename.to_string(), (path, checksum));
                        },
                        Err(e) => {
                            eprintln!("Warning: Could not calculate checksum for {:?}: {}", path, e);
                        }
                    }
                }
            }
        }
    } else {
        for entry in fs::read_dir(source_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_file() {
                if let Some(filename) = path.file_name().and_then(|n| n.to_str()) {
                    source_files.insert(filename.to_string(), (path, String::new())); // Checksum not used
                }
            }
        }
    }

    let mut dest_files = HashMap::new();
    if verify_checksum {
        for entry in fs::read_dir(dest_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_file() {
                if let Some(filename) = path.file_name().and_then(|n| n.to_str()) {
                    match calculate_sha256(&path) {
                        Ok(checksum) => {
                            dest_files.insert(filename.to_string(), (path, checksum));
                        },
                        Err(e) => {
                            eprintln!("Warning: Could not calculate checksum for {:?}: {}", path, e);
                        }
                    }
                }
            }
        }
    } else {
        for entry in fs::read_dir(dest_dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_file() {
                if let Some(filename) = path.file_name().and_then(|n| n.to_str()) {
                    dest_files.insert(filename.to_string(), (path, String::new())); // Checksum not used
                }
            }
        }
    }

    // Copy new or modified files
    for (filename, (source_path, source_checksum)) in source_files.iter() {
        let dest_path = dest_dir.join(filename);

        match dest_files.get(filename) {
            Some((_, dest_checksum)) => {
                if verify_checksum && source_checksum != dest_checksum {
                    println!("Updating modified file: {}", filename);
                    fs::copy(source_path, &dest_path)?;
                } else if !verify_checksum {
                    // If not verifying checksum, always copy if file exists to ensure latest version
                    println!("Updating file (no checksum): {}", filename);
                    fs::copy(source_path, &dest_path)?;
                }
            },
            None => {
                println!("Copying new file: {}", filename);
                fs::copy(source_path, &dest_path)?;
            }
        }
    }

    // Optionally remove files that are no longer in the source
    // For this utility, we'll keep it simple and only add/update.
    // A more advanced version could implement deletion.

    Ok(())
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 3 || args.len() > 4 {
        eprintln!("Usage: nightly-rust-file-sync <source_dir> <destination_dir> [--verify-checksum]");
        process::exit(1);
    }

    let source_dir = PathBuf::from(&args[1]);
    let dest_dir = PathBuf::from(&args[2]);
    let verify_checksum = args.len() == 4 && args[3] == "--verify-checksum";

    if !source_dir.is_dir() {
        eprintln!("Error: Source directory '{}' does not exist or is not a directory.", source_dir.display());
        process::exit(1);
    }

    match sync_files(&source_dir, &dest_dir, verify_checksum) {
        Ok(_) => println!("File synchronization complete."),
        Err(e) => {
            eprintln!("Error during synchronization: {}", e);
            process::exit(1);
        }
    }
}
