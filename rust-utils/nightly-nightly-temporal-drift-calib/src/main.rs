use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[command(author, version, about = "Detects and optionally fixes temporal drift in file modification timestamps.", long_about = None)]
struct Args {
    /// The directory to scan for temporal drift. Defaults to current directory.
    #[arg(default_value = ".")]
    path: PathBuf,

    /// The maximum allowed temporal drift in seconds. Files deviating more than this will be reported.
    #[arg(short, long, default_value_t = 60)]
    threshold: u64,

    /// If present, detected drifted files will have their modification times updated to the current system time.
    #[arg(short, long)]
    fix: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let current_time = SystemTime::now();
    let threshold_duration = std::time::Duration::from_secs(args.threshold);

    println!("Scanning '{}' for temporal drift (threshold: {} seconds)...", args.path.display(), args.threshold);

    let mut drifted_files_count = 0;

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| e.file_type().is_file())
    {
        let path = entry.path();
        let metadata = fs::metadata(path)?;
        let modified_time = metadata.modified()?;

        let drift_duration = if modified_time > current_time {
            modified_time.duration_since(current_time)?
        } else {
            current_time.duration_since(modified_time)?
        };

        if drift_duration > threshold_duration {
            drifted_files_count += 1;
            println!(
                "  [DRIFT DETECTED] File: '{}' -- Drift: {:.2?} {}",
                path.display(),
                drift_duration,
                if modified_time > current_time { "(future)" } else { "(past)" }
            );

            if args.fix {
                // Set mtime to current_time
                let file = fs::File::open(path)?;
                file.set_modified(current_time)?;
                println!("    -> Recalibrated '{}' to current time.", path.display());
            }
        }
    }

    if drifted_files_count == 0 {
        println!("No significant temporal drift detected. Reality remains aligned.");
    } else if args.fix {
        println!("Successfully recalibrated {} drifted files.", drifted_files_count);
    } else {
        println!("Detected {} files with temporal drift. Use --fix to recalibrate.", drifted_files_count);
    }

    Ok(())
}

// Helper function for tests to set modification time
#[cfg(test)]
fn set_mtime(path: &Path, duration_from_now: std::time::Duration, is_future: bool) -> Result<(), Box<dyn std::error::Error>> {
    use filetime::{set_file_times, FileTime};
    let now = SystemTime::now();
    let target_time = if is_future {
        now + duration_from_now
    } else {
        now - duration_from_now
    };
    let target_file_time = FileTime::from_system_time(target_time);
    set_file_times(path, target_file_time, target_file_time)?;
    Ok(())
}
