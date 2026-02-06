use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::SystemTime;
use chrono::{DateTime, Local};

#[derive(Parser, Debug)]
#[clap(author, version, about = "Sorts files into temporal directories based on modification timestamps.", long_about = None)]
struct Args {
    /// Source directory containing files to sort.
    #[clap(short, long, value_parser)]
    source: PathBuf,

    /// Destination directory where temporal vaults will be created.
    #[clap(short, long, value_parser)]
    destination: PathBuf,

    /// Copy files instead of moving them. If not set, files are moved.
    #[clap(short, long, action)]
    copy: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.source.is_dir() {
        eprintln!("Error: Source path is not a directory or does not exist: {}", args.source.display());
        std::process::exit(1);
    }

    // Call the public function for sorting
    sort_chrono_shards(&args.source, &args.destination, args.copy)?; 

    println!("Chrono-shards sorted successfully from '{}' to '{}'.", args.source.display(), args.destination.display());
    Ok(())
}

pub fn sort_chrono_shards(source_dir: &Path, dest_dir: &Path, copy_mode: bool) -> Result<(), Box<dyn std::error::Error>> {
    fs::create_dir_all(dest_dir)?;

    for entry in fs::read_dir(source_dir)? {
        let entry = entry?;
        let path = entry.path();

        if path.is_file() {
            let metadata = fs::metadata(&path)?;
            let modified_time: SystemTime = metadata.modified()?;

            // Convert SystemTime to DateTime<Local> for formatting
            let datetime: DateTime<Local> = modified_time.into();
            let year = datetime.format("%Y").to_string();
            let month = datetime.format("%m").to_string();
            let day = datetime.format("%d").to_string();

            let target_subdir = dest_dir.join(&year).join(&month).join(&day);
            fs::create_dir_all(&target_subdir)?;

            let original_file_name = path.file_name().ok_or("Could not get file name")?.to_string_lossy().into_owned();
            let mut target_file_path = target_subdir.join(&original_file_name);

            // Conflict resolution: if target file exists, append timestamp to filename
            if target_file_path.exists() {
                let stem = path.file_stem().map(|s| s.to_string_lossy().into_owned()).unwrap_or_default();
                let extension = path.extension().map(|s| format!(".{}", s.to_string_lossy())).unwrap_or_default();
                let timestamp_suffix = modified_time.duration_since(SystemTime::UNIX_EPOCH)?.as_secs();
                let new_file_name = format!("{}_{}{}", stem, timestamp_suffix, extension);
                target_file_path = target_subdir.join(&new_file_name);
                eprintln!("Warning: File '{}' already exists in target. Renaming to '{}'.", original_file_name, new_file_name);
            }

            if copy_mode {
                fs::copy(&path, &target_file_path)?;
                println!("Copied '{}' to '{}'.", path.display(), target_file_path.display());
            } else {
                fs::rename(&path, &target_file_path)?;
                println!("Moved '{}' to '{}'.", path.display(), target_file_path.display());
            }
        }
    }
    Ok(())
}
