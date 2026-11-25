use clap::Parser;
use chrono::{Duration, Local, DateTime};
use walkdir::WalkDir;
use std::fs;
use std::path::{Path, PathBuf};
use std::io;
use std::error::Error;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Sweeps away digital dust bunnies (old, unaccessed files).", long_about = None)]
pub struct Args {
    /// The path to scan for dust bunnies.
    #[clap(value_parser)]
    pub path: PathBuf,

    /// Files older than this many days will be considered dust bunnies.
    #[clap(short, long, value_parser, value_name = "DAYS", value_than_eq = 0)]
    pub older_than: u64,

    /// Directory to move dust bunnies to. If not specified, they are only listed.
    #[clap(short, long, value_parser, value_name = "DIR")]
    pub archive_to: Option<PathBuf>,

    /// Perform a dry run: list files but don't move them.
    #[clap(short, long)]
    pub dry_run: bool,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();
    run_app(args)
}

pub fn run_app(args: Args) -> Result<(), Box<dyn Error>> {
    if !args.path.exists() {
        return Err(format!("Error: Path '{}' does not exist.", args.path.display()).into());
    }
    if !args.path.is_dir() {
        return Err(format!("Error: Path '{}' is not a directory.", args.path.display()).into());
    }

    let cutoff_time = Local::now() - Duration::days(args.older_than as i64);

    if let Some(ref archive_dir) = args.archive_to {
        if !archive_dir.exists() {
            println!("Creating archive directory: {}", archive_dir.display());
            fs::create_dir_all(archive_dir)?;
        } else if !archive_dir.is_dir() {
            return Err(format!("Error: Archive path '{}' is not a directory.", archive_dir.display()).into());
        }
    }

    println!("Scanning '{}' for files older than {} days (cutoff: {})...",
             args.path.display(), args.older_than, cutoff_time.format("%Y-%m-%d %H:%M:%S"));

    let mut found_count = 0;
    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                // Use modified time as access time is often not updated on Linux by default
                // and can be unreliable. Modified time is a good proxy for "last touched".
                if let Ok(modified_time_sys) = metadata.modified() {
                    let modified_datetime: DateTime<Local> = modified_time_sys.into();
                    if modified_datetime < cutoff_time {
                        found_count += 1;
                        println!("  Found dust bunny: '{}' (last modified: {})",
                                 path.display(), modified_datetime.format("%Y-%m-%d %H:%M:%S"));

                        if !args.dry_run {
                            if let Some(ref archive_dir) = args.archive_to {
                                let file_name = path.file_name().ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "Could not get file name"))?;
                                let dest_path = archive_dir.join(file_name);
                                println!("    Moving to: '{}'", dest_path.display());
                                fs::rename(path, &dest_path)?;
                            } else {
                                println!("    (No archive directory specified, skipping move)");
                            }
                        } else {
                            println!("    (Dry run, not moving)");
                        }
                    }
                } else {
                    eprintln!("Warning: Could not get modified time for '{}'", path.display());
                }
            }
        }
    }

    println!("\nScan complete. Found {} potential dust bunnies.", found_count);
    Ok(())
}
