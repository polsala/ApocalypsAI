use std::{
    fs,
    path::{Path, PathBuf},
    time::SystemTime,
};
use chrono::{DateTime, Utc, Duration};
use clap::Parser;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Directory to scavenge
    #[clap(short, long, default_value = ".")]
    path: PathBuf,

    /// Maximum age in days for a file to be considered 'forgotten'
    #[clap(short, long, default_value_t = 30)]
    max_age_days: u64,

    /// Minimum size in bytes for a file to be considered 'significant'
    #[clap(short, long, default_value_t = 1024 * 1024)] // 1MB
    min_size_bytes: u64,

    /// Include subdirectories in the scan
    #[clap(short, long)]
    recursive: bool,
}

struct ScavengedFile {
    path: PathBuf,
    size: u64,
    modified: SystemTime,
    age_days: i64,
    category: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let now = Utc::now();

    println!("Initiating Nightly Resource Scavenger Protocol...");
    println!("Scanning: {}", args.path.display());
    println!("Criteria: Max age {} days, Min size {} bytes", args.max_age_days, args.min_size_bytes);
    println!("Recursive: {}", args.recursive);
    println!("--------------------------------------------------");

    let mut files_found: Vec<ScavengedFile> = Vec::new();
    scan_directory(&args.path, &args, &mut files_found, now)?;

    if files_found.is_empty() {
        println!("\nNo forgotten relics or dusty archives found. Your digital wasteland is surprisingly tidy!");
    } else {
        println!("\n--- Scavenger Report ---");
        // Sort files for consistent output
        files_found.sort_by(|a, b| a.path.cmp(&b.path));

        for file in files_found {
            let modified_dt: DateTime<Utc> = file.modified.into();
            println!(
                "[{}] {} ({} bytes, last modified: {} - {} days ago)",
                file.category,
                file.path.display(),
                file.size,
                modified_dt.format("%Y-%m-%d"),
                file.age_days
            );
        }
        println!("------------------------");
        println!("Consider these findings for reclamation or respectful disposal.");
    }

    Ok(())
}

fn scan_directory(
    dir: &Path,
    args: &Args,
    files_found: &mut Vec<ScavengedFile>,
    now: DateTime<Utc>,
) -> Result<(), Box<dyn std::error::Error>> {
    // Check if the directory exists and is readable
    if !dir.exists() || !dir.is_dir() {
        eprintln!("Warning: Directory '{}' does not exist or is not a directory. Skipping.", dir.display());
        return Ok(());
    }

    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        let path = entry.path();
        let metadata = match entry.metadata() {
            Ok(m) => m,
            Err(e) => {
                eprintln!("Warning: Could not get metadata for '{}': {}. Skipping.", path.display(), e);
                continue;
            }
        };

        if metadata.is_dir() {
            if args.recursive {
                scan_directory(&path, args, files_found, now)?;
            }
        } else if metadata.is_file() {
            let modified_time = match metadata.modified() {
                Ok(t) => t,
                Err(e) => {
                    eprintln!("Warning: Could not get modification time for '{}': {}. Skipping.", path.display(), e);
                    continue;
                }
            };
            let modified_dt: DateTime<Utc> = modified_time.into();
            let age_duration = now.signed_duration_since(modified_dt);
            let age_days = age_duration.num_days();

            let mut category_parts = Vec::new();
            let mut include_file = false;

            if age_days >= args.max_age_days as i64 {
                category_parts.push("Forgotten Relic");
                include_file = true;
            }
            if metadata.len() >= args.min_size_bytes {
                category_parts.push("Significant");
                include_file = true;
            }
            // Add more whimsical categories based on file extensions or names
            if path.extension().map_or(false, |ext| {
                let ext_str = ext.to_ascii_lowercase();
                ext_str == "log" || ext_str == "tmp" || ext_str == "bak" || ext_str == "old" || ext_str == "swp"
            }) {
                category_parts.push("Ephemeral Scrap");
                include_file = true;
            }

            if include_file {
                let category = if category_parts.is_empty() {
                    "Uncategorized Find".to_string()
                } else {
                    // Combine categories, e.g., "Forgotten Relic & Significant (Ephemeral Scrap)"
                    let mut combined = String::new();
                    let mut has_main_category = false;
                    let mut has_ephemeral = false;

                    for part in &category_parts {
                        if *part == "Ephemeral Scrap" {
                            has_ephemeral = true;
                        } else {
                            if has_main_category { combined.push_str(" & "); }
                            combined.push_str(part);
                            has_main_category = true;
                        }
                    }

                    if combined.is_empty() && has_ephemeral { // Only Ephemeral Scrap
                        "Ephemeral Scrap".to_string()
                    } else if has_ephemeral { // Main categories + Ephemeral Scrap
                        format!("{} (Ephemeral Scrap)", combined)
                    } else { // Only main categories
                        combined
                    }
                };

                files_found.push(ScavengedFile {
                    path,
                    size: metadata.len(),
                    modified: modified_time,
                    age_days,
                    category,
                });
            }
        }
    }
    Ok(())
}
