use clap::{Parser, Subcommand};
use walkdir::WalkDir;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use chrono::{Utc, Duration as ChronoDuration};

#[derive(Parser, Debug)]
#[command(author, version, about = "Collects digital dust bunnies (old files) from your filesystem.", long_about = None)]
struct Cli {
    /// The path to scan for dust bunnies.
    #[arg(short, long, value_name = "PATH")]
    path: PathBuf,

    /// Files older than this many days will be considered dust bunnies.
    #[arg(short, long, default_value_t = 365, value_name = "DAYS")]
    age: u64,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Lists the digital dust bunnies found.
    List,
    /// Moves the digital dust bunnies to a specified destination directory.
    Move {
        /// The destination directory for the moved dust bunnies.
        #[arg(short, long, value_name = "DEST_PATH")]
        destination: PathBuf,
    },
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();

    let threshold_time = Utc::now() - ChronoDuration::days(cli.age as i64);

    println!("Scanning '{}' for files older than {} days (before {})...",
             cli.path.display(), cli.age, threshold_time.format("%Y-%m-%d %H:%M:%S"));

    let mut dust_bunnies_found = 0;

    for entry in WalkDir::new(&cli.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_utc: chrono::DateTime<Utc> = modified_time.into();
                    if modified_utc < threshold_time {
                        dust_bunnies_found += 1;
                        match &cli.command {
                            Commands::List => {
                                println!("  [DUST BUNNY] {}", path.display());
                            },
                            Commands::Move { destination } => {
                                let relative_path = path.strip_prefix(&cli.path).unwrap_or(path);
                                let dest_path = destination.join(relative_path);

                                if let Some(parent) = dest_path.parent() {
                                    fs::create_dir_all(parent)?;
                                }

                                match fs::rename(path, &dest_path) {
                                    Ok(_) => println!("  [MOVED] {} -> {}", path.display(), dest_path.display()),
                                    Err(e) => eprintln!("  [ERROR] Failed to move {}: {}", path.display(), e),
                                }
                            },
                        }
                    }
                }
            }
        }
    }

    println!("Scan complete. Found {} digital dust bunnies.", dust_bunnies_found);

    Ok(())
}

// Helper to convert SystemTime to chrono::DateTime<Utc>
impl From<SystemTime> for chrono::DateTime<Utc> {
    fn from(sys_time: SystemTime) -> Self {
        chrono::DateTime::from(sys_time)
    }
}
