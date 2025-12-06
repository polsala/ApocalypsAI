use clap::Parser;
use std::path::{Path, PathBuf};
use std::fs;
use std::io::{self, Read, Write};
use flate2::write::GzEncoder;
use flate2::Compression;
use walkdir::WalkDir;
use chrono::{Duration, Utc, DateTime};
use std::time::SystemTime;

/// A high-performance CLI tool to identify and shred (compress and optionally delete) files
/// older than a specified duration, sending them to a 'temporal void' archive.
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// The path to the directory to scan for old files.
    #[clap(value_parser)]
    source_directory: PathBuf,

    /// The path where compressed archives will be stored.
    #[clap(value_parser)]
    archive_directory: PathBuf,

    /// Specifies the age threshold for files to be shredded.
    /// Format: <number><unit>, e.g., 7d (7 days), 30m (30 minutes), 1h (1 hour).
    /// Supported units: d (days), h (hours), m (minutes), s (seconds).
    #[clap(long, value_parser = parse_duration)]
    older_than: Duration,

    /// If present, the original files will be deleted after successful compression.
    #[clap(long)]
    delete_originals: bool,
}

fn parse_duration(s: &str) -> Result<Duration, String> {
    let (num_str, unit_str) = s.split_at(s.find(|c: char| c.is_alphabetic()).unwrap_or(s.len()));
    let num: i64 = num_str.parse().map_err(|_| format!("Invalid number in duration: {}", num_str))?;

    match unit_str {
        "s" => Ok(Duration::seconds(num)),
        "m" => Ok(Duration::minutes(num)),
        "h" => Ok(Duration::hours(num)),
        "d" => Ok(Duration::days(num)),
        _ => Err(format!("Invalid duration unit: {}. Supported units: s, m, h, d", unit_str)),
    }
}

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct FileToProcess {
    pub path: PathBuf,
    pub modified_time: SystemTime,
}

#[derive(Debug, PartialEq, Eq)]
pub enum ShredAction {
    Compress {
        source_path: PathBuf,
        dest_path: PathBuf,
        delete_original: bool,
    },
    // Add other actions if needed, e.g., Ignore
}

// # Mock rationale: This function is designed to be testable offline by taking a Vec<FileToProcess>
// # instead of directly scanning the filesystem. In main, we convert real filesystem entries
// # into this struct.
pub fn plan_shredding(
    files: Vec<FileToProcess>,
    older_than_duration: Duration,
    archive_dir: &Path,
    delete_originals: bool,
) -> Vec<ShredAction> {
    let now: DateTime<Utc> = Utc::now(); // # Mock rationale: In tests, `files` will have `modified_time` set relative to a fixed `now` for deterministic results.
    let cutoff_time = now - older_than_duration;

    let mut actions = Vec::new();
    for file in files {
        let file_datetime: DateTime<Utc> = file.modified_time.into();
        if file_datetime < cutoff_time {
            let file_name = file.path.file_name().unwrap_or_default().to_string_lossy();
            let compressed_file_name = format!("{}.gz", file_name);
            let dest_path = archive_dir.join(compressed_file_name);
            actions.push(ShredAction::Compress {
                source_path: file.path,
                dest_path,
                delete_original: delete_originals,
            });
        }
    }
    actions
}

fn execute_shred_action(action: ShredAction) -> io::Result<()> {
    match action {
        ShredAction::Compress { source_path, dest_path, delete_original } => {
            println!("Shredding: {} -> {}", source_path.display(), dest_path.display());

            // Ensure archive directory exists
            if let Some(parent) = dest_path.parent() {
                fs::create_dir_all(parent)?;
            }

            let mut input_file = fs::File::open(&source_path)?;
            let output_file = fs::File::create(&dest_path)?;
            let mut encoder = GzEncoder::new(output_file, Compression::default());

            io::copy(&mut input_file, &mut encoder)?;
            encoder.finish()?;

            if delete_original {
                fs::remove_file(&source_path)?;
                println!("Deleted original: {}", source_path.display());
            }
            Ok(())
        }
    }
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    if !args.source_directory.is_dir() {
        return Err(io::Error::new(io::ErrorKind::NotFound, "Source directory not found or is not a directory"));
    }

    fs::create_dir_all(&args.archive_directory)?;

    let mut files_to_process = Vec::new();
    for entry in WalkDir::new(&args.source_directory)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path().to_path_buf();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(&path) {
                if let Ok(modified_time) = metadata.modified() {
                    files_to_process.push(FileToProcess { path, modified_time });
                }
            }
        }
    }

    let actions = plan_shredding(
        files_to_process,
        args.older_than,
        &args.archive_directory,
        args.delete_originals,
    );

    for action in actions {
        if let Err(e) = execute_shred_action(action) {
            eprintln!("Error executing shred action: {}", e);
        }
    }

    Ok(())
}
