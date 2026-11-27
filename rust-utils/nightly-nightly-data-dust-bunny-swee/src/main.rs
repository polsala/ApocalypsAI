use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the directory to sweep for data dust bunnies
    #[clap(value_parser)]
    path: PathBuf,

    /// Show verbose output for each file found
    #[clap(short, long)]
    verbose: bool,
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
enum FileCategory {
    Fresh, // < 30 days
    Stale, // 30 days - 90 days
    Ancient, // 90 days - 1 year
    Fossilized, // > 1 year
    Unknown, // Error getting metadata
}

impl FileCategory {
    fn from_duration(duration: Duration) -> Self {
        if duration < Duration::days(30) {
            FileCategory::Fresh
        } else if duration < Duration::days(90) {
            FileCategory::Stale
        } else if duration < Duration::days(365) {
            FileCategory::Ancient
        } else {
            FileCategory::Fossilized
        }
    }

    fn display_name(&self) -> &str {
        match self {
            FileCategory::Fresh => "Fresh (accessed < 30 days ago)",
            FileCategory::Stale => "Stale (accessed 30-90 days ago)",
            FileCategory::Ancient => "Ancient (accessed 90 days-1 year ago)",
            FileCategory::Fossilized => "Fossilized (accessed > 1 year ago)",
            FileCategory::Unknown => "Unknown (metadata error)",
        }
    }
}

#[derive(Debug)]
struct FileReport {
    path: PathBuf,
    category: FileCategory,
    last_accessed: Option<DateTime<Utc>>,
}

fn sweep_directory(path: &PathBuf, verbose: bool) -> HashMap<FileCategory, Vec<FileReport>> {
    let mut categories: HashMap<FileCategory, Vec<FileReport>> = HashMap::new();
    let now = Utc::now();

    for entry in WalkDir::new(path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path().to_path_buf();
            let mut category = FileCategory::Unknown;
            let mut last_accessed_dt: Option<DateTime<Utc>> = None;

            if let Ok(metadata) = fs::metadata(&path) {
                if let Ok(accessed_time) = metadata.accessed() {
                    // Convert SystemTime to DateTime<Utc>
                    let accessed_dt: DateTime<Utc> = accessed_time.into();
                    let duration = now.signed_duration_since(accessed_dt);
                    category = FileCategory::from_duration(duration);
                    last_accessed_dt = Some(accessed_dt);
                }
            }

            if verbose {
                println!(
                    "  - {}: {} ({})",
                    path.display(),
                    category.display_name(),
                    last_accessed_dt.map_or("N/A".to_string(), |dt| dt.format("%Y-%m-%d").to_string())
                );
            }

            categories.entry(category).or_default().push(FileReport {
                path,
                category,
                last_accessed: last_accessed_dt,
            });
        }
    }
    categories
}

fn main() {
    let args = Args::parse();

    if !args.path.exists() {
        eprintln!("Error: Path '{}' does not exist.", args.path.display());
        std::process::exit(1);
    }
    if !args.path.is_dir() {
        eprintln!("Error: Path '{}' is not a directory.", args.path.display());
        std::process::exit(1);
    }

    println!("Sweeping for data dust bunnies in: {}", args.path.display());
    let results = sweep_directory(&args.path, args.verbose);

    println!("\n--- Data Dust Bunny Report ---");
    let mut sorted_categories: Vec<(&FileCategory, &Vec<FileReport>)> = results.iter().collect();
    sorted_categories.sort_by_key(|(cat, _)| match cat {
        FileCategory::Fresh => 0,
        FileCategory::Stale => 1,
        FileCategory::Ancient => 2,
        FileCategory::Fossilized => 3,
        FileCategory::Unknown => 4,
    });

    for (category, files) in sorted_categories {
        println!("{}: {} files", category.display_name(), files.len());
    }
    println!("------------------------------");
}
