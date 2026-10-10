use clap::Parser;
use walkdir::WalkDir;
use sha2::{Sha256, Digest};
use chrono::{Utc, Duration, DateTime};
use serde::{Serialize, Deserialize};
use std::fs;
use std::io::{self, Read};
use std::path::{Path, PathBuf};

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Directory to scan for relics
    #[clap(short, long, value_parser)]
    input_dir: String,

    /// Output file for the relic registry (JSON format)
    #[clap(short, long, value_parser, default_value = "relic_registry.json")]
    output_file: String,
}

#[derive(Serialize, Deserialize, Debug, PartialEq)]
enum DecayStatus {
    Pristine,
    Weathered,
    Decaying,
    Dust,
    Unknown, // For files with no valid modification time
}

impl DecayStatus {
    fn from_timestamp(timestamp: DateTime<Utc>) -> Self {
        let now = Utc::now();
        let age = now - timestamp;

        if age < Duration::days(365) { // Less than 1 year
            DecayStatus::Pristine
        } else if age < Duration::days(365 * 5) { // 1 to 5 years
            DecayStatus::Weathered
        } else if age < Duration::days(365 * 10) { // 5 to 10 years
            DecayStatus::Decaying
        } else { // More than 10 years
            DecayStatus::Dust
        }
    }
}

#[derive(Serialize, Deserialize, Debug)]
struct RelicEntry {
    id: String,
    path: PathBuf,
    filename: String,
    checksum_sha256: String,
    last_modified: Option<DateTime<Utc>>,
    decay_status: DecayStatus,
    size_bytes: u64,
}

fn calculate_sha256(path: &Path) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 1024];
    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }
    Ok(format!("{:x}", hasher.finalize()))
}

fn generate_relic_registry(input_dir: &Path) -> io::Result<Vec<RelicEntry>> {
    let mut registry = Vec::new();
    let mut relic_counter = 0;

    for entry in WalkDir::new(input_dir).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            relic_counter += 1;
            let filename = path.file_name().unwrap_or_default().to_string_lossy().into_owned();
            let checksum = calculate_sha256(path)?;
            let metadata = fs::metadata(path)?;
            let last_modified: Option<DateTime<Utc>> = metadata.modified().ok().map(Into::into);
            let decay_status = last_modified.map_or(DecayStatus::Unknown, DecayStatus::from_timestamp);
            let size_bytes = metadata.len();

            registry.push(RelicEntry {
                id: format!("RELIC-{}", relic_counter),
                path: path.to_path_buf(),
                filename,
                checksum_sha256: checksum,
                last_modified,
                decay_status,
                size_bytes,
            });
        }
    }
    Ok(registry)
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let input_path = PathBuf::from(&args.input_dir);
    if !input_path.exists() {
        eprintln!("Error: Input directory '{}' does not exist.", args.input_dir);
        std::process::exit(1);
    }
    if !input_path.is_dir() {
        eprintln!("Error: Input path '{}' is not a directory.", args.input_dir);
        std::process::exit(1);
    }

    println!("Scanning '{}' for relics...", args.input_dir);
    let registry = generate_relic_registry(&input_path)?;

    let output_json = serde_json::to_string_pretty(&registry)?;
    fs::write(&args.output_file, output_json)?;

    println!("Relic registry generated successfully to '{}'. Found {} relics.", args.output_file, registry.len());

    Ok(())
}
