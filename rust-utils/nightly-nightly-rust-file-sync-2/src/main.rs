use clap::Parser;
use std::fs;
use std::io::{self, Read, Write};
use std::path::{Path, PathBuf};
use std::process;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

/// A high-performance Rust CLI tool for synchronizing files between two directories.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Source directory to synchronize from.
    #[arg(short, long)]
    source: PathBuf,

    /// Destination directory to synchronize to.
    #[arg(short, long)]
    destination: PathBuf,

    /// Enable MD5 checksum verification for files.
    #[arg(short, long)]
    checksum: bool,

    /// Overwrite existing files in the destination directory.
    #[arg(short, long)]
    overwrite: bool,

    /// Perform a dry run, showing what would be synchronized without making changes.
    #[arg(short, long)]
    dry_run: bool,
}

fn calculate_md5<P: AsRef<Path>>(path: P) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = DefaultHasher::new();
    let mut buffer = [0u8; 4096];

    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.write(&buffer[..bytes_read]);
    }

    Ok(format!("{:x}", hasher.finish()))
}

fn sync_files(source: &Path, destination: &Path, checksum: bool, overwrite: bool, dry_run: bool) -> io::Result<()>
{
    if !source.is_dir() {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, "Source must be a directory."));
    }

    if !destination.exists() {
        if dry_run {
            println!("[DRY RUN] Creating directory: {:?}", destination);
        } else {
            fs::create_dir_all(destination)?;
            println!("Created directory: {:?}", destination);
        }
    } else if !destination.is_dir() {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, "Destination must be a directory."));
    }

    for entry in fs::read_dir(source)? {
        let entry = entry?;
        let src_path = entry.path();
        let file_name = src_path.file_name().ok_or_else(|| io::Error::new(io::ErrorKind::InvalidData, "Failed to get file name"))?;
        let dest_path = destination.join(file_name);

        if src_path.is_file() {
            let src_metadata = fs::metadata(&src_path)?;
            let src_modified = src_metadata.modified()?;

            let mut needs_copy = true;
            let mut src_checksum = None;

            if checksum {
                src_checksum = Some(calculate_md5(&src_path)?);
            }

            if dest_path.exists() {
                if overwrite {
                    if dry_run {
                        println!("[DRY RUN] Overwriting file: {:?} with {:?}", dest_path, src_path);
                    } else {
                        println!("Overwriting file: {:?} with {:?}", dest_path, src_path);
                        fs::copy(&src_path, &dest_path)?;
                    }
                    needs_copy = false; // Already handled by overwrite
                } else {
                    let dest_metadata = fs::metadata(&dest_path)?;
                    let dest_modified = dest_metadata.modified()?;

                    if src_modified > dest_modified {
                        if dry_run {
                            println!("[DRY RUN] Updating file: {:?} (newer source)", dest_path);
                        } else {
                            println!("Updating file: {:?} (newer source)", dest_path);
                            fs::copy(&src_path, &dest_path)?;
                        }
                        needs_copy = false; // Already handled by update
                    } else if checksum {
                        let dest_checksum = calculate_md5(&dest_path)?;
                        if src_checksum.as_ref().unwrap() != &dest_checksum {
                            if dry_run {
                                println!("[DRY RUN] Updating file: {:?} (checksum mismatch)", dest_path);
                            } else {
                                println!("Updating file: {:?} (checksum mismatch)", dest_path);
                                fs::copy(&src_path, &dest_path)?;
                            }
                            needs_copy = false; // Already handled by checksum mismatch
                        } else {
                            // File is up-to-date and checksums match
                            needs_copy = false;
                        }
                    } else {
                        // File exists, not overwriting, and modification times are the same
                        needs_copy = false;
                    }
                }
            }

            if needs_copy {
                if dry_run {
                    println!("[DRY RUN] Copying file: {:?} to {:?}", src_path, dest_path);
                } else {
                    println!("Copying file: {:?} to {:?}", src_path, dest_path);
                    fs::copy(&src_path, &dest_path)?;
                }
            }
        } else if src_path.is_dir() {
            // Recursively sync subdirectories
            sync_files(&src_path, &dest_path, checksum, overwrite, dry_run)?;
        }
    }

    Ok(())
}

fn main() {
    let args = Args::parse();

    if args.dry_run {
        println!("--- DRY RUN MODE ENABLED ---");
    }

    match sync_files(&args.source, &args.destination, args.checksum, args.overwrite, args.dry_run) {
        Ok(_) => {
            if !args.dry_run {
                println!("Synchronization complete.");
            }
        }
        Err(e) => {
            eprintln!("Error during synchronization: {}", e);
            process::exit(1);
        }
    }
}
