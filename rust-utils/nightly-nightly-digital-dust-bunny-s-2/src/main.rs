use clap::Parser;
use walkdir::WalkDir;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use std::fs::Metadata;

/// A whimsical yet powerful command-line utility to sweep away digital dust bunnies.
/// It scans specified directories for files that are either very old or excessively large.
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// The root directory to start scanning from.
    #[clap(short, long, default_value = ".")]
    path: PathBuf,

    /// Files older than this many days will be considered dust bunnies.
    #[clap(short, long, default_value_t = 365)]
    age: u64,

    /// Files larger than this many megabytes will be considered dust bunnies.
    #[clap(short, long, default_value_t = 100)]
    size: u64,

    /// Show more detailed output during scanning.
    #[clap(short, long)]
    verbose: bool,
}

#[derive(Debug, PartialEq)]
struct DustBunny {
    path: PathBuf,
    size_bytes: u64,
    modified_time: SystemTime,
}

impl DustBunny {
    fn new(path: PathBuf, metadata: &Metadata) -> Option<Self> {
        let modified_time = metadata.modified().ok()?;
        Some(DustBunny {
            path,
            size_bytes: metadata.len(),
            modified_time,
        })
    }

    fn is_old(&self, age_threshold_days: u64) -> bool {
        if age_threshold_days == 0 { return false; } // 0 days means no age limit
        let now = SystemTime::now();
        if let Ok(elapsed) = now.duration_since(self.modified_time) {
            elapsed.as_secs() > age_threshold_days * 24 * 60 * 60
        } else {
            // File modified time is in the future, or other error. Treat as not old.
            false
        }
    }

    fn is_large(&self, size_threshold_mb: u64) -> bool {
        if size_threshold_mb == 0 { return false; } // 0 MB means no size limit
        self.size_bytes > size_threshold_mb * 1024 * 1024
    }

    fn report_line(&self) -> String {
        let size_mb = self.size_bytes as f64 / (1024.0 * 1024.0);
        let now = SystemTime::now();
        let age_str = if let Ok(elapsed) = now.duration_since(self.modified_time) {
            let days = elapsed.as_secs() / (24 * 60 * 60);
            format!("last modified {} days ago", days)
        } else {
            "modification time unknown/future".to_string()
        };
        format!("- {} ({:.2} MB, {})", self.path.display(), size_mb, age_str)
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if args.verbose {
        println!("Scanning directory: {}", args.path.display());
        println!("Looking for files older than {} days or larger than {} MB.", args.age, args.size);
    }

    let mut dust_bunnies: Vec<DustBunny> = Vec::new();

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = path.metadata() {
                if let Some(bunny) = DustBunny::new(path.to_path_buf(), &metadata) {
                    if bunny.is_old(args.age) || bunny.is_large(args.size) {
                        dust_bunnies.push(bunny);
                    }
                }
            }
        }
    }

    if dust_bunnies.is_empty() {
        println!("No digital dust bunnies found! Your filesystem is sparkling clean.");
    } else {
        println!("Found {} digital dust bunnies:", dust_bunnies.len());
        for bunny in dust_bunnies {
            println!("{}", bunny.report_line());
        }
    }

    Ok(())
}
