use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::fs;
use std::path::PathBuf;
use std::io::{self, Write};

#[derive(Parser, Debug)]
#[clap(author, version, about = "Sweep away stellar dust (old, unused files) from your filesystem.", long_about = None)]
pub struct Args {
    /// The directory to start sweeping for stellar dust.
    #[clap(value_parser)]
    pub path: PathBuf,

    /// Files older than this many days will be considered dust.
    #[clap(short = 'd', long)]
    pub days: Option<u64>,

    /// Files older than this many months will be considered dust.
    #[clap(short = 'm', long)]
    pub months: Option<u64>,

    /// Files older than this many years will be considered dust.
    #[clap(short = 'y', long)]
    pub years: Option<u64>,

    /// Sort results by 'path', 'size', or 'age'.
    #[clap(short = 's', long, default_value = "age", value_parser = ["path", "size", "age"])]
    pub sort_by: String,

    /// Reverse the sort order.
    #[clap(short = 'r', long)]
    pub reverse: bool,
}

#[derive(Debug)]
pub struct DustFile {
    pub path: PathBuf,
    pub size: u64,
    pub modified: DateTime<Utc>,
    pub age_days: i64,
}

fn main() -> io::Result<()> {
    let args = Args::parse();
    let mut stdout = io::stdout();
    run_app_and_print(args, &mut stdout)
}

// This function contains the core logic for finding and sorting dust files.
pub fn find_stellar_dust(args: &Args) -> io::Result<Vec<DustFile>> {
    let now = Utc::now();

    let threshold_duration = if let Some(days) = args.days {
        Duration::days(days as i64)
    } else if let Some(months) = args.months {
        Duration::days((months as i64) * 30) // Approximation for months
    } else if let Some(years) = args.years {
        Duration::days((years as i64) * 365) // Approximation for years
    } else {
        // Default if no specific duration is provided
        Duration::days(90) // Default to 90 days
    };

    let mut dust_files: Vec<DustFile> = Vec::new();

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        if entry.file_type().is_file() {
            let metadata = match fs::metadata(entry.path()) {
                Ok(meta) => meta,
                Err(_) => continue, // Skip files we can't get metadata for
            };

            let modified_time: DateTime<Utc> = match metadata.modified() {
                Ok(time) => time.into(),
                Err(_) => continue, // Skip files we can't get modification time for
            };

            if now - modified_time > threshold_duration {
                let age_days = (now - modified_time).num_days();
                dust_files.push(DustFile {
                    path: entry.path().to_path_buf(),
                    size: metadata.len(),
                    modified: modified_time,
                    age_days,
                });
            }
        }
    }

    // Sort the results
    match args.sort_by.as_str() {
        "path" => dust_files.sort_by(|a, b| a.path.cmp(&b.path)),
        "size" => dust_files.sort_by(|a, b| a.size.cmp(&b.size)),
        "age" => dust_files.sort_by(|a, b| b.age_days.cmp(&a.age_days)), // Newest first by default for age
        _ => {} // Should not happen due to clap validation
    }

    if args.reverse {
        dust_files.reverse();
    }

    Ok(dust_files)
}

// This function handles printing the results to a given writer.
pub fn run_app_and_print(args: Args, writer: &mut dyn Write) -> io::Result<()> {
    let threshold_duration = if let Some(days) = args.days {
        Duration::days(days as i64)
    } else if let Some(months) = args.months {
        Duration::days((months as i64) * 30) // Approximation
    } else if let Some(years) = args.years {
        Duration::days((years as i64) * 365) // Approximation
    } else {
        Duration::days(90) // Default to 90 days
    };
    let threshold_days_for_display = threshold_duration.num_days();

    let dust_files = find_stellar_dust(&args)?; // Pass a reference to args

    if dust_files.is_empty() {
        writeln!(writer, "No stellar dust found older than {} days. Your digital cosmos is sparkling!", threshold_days_for_display)?;
    } else {
        writeln!(writer, "Stellar Dust Report (older than {} days):", threshold_days_for_display)?;
        writeln!(writer, "{:<70} {:>10} {:<25} {:>8}", "PATH", "SIZE (B)", "LAST MODIFIED", "AGE (D)")?;
        writeln!(writer, "{}", "-".repeat(115))?;
        for file in dust_files {
            writeln!(
                writer,
                "{:<70} {:>10} {:<25} {:>8}",
                file.path.display(),
                file.size,
                file.modified.format("%Y-%m-%d %H:%M:%S"),
                file.age_days
            )?;
        }
        writeln!(writer, "\nConsider sweeping these files away to free up cosmic space!")?;
    }

    Ok(())
}
