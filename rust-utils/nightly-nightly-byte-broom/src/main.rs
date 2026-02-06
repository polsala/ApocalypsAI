use clap::Parser;
use walkdir::WalkDir;
use std::path::PathBuf;
use std::time::SystemTime;
use chrono::{Utc, Duration as ChronoDuration};
use human_bytes::human_bytes;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Sweep away digital dust bunnies (large or old files)!", long_about = None)]
struct Args {
    /// Directory to sweep
    #[clap(default_value = ".")]
    path: PathBuf,

    /// Minimum size for a file to be considered a dust bunny (e.g., "10MB", "1GB")
    #[clap(short, long, default_value = "10MB")]
    min_size: String,

    /// Minimum age for a file to be considered a dust bunny (e.g., "30d", "1y")
    #[clap(short, long, default_value = "30d")]
    min_age: String,
}

#[derive(Debug)]
struct DustBunny {
    path: PathBuf,
    size: u64,
    age_days: i64,
}

fn parse_size_string(s: &str) -> Option<u64> {
    let s_lower = s.to_lowercase();
    let (num_str, unit_str) = if s_lower.ends_with("kb") {
        (&s_lower[..s_lower.len() - 2], "kb")
    } else if s_lower.ends_with("mb") {
        (&s_lower[..s_lower.len() - 2], "mb")
    } else if s_lower.ends_with("gb") {
        (&s_lower[..s_lower.len() - 2], "gb")
    } else if s_lower.ends_with("tb") {
        (&s_lower[..s_lower.len() - 2], "tb")
    } else if s_lower.ends_with('k') {
        (&s_lower[..s_lower.len() - 1], "kb")
    } else if s_lower.ends_with('m') {
        (&s_lower[..s_lower.len() - 1], "mb")
    } else if s_lower.ends_with('g') {
        (&s_lower[..s_lower.len() - 1], "gb")
    } else if s_lower.ends_with('t') {
        (&s_lower[..s_lower.len() - 1], "tb")
    } else {
        (s_lower.as_str(), "")
    };

    let num: f64 = num_str.trim().parse().ok()?;
    match unit_str {
        "kb" => Some((num * 1024.0) as u64),
        "mb" => Some((num * 1024.0 * 1024.0) as u64),
        "gb" => Some((num * 1024.0 * 1024.0 * 1024.0) as u64),
        "tb" => Some((num * 1024.0 * 1024.0 * 1024.0 * 1024.0) as u64),
        "" => Some(num as u64), // Assume bytes if no unit
        _ => None,
    }
}

fn parse_age_string(s: &str) -> Option<ChronoDuration> {
    let s_lower = s.to_lowercase();
    let (num_str, unit_str) = if s_lower.ends_with('d') {
        (&s_lower[..s_lower.len() - 1], "d")
    } else if s_lower.ends_with('w') {
        (&s_lower[..s_lower.len() - 1], "w")
    } else if s_lower.ends_with('m') { // month
        (&s_lower[..s_lower.len() - 1], "m")
    } else if s_lower.ends_with('y') {
        (&s_lower[..s_lower.len() - 1], "y")
    } else {
        (s_lower.as_str(), "d") // Default to days if no unit
    };

    let num: i64 = num_str.trim().parse().ok()?;
    match unit_str {
        "d" => Some(ChronoDuration::days(num)),
        "w" => Some(ChronoDuration::weeks(num)),
        "m" => Some(ChronoDuration::days(num * 30)), // Approximation for months
        "y" => Some(ChronoDuration::days(num * 365)), // Approximation for years
        _ => None,
    }
}

fn find_dust_bunnies(
    root_path: &PathBuf,
    min_size_bytes: u64,
    min_age_duration: ChronoDuration,
) -> Vec<DustBunny> {
    let mut bunnies = Vec::new();
    let now = Utc::now();

    for entry in WalkDir::new(root_path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = std::fs::metadata(path) {
                let size = metadata.len();
                if let Ok(modified_time) = metadata.modified() {
                    let modified_utc = chrono::DateTime::<Utc>::from(modified_time);
                    let age = now.signed_duration_since(modified_utc);

                    if size >= min_size_bytes && age >= min_age_duration {
                        bunnies.push(DustBunny {
                            path: path.to_path_buf(),
                            size,
                            age_days: age.num_days(),
                        });
                    }
                }
            }
        }
    }
    bunnies
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let min_size_bytes = parse_size_string(&args.min_size)
        .ok_or_else(|| format!("Invalid minimum size format: {}", args.min_size))?;
    let min_age_duration = parse_age_string(&args.min_age)
        .ok_or_else(|| format!("Invalid minimum age format: {}", args.min_age))?;

    println!("Sweeping for digital dust bunnies in '{}'...", args.path.display());
    println!("  (Looking for files >= {} and >= {} old)", human_bytes(min_size_bytes as f64), args.min_age);
    println!();

    let bunnies = find_dust_bunnies(&args.path, min_size_bytes, min_age_duration);

    if bunnies.is_empty() {
        println!("✨ The digital realm is sparkling clean! No dust bunnies found. ✨");
    } else {
        println!("🧹 Found some digital dust bunnies lurking around:");
        for bunny in bunnies {
            println!(
                "  - A forgotten relic: {} ({}, {} days old)",
                bunny.path.display(),
                human_bytes(bunny.size as f64),
                bunny.age_days
            );
        }
        println!("\nConsider giving these digital dust bunnies a new home (the recycle bin) or a good scrub!");
    }

    Ok(())
}
