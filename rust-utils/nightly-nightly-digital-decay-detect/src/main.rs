use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[command(author, version, about = "Detects and reports files older than a specified duration.", long_about = None)]
struct Args {
    /// The directory to scan for old files.
    #[arg(index = 1)]
    path: PathBuf,

    /// The minimum age a file must be (e.g., 30d, 1w, 24h, 60m, 30s).
    #[arg(short, long, value_parser = parse_duration_arg)]
    age: Duration,
}

/// Parses a duration string (e.g., "30d", "1w", "24h", "60m", "30s") into a `std::time::Duration`.
pub fn parse_duration_arg(s: &str) -> Result<Duration, String> {
    let s = s.trim();
    if s.is_empty() {
        return Err("Duration string cannot be empty.".to_string());
    }

    let (num_str, unit) = s.split_at(s.len() - 1);
    let num: u64 = num_str.parse().map_err(|_| format!("Invalid number in duration: {}", num_str))?;

    match unit {
        "s" => Ok(Duration::from_secs(num)),
        "m" => Ok(Duration::from_secs(num * 60)),
        "h" => Ok(Duration::from_secs(num * 3600)),
        "d" => Ok(Duration::from_secs(num * 3600 * 24)),
        "w" => Ok(Duration::from_secs(num * 3600 * 24 * 7)),
        _ => Err(format!("Invalid duration unit: {}. Expected s, m, h, d, or w.", unit)),
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let scan_path = &args.path;
    let min_age = args.age;

    if !scan_path.exists() {
        eprintln!("Error: Path does not exist: {}", scan_path.display());
        std::process::exit(1);
    }
    if !scan_path.is_dir() {
        eprintln!("Error: Path is not a directory: {}", scan_path.display());
        std::process::exit(1);
    }

    println!("\n🔍 Initiating Digital Decay Detection in '{}' for files older than {:?}...\n", scan_path.display(), min_age);

    let mut found_decaying_files = 0;
    let current_time = SystemTime::now();
    let cutoff_time = current_time - min_age;

    for entry in WalkDir::new(scan_path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path();
            match fs::metadata(path) {
                Ok(metadata) => {
                    if let Ok(modified_time) = metadata.modified() {
                        if modified_time < cutoff_time {
                            println!("  ⏳ Found ancient data: {}", path.display());
                            found_decaying_files += 1;
                        }
                    }
                }
                Err(e) => {
                    eprintln!("  ⚠️ Could not read metadata for {}: {}", path.display(), e);
                }
            }
        }
    }

    if found_decaying_files == 0 {
        println!("\n✨ All clear! No digital dust bunnies or temporal echoes found. Your files are spry!\n");
    } else {
        println!("\n🧹 Digital decay detected! Found {} ancient files whispering tales of old. Consider a digital spring cleaning!\n", found_decaying_files);
    }

    Ok(())
}
