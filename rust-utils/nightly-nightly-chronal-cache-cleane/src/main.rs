use clap::Parser;
use std::error::Error;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::SystemTime;
use chrono::{Utc, Duration as ChronoDuration, DateTime};

#[derive(Parser, Debug)]
#[command(author, version, about = "A whimsical Rust CLI tool that 'archives' old files into a 'temporal void'.", long_about = None)]
pub struct Args {
    /// The directory to scan for old files.
    #[arg(short, long)]
    pub target_dir: PathBuf,

    /// Files older than this many days will be moved to the temporal void.
    #[arg(short, long)]
    pub age: u64,

    /// The directory where old files will be 'archived' (the temporal void).
    /// Defaults to ~/.chronal_void/
    #[arg(short, long)]
    pub void_dir: Option<PathBuf>,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();
    run_app(args)
}

// This function contains the core logic, separated for testability.
fn run_app(args: Args) -> Result<(), Box<dyn Error>> {
    let target_dir = &args.target_dir;
    let age_threshold_days = args.age;

    if !target_dir.is_dir() {
        eprintln!("Error: Target directory '{}' does not exist or is not a directory.", target_dir.display());
        return Ok(()); // Graceful exit for non-existent target dir
    }

    let void_dir = match args.void_dir {
        Some(path) => path,
        None => {
            let home_dir = dirs::home_dir().ok_or("Could not find home directory")?;
            home_dir.join(".chronal_void")
        }
    };

    if !void_dir.exists() {
        println!("Creating the temporal void at '{}'...", void_dir.display());
        fs::create_dir_all(&void_dir)?;
    }

    println!("Initiating Chronal Cache Cleaner...");
    println!("Scanning '{}' for files older than {} days...", target_dir.display(), age_threshold_days);
    println!("Files will be moved to the temporal void: '{}'", void_dir.display());

    let now: DateTime<Utc> = Utc::now();
    let threshold_time = now - ChronoDuration::days(age_threshold_days as i64);

    let mut moved_count = 0;

    for entry in fs::read_dir(target_dir)? {
        let entry = entry?;
        let path = entry.path();

        if path.is_file() {
            let metadata = fs::metadata(&path)?;
            let modified_time: DateTime<Utc> = metadata.modified()?.into();

            if modified_time < threshold_time {
                let file_name = path.file_name().ok_or("Could not get file name")?;
                let destination_path = void_dir.join(file_name);

                println!("Sending '{}' to the temporal void...", path.display());
                fs::rename(&path, &destination_path)?;
                moved_count += 1;
            }
        }
    }

    if moved_count > 0 {
        println!("Chronal Cache Cleaner complete! {} ancient echoes sent to the void.", moved_count);
    } else {
        println!("No ancient echoes found. The timeline is pristine!");
    }

    Ok(())
}
