use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::SystemTime;
use chrono::{Utc, Duration, DateTime};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance CLI tool to find and 'compost' old, unused files.", long_about = None)]
struct Args {
    /// The directory to scan for digital dust bunnies
    path: PathBuf,

    /// Files older than this many days will be considered dust bunnies
    #[arg(short = 'a', long, default_value_t = 365)]
    age_days: u64,

    /// Optional directory to move identified dust bunnies to. If not provided, files are only listed.
    #[arg(short = 'c', long)]
    compost_dir: Option<PathBuf>,

    /// Perform composting without confirmation (use with caution!)
    #[arg(short = 'f', long)]
    force: bool,
}

fn is_file_old_enough(file_path: &Path, age_threshold: DateTime<Utc>) -> Result<bool, String> {
    let metadata = fs::metadata(file_path)
        .map_err(|e| format!("Failed to get metadata for {}: {}", file_path.display(), e))?;

    let modified_time: DateTime<Utc> = metadata.modified()
        .map_err(|e| format!("Failed to get modified time for {}: {}", file_path.display(), e))?
        .into(); // Convert SystemTime to DateTime<Utc>

    Ok(modified_time < age_threshold)
}

fn compost_file(file_path: &Path, compost_dir: &Path) -> Result<(), String> {
    fs::create_dir_all(compost_dir)
        .map_err(|e| format!("Failed to create compost directory {}: {}", compost_dir.display(), e))?;

    let file_name = file_path.file_name()
        .ok_or_else(|| format!("Could not get file name for {}", file_path.display()))?;

    let destination_path = compost_dir.join(file_name);

    println!("    Moving '{}' to '{}'", file_path.display(), destination_path.display());
    fs::rename(file_path, &destination_path)
        .map_err(|e| format!("Failed to move '{}' to '{}': {}", file_path.display(), destination_path.display(), e))?;

    Ok(())
}

fn main() -> Result<(), String> {
    let args = Args::parse();

    let scan_path = &args.path;
    let age_duration = Duration::days(args.age_days as i64);
    let age_threshold = Utc::now() - age_duration;

    if !scan_path.exists() {
        return Err(format!("Error: Path '{}' does not exist.", scan_path.display()));
    }
    if !scan_path.is_dir() {
        return Err(format!("Error: Path '{}' is not a directory.", scan_path.display()));
    }

    println!("\nScanning '{}' for digital dust bunnies older than {} days...\n", scan_path.display(), args.age_days);

    let mut dust_bunnies: Vec<PathBuf> = Vec::new();

    for entry in WalkDir::new(scan_path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            match is_file_old_enough(path, age_threshold) {
                Ok(true) => {
                    dust_bunnies.push(path.to_path_buf());
                },
                Ok(false) => { /* File is not old enough */ },
                Err(e) => eprintln!("Warning: {}", e),
            }
        }
    }

    if dust_bunnies.is_empty() {
        println!("No digital dust bunnies found. Your filesystem is sparkling clean!\n");
        return Ok(());
    }

    println!("Found {} digital dust bunnies:\n", dust_bunnies.len());
    for bunny in &dust_bunnies {
        println!("- {}", bunny.display());
    }

    if let Some(compost_dir) = &args.compost_dir {
        if !args.force {
            println!("\nProceed with composting these files to '{}'? (y/N)", compost_dir.display());
            let mut input = String::new();
            std::io::stdin().read_line(&mut input)
                .map_err(|e| format!("Failed to read input: {}", e))?;
            if input.trim().to_lowercase() != "y" {
                println!("Composting cancelled. Dust bunnies remain.\n");
                return Ok(());
            }
        }

        println!("\nComposting digital dust bunnies...\n");
        let mut composted_count = 0;
        for bunny in dust_bunnies {
            match compost_file(&bunny, compost_dir) {
                Ok(_) => composted_count += 1,
                Err(e) => eprintln!("Error composting {}: {}", bunny.display(), e),
            }
        }
        println!("\nSuccessfully composted {} digital dust bunnies.\n", composted_count);
    } else {
        println!("\nTo compost these files, run again with the --compost-dir <DIRECTORY> option.\n");
    }

    Ok(())
}
