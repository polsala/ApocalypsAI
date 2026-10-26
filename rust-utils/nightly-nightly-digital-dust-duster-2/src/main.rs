use clap::Parser;
use walkdir::{DirEntry, WalkDir};
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH, Duration};
use std::io;
use std::cmp::Ordering;

#[derive(Parser, Debug)]
#[clap(author, version, about = "A high-performance CLI tool to identify and report stale files, calculating their 'dustiness' based on last access/modification times.", long_about = None)]
struct Args {
    /// The root directory to start scanning from.
    #[clap(value_parser)]
    path: PathBuf,

    /// Minimum dustiness score (in days) for a file to be reported.
    /// Files older than this threshold will be considered "dusty".
    #[clap(short = 'm', long, value_parser, default_value = "30")]
    min_dustiness: u64,

    /// Maximum depth to traverse into subdirectories. 0 means only the root directory.
    #[clap(short = 'd', long, value_parser)]
    max_depth: Option<usize>,

    /// Sort results by 'path', 'size', or 'dustiness'.
    #[clap(short = 's', long, value_parser, default_value = "dustiness")]
    sort_by: SortField,

    /// Reverse the sort order.
    #[clap(short = 'r', long)]
    reverse: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum SortField {
    Path,
    Size,
    Dustiness,
}

impl std::str::FromStr for SortField {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "path" => Ok(SortField::Path),
            "size" => Ok(SortField::Size),
            "dustiness" => Ok(SortField::Dustiness),
            _ => Err(format!("Invalid sort field: {}. Must be 'path', 'size', or 'dustiness'.", s)),
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
struct DustyFile {
    path: PathBuf,
    size: u64,
    dustiness_days: u64,
}

fn main() -> io::Result<()> {
    let args = Args::parse();
    let now = SystemTime::now();

    match run(args, now) {
        Ok(dusty_files) => {
            if dusty_files.is_empty() {
                println!("No digital dust bunnies found matching your criteria. Your system is sparkling clean!");
            } else {
                println!("{:<70} {:>10} {:>10}", "Path", "Size (bytes)", "Dustiness (days)");
                println!("{}", "-".repeat(92));
                for file in dusty_files {
                    println!("{:<70} {:>10} {:>10}",
                             truncate_path(&file.path, 68),
                             file.size,
                             file.dustiness_days);
                }
            }
            Ok(())
        },
        Err(e) => {
            eprintln!("Error: {}", e);
            Err(e)
        }
    }
}

fn run(args: Args, now: SystemTime) -> io::Result<Vec<DustyFile>> {
    let mut walker = WalkDir::new(&args.path).into_iter();
    if let Some(depth) = args.max_depth {
        walker = WalkDir::new(&args.path).max_depth(depth + 1).into_iter(); // +1 because max_depth is inclusive of the starting directory
    }

    let mut dusty_files: Vec<DustyFile> = Vec::new();

    for entry_result in walker {
        let entry = match entry_result {
            Ok(e) => e,
            Err(e) => {
                eprintln!("Error accessing entry: {}", e);
                continue;
            }
        };

        if entry.file_type().is_file() {
            let metadata = match entry.metadata() {
                Ok(m) => m,
                Err(e) => {
                    eprintln!("Error getting metadata for {}: {}", entry.path().display(), e);
                    continue;
                }
            };

            let modified_time = metadata.modified().unwrap_or(UNIX_EPOCH);
            let accessed_time = metadata.accessed().unwrap_or(UNIX_EPOCH);

            let last_activity_time = if modified_time > accessed_time {
                modified_time
            } else {
                accessed_time
            };

            let duration_since_activity = now.duration_since(last_activity_time)
                .unwrap_or_else(|_| now.duration_since(UNIX_EPOCH).unwrap_or(Duration::new(0,0))); // Fallback if time goes backwards or is before epoch

            let dustiness_days = duration_since_activity.as_secs() / (24 * 60 * 60);

            if dustiness_days >= args.min_dustiness {
                dusty_files.push(DustyFile {
                    path: entry.path().to_path_buf(),
                    size: metadata.len(),
                    dustiness_days,
                });
            }
        }
    }

    // Sort results
    dusty_files.sort_by(|a, b| {
        let cmp = match args.sort_by {
            SortField::Path => a.path.cmp(&b.path),
            SortField::Size => a.size.cmp(&b.size),
            SortField::Dustiness => a.dustiness_days.cmp(&b.dustiness_days),
        };
        if args.reverse {
            cmp.reverse()
        } else {
            cmp
        }
    });

    Ok(dusty_files)
}

// Helper function to truncate long paths for display
fn truncate_path(path: &PathBuf, max_len: usize) -> String {
    let path_str = path.to_string_lossy();
    if path_str.len() > max_len {
        let start_index = path_str.len() - max_len + 3; // +3 for "..."
        format!("...{}", &path_str[start_index..])
    } else {
        path_str.to_string()
    }
}
