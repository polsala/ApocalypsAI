use clap::Parser;
use chrono::{Utc, Duration, DateTime};
use walkdir::WalkDir;
use std::fs;
use std::path::{Path, PathBuf};
use dialoguer::{Confirm, Select};
use colored::Colorize;
use humantime::format_duration;
use std::thread::sleep;
use std::time::Duration as StdDuration;

#[derive(Parser, Debug)]
#[command(author, version, about = "Sweeps away digital dust bunnies!", long_about = None)]
struct Args {
    /// Path to scan for dust bunnies
    #[arg(short, long, default_value = ".")]
    path: PathBuf,

    /// Files older than this many days are considered dust bunnies
    #[arg(short, long, default_value_t = 30)]
    age_days: u64,

    /// Enable interactive mode to choose action for each dust bunny
    #[arg(short, long)]
    interactive: bool,

    /// Move all found dust bunnies to this directory (overrides interactive)
    #[arg(long)]
    cuddle_to: Option<PathBuf>,

    /// Release (delete) all found dust bunnies (overrides interactive, requires --confirm-release)
    #[arg(long)]
    release_all: bool,

    /// Confirm deletion when using --release-all
    #[arg(long)]
    confirm_release: bool,
}

struct DustBunny {
    path: PathBuf,
    modified: DateTime<Utc>,
    size: u64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if args.release_all && !args.confirm_release {
        eprintln!("{}", "Error: --release-all requires --confirm-release for safety.".red());
        std::process::exit(1);
    }

    let cutoff_time = Utc::now() - Duration::days(args.age_days as i64);
    println!("{} Scanning '{}' for files older than {} days (modified before {})...",
             "🔍".yellow(), args.path.display(), args.age_days, cutoff_time.format("%Y-%m-%d %H:%M:%S").blue());

    let mut dust_bunnies = Vec::new();
    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let metadata = entry.metadata()?;
            let modified_time: DateTime<Utc> = metadata.modified()?.into();
            if modified_time < cutoff_time {
                dust_bunnies.push(DustBunny {
                    path: entry.path().to_path_buf(),
                    modified: modified_time,
                    size: metadata.len(),
                });
            }
        }
    }

    if dust_bunnies.is_empty() {
        println!("{}", "✨ No digital dust bunnies found! Your digital space is sparkling clean.".green());
        return Ok(());
    }

    println!("{} Found {} digital dust bunnies:", "🐰".yellow(), dust_bunnies.len().to_string().yellow());

    if let Some(cuddle_dir) = args.cuddle_to {
        fs::create_dir_all(&cuddle_dir)?;
        println!("{} Cuddling all dust bunnies to '{}'...", "📦".blue(), cuddle_dir.display());
        for bunny in dust_bunnies {
            let file_name = bunny.path.file_name().ok_or("Invalid file name")?;
            let dest_path = cuddle_dir.join(file_name);
            match fs::rename(&bunny.path, &dest_path) {
                Ok(_) => println!("  {} '{}' -> '{}'", "✅".green(), bunny.path.display(), dest_path.display()),
                Err(e) => eprintln!("  {} Failed to cuddle '{}': {}", "❌".red(), bunny.path.display(), e),
            }
        }
    } else if args.release_all {
        println!("{} Releasing all dust bunnies...", "🗑️".blue());
        for bunny in dust_bunnies {
            match fs::remove_file(&bunny.path) {
                Ok(_) => println!("  {} Released '{}'", "✅".green(), bunny.path.display()),
                Err(e) => eprintln!("  {} Failed to release '{}': {}", "❌".red(), bunny.path.display(), e),
            }
        }
    } else if args.interactive {
        println!("{}", "Entering interactive mode...".cyan());
        for bunny in dust_bunnies {
            println!("\n{} Dust Bunny: {}", "👉".yellow(), bunny.path.display().to_string().blue());
            println!("  Modified: {} ({} ago)",
                     bunny.modified.format("%Y-%m-%d %H:%M:%S"),
                     format_duration(Utc::now().signed_duration_since(bunny.modified).to_std()?).to_string().cyan());
            println!("  Size: {} bytes", bunny.size.to_string().magenta());

            let options = &["Cuddle (Move to archive)", "Release (Delete)", "Ignore"];
            let selection = Select::new()
                .with_prompt("What to do with this dust bunny?")
                .items(options)
                .default(2)
                .interact()?;

            match selection {
                0 => { // Cuddle
                    let default_cuddle_dir = PathBuf::from("./dust_bunnies_archive");
                    let cuddle_dir_str = dialoguer::Input::<String>::new()
                        .with_prompt("Enter archive directory (default: ./dust_bunnies_archive)")
                        .default(default_cuddle_dir.to_string_lossy().into_owned())
                        .interact_text()?;
                    let cuddle_dir = PathBuf::from(cuddle_dir_str);
                    fs::create_dir_all(&cuddle_dir)?;
                    let file_name = bunny.path.file_name().ok_or("Invalid file name")?;
                    let dest_path = cuddle_dir.join(file_name);
                    match fs::rename(&bunny.path, &dest_path) {
                        Ok(_) => println!("  {} Cuddled '{}' to '{}'", "✅".green(), bunny.path.display(), dest_path.display()),
                        Err(e) => eprintln!("  {} Failed to cuddle '{}': {}", "❌".red(), bunny.path.display(), e),
                    }
                }
                1 => { // Release
                    if Confirm::new()
                        .with_prompt(format!("Are you sure you want to release '{}'?", bunny.path.display()))
                        .interact()? {
                        match fs::remove_file(&bunny.path) {
                            Ok(_) => println!("  {} Released '{}'", "✅".green(), bunny.path.display()),
                            Err(e) => eprintln!("  {} Failed to release '{}': {}", "❌".red(), bunny.path.display(), e),
                        }
                    } else {
                        println!("  {} Keeping '{}'", "ℹ️".blue(), bunny.path.display());
                    }
                }
                _ => { // Ignore
                    println!("  {} Ignoring '{}'", "ℹ️".blue(), bunny.path.display());
                }
            }
        }
    } else {
        // Default: list only
        for bunny in dust_bunnies {
            println!("  - {} (Modified: {}, Size: {} bytes)",
                     bunny.path.display().to_string().blue(),
                     bunny.modified.format("%Y-%m-%d %H:%M:%S"),
                     bunny.size.to_string().magenta());
        }
        println!("\n{} Use --interactive, --cuddle-to, or --release-all to manage these dust bunnies.", "💡".cyan());
    }

    Ok(())
}
