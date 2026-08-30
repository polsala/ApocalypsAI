use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{Duration, SystemTime};

#[derive(Parser, Debug)]
#[clap(author, version, about = "Identifies and prioritizes 'data rot' (old, large, unused files) for purging.", long_about = None)]
pub struct Args {
    /// Path to the directory to scavenge for data rot
    #[clap(short, long, value_parser, default_value = ".")]
    pub path: PathBuf,

    /// Minimum age in days for a file to be considered 'rot'
    #[clap(short = 'a', long, value_parser, default_value_t = 365)]
    pub min_age_days: u64,

    /// Minimum size in megabytes for a file to be considered 'rot'
    #[clap(short = 's', long, value_parser, default_value_t = 10)]
    pub min_size_mb: u64,

    /// Limit the number of top 'rot' files to display
    #[clap(short, long, value_parser, default_value_t = 10)]
    pub limit: usize,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct RotFile {
    pub rot_score: u64,
    pub path: PathBuf,
    pub size_mb: u64,
    pub age_days: u64,
}

pub fn calculate_rot_score(metadata: &fs::Metadata, min_age_days: u64, min_size_mb: u64, now: SystemTime) -> Option<u64> {
    let file_size_bytes = metadata.len();
    let file_size_mb = file_size_bytes / (1024 * 1024);

    let modified_time = metadata.modified().ok()?;
    let duration_since_modified = now.duration_since(modified_time).ok()?;
    let age_days = duration_since_modified.as_secs() / (24 * 60 * 60);

    if age_days >= min_age_days && file_size_mb >= min_size_mb {
        // Simple rot score: age in days * size in MB
        Some(age_days * file_size_mb)
    } else {
        None
    }
}

pub fn find_rot_files(
    path: &Path,
    min_age_days: u64,
    min_size_mb: u64,
    now: SystemTime,
) -> Vec<RotFile> {
    let mut rot_files = Vec::new();
    let mut stack = vec![path.to_path_buf()];

    while let Some(current_path) = stack.pop() {
        if let Ok(entries) = fs::read_dir(&current_path) {
            for entry in entries {
                if let Ok(entry) = entry {
                    let path = entry.path();
                    if path.is_dir() {
                        stack.push(path);
                    } else if path.is_file() {
                        if let Ok(metadata) = fs::metadata(&path) {
                            if let Some(rot_score) = calculate_rot_score(&metadata, min_age_days, min_size_mb, now) {
                                let file_size_mb = metadata.len() / (1024 * 1024);
                                let modified_time = metadata.modified().unwrap();
                                let age_days = now.duration_since(modified_time).unwrap().as_secs() / (24 * 60 * 60);
                                rot_files.push(RotFile {
                                    rot_score,
                                    path,
                                    size_mb: file_size_mb,
                                    age_days,
                                });
                            }
                        }
                    }
                }
            }
        }
    }

    rot_files.sort_by(|a, b| b.rot_score.cmp(&a.rot_score)); // Sort descending
    rot_files
}

fn main() {
    let args = Args::parse();
    let now = SystemTime::now(); // Get actual time for main execution

    println!("Scavenging for data rot in '{}'...", args.path.display());
    println!("  Minimum age: {} days", args.min_age_days);
    println!("  Minimum size: {} MB", args.min_size_mb);
    println!();

    let rot_files = find_rot_files(&args.path, args.min_age_days, args.min_size_mb, now);

    if rot_files.is_empty() {
        println!("No significant data rot detected. Your digital garden is pristine!");
    } else {
        println!("Detected {} potential data rot relics (top {} shown):", rot_files.len(), args.limit);
        println!("{:-<80}", "");
        println!("{:<10} {:<10} {:<10} {}", "Score", "Age (days)", "Size (MB)", "Path");
        println!("{:-<80}", "");
        for file in rot_files.iter().take(args.limit) {
            println!(
                "{:<10} {:<10} {:<10} {}",
                file.rot_score,
                file.age_days,
                file.size_mb,
                file.path.display()
            );
        }
        println!("{:-<80}", "");
        println!("\nConsider purging these digital detritus to reclaim system vitality!");
    }
}
