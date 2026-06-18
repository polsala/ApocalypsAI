use clap::{Arg, Command};
use std::fs;
use std::io::{self, Write};
use std::path::{Path, PathBuf};

fn main() -> io::Result<()> {
    let matches = Command::new("nightly-rust-file-sync")
        .version("1.0")
        .author("ApocalypsAI Integrator")
        .about("Synchronizes files between two directories.")
        .arg(Arg::new("source")
            .help("The source directory")
            .required(true)
            .index(1))
        .arg(Arg::new("destination")
            .help("The destination directory")
            .required(true)
            .index(2))
        .arg(Arg::new("dry_run")
            .short('d')
            .long("dry-run")
            .help("Perform a trial run with no changes made"))
        .arg(Arg::new("verbose")
            .short('v')
            .long("verbose")
            .help("Enable verbose output"))
        .get_matches();

    let source_path = PathBuf::from(matches.get_one::<String>("source").unwrap());
    let dest_path = PathBuf::from(matches.get_one::<String>("destination").unwrap());
    let dry_run = matches.get_flag("dry_run");
    let verbose = matches.get_flag("verbose");

    if verbose {
        println!("Starting file synchronization from {:?} to {:?}", source_path, dest_path);
        if dry_run {
            println!("Running in DRY-RUN mode. No files will be modified.");
        }
    }

    sync_directories(&source_path, &dest_path, dry_run, verbose)?;

    if verbose {
        println!("File synchronization complete.");
    }

    Ok(())
}

fn sync_directories(source: &Path, destination: &Path, dry_run: bool, verbose: bool) -> io::Result<()> {
    if !source.is_dir() {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, "Source path is not a directory."));
    }

    if !destination.exists() {
        if verbose || !dry_run {
            println!("Creating destination directory: {:?}", destination);
        }
        if !dry_run {
            fs::create_dir_all(destination)?;
        }
    } else if !destination.is_dir() {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, "Destination path exists but is not a directory."));
    }

    for entry in fs::read_dir(source)? {
        let entry = entry?;
        let src_file_path = entry.path();
        let file_name = src_file_path.file_name().ok_or_else(|| io::Error::new(io::ErrorKind::InvalidData, "Failed to get file name"))?;
        let dest_file_path = destination.join(file_name);

        if src_file_path.is_dir() {
            // Recursively sync subdirectories
            sync_directories(&src_file_path, &dest_file_path, dry_run, verbose)?;
        } else {
            // Sync files
            let src_metadata = fs::metadata(&src_file_path)?;
            let mut needs_copy = true;

            if dest_file_path.exists() {
                let dest_metadata = fs::metadata(&dest_file_path)?;
                if src_metadata.len() == dest_metadata.len() && src_metadata.modified()? == dest_metadata.modified()? {
                    needs_copy = false;
                    if verbose {
                        println!("Skipping {:?}: File is up-to-date.", dest_file_path);
                    }
                }
            }

            if needs_copy {
                if verbose {
                    println!("Copying {:?} to {:?}", src_file_path, dest_file_path);
                }
                if !dry_run {
                    fs::copy(&src_file_path, &dest_file_path)?;
                }
            }
        }
    }

    Ok(())
}
