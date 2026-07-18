use clap::Parser;
use walkdir::WalkDir;
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use humansize::{format_size, DECIMAL};
use std::cmp::Ordering;

#[derive(Parser, Debug)]
#[command(author, version, about = "Audits disk usage by file type and size, identifying digital hoarding patterns.", long_about = None)]
struct Args {
    /// The root directory to start the audit from.
    path: PathBuf,

    /// Number of top largest files/directories to display (default: 5).
    #[arg(short = 'n', long, default_value_t = 5)]
    top_n: usize,

    /// Minimum file size (e.g., "10MB", "1GB") to include in the detailed file list.
    #[arg(short = 'm', long, value_parser = parse_size_string)]
    min_size: Option<u64>,

    /// Comma-separated list of extensions to include (e.g., "jpg,png,mp4"). If not specified, all extensions are included.
    #[arg(short = 'e', long, value_delimiter = ',')]
    extensions: Option<Vec<String>>,

    /// Show more detailed output, including individual files.
    #[arg(short = 'v', long)]
    verbose: bool,
}

fn parse_size_string(s: &str) -> Result<u64, String> {
    let s_lower = s.to_lowercase();
    let (value_str, unit_str) = if s_lower.ends_with("kb") {
        (&s_lower[..s_lower.len() - 2], "kb")
    } else if s_lower.ends_with("mb") {
        (&s_lower[..s_lower.len() - 2], "mb")
    } else if s_lower.ends_with("gb") {
        (&s_lower[..s_lower.len() - 2], "gb")
    } else if s_lower.ends_with("tb") {
        (&s_lower[..s_lower.len() - 2], "tb")
    } else if s_lower.ends_with("b") {
        (&s_lower[..s_lower.len() - 1], "b")
    } else {
        (s_lower.as_str(), "b") // Assume bytes if no unit
    };

    let value = value_str.trim().parse::<f64>()
        .map_err(|_| format!("Invalid size value: {}", value_str))?;

    let bytes = match unit_str {
        "b" => value as u64,
        "kb" => (value * 1024.0) as u64,
        "mb" => (value * 1024.0 * 1024.0) as u64,
        "gb" => (value * 1024.0 * 1024.0 * 1024.0) as u64,
        "tb" => (value * 1024.0 * 1024.0 * 1024.0 * 1024.0) as u64,
        _ => return Err(format!("Unknown size unit: {}", unit_str)),
    };
    Ok(bytes)
}

struct AuditResult {
    total_size: u64,
    file_count: u64,
    extension_summary: HashMap<String, (u64, u64)>, // (total_size, count)
    largest_files: Vec<(PathBuf, u64)>,
    largest_dirs: Vec<(PathBuf, u64)>,
}

fn run_audit(args: &Args) -> Result<AuditResult, Box<dyn std::error::Error>> {
    let mut total_size = 0;
    let mut file_count = 0;
    let mut extension_summary: HashMap<String, (u64, u64)> = HashMap::new();
    let mut largest_files: Vec<(PathBuf, u64)> = Vec::new();
    let mut dir_sizes: HashMap<PathBuf, u64> = HashMap::new();

    let allowed_extensions: Option<Vec<String>> = args.extensions.as_ref().map(|exts| {
        exts.iter().map(|s| s.to_lowercase()).collect()
    });

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        let metadata = entry.metadata()?;

        if metadata.is_file() {
            let size = metadata.len();
            let extension = path.extension()
                .and_then(|s| s.to_str())
                .unwrap_or("")
                .to_lowercase();

            if let Some(ref allowed) = allowed_extensions {
                if !allowed.contains(&extension) {
                    continue; // Skip if extension not allowed
                }
            }

            total_size += size;
            file_count += 1;

            let entry = extension_summary.entry(extension.clone()).or_insert((0, 0));
            entry.0 += size;
            entry.1 += 1;

            // Keep track of largest files
            if args.verbose && size >= args.min_size.unwrap_or(0) {
                largest_files.push((path.to_path_buf(), size));
                largest_files.sort_unstable_by(|a, b| b.1.cmp(&a.1)); // Sort descending by size
                largest_files.truncate(args.top_n);
            }

            // Accumulate directory sizes
            if let Some(parent) = path.parent() {
                *dir_sizes.entry(parent.to_path_buf()).or_insert(0) += size;
            }
        } else if metadata.is_dir() {
            // Initialize directory size if not already present
            dir_sizes.entry(path.to_path_buf()).or_insert(0);
        }
    }

    let mut largest_dirs: Vec<(PathBuf, u64)> = dir_sizes.into_iter().collect();
    largest_dirs.sort_unstable_by(|a, b| b.1.cmp(&a.1));
    largest_dirs.truncate(args.top_n);

    Ok(AuditResult {
        total_size,
        file_count,
        extension_summary,
        largest_files,
        largest_dirs,
    })
}

fn print_report(args: &Args, result: AuditResult) {
    println!("\n--- Digital Hoarder Audit Report ---");
    println!("Target Path: {}", args.path.display());
    println!("Total Files Scanned: {}", result.file_count);
    println!("Total Size: {}", format_size(result.total_size, DECIMAL));

    println!("\n--- Summary by File Extension ---");
    let mut sorted_extensions: Vec<_> = result.extension_summary.into_iter().collect();
    sorted_extensions.sort_unstable_by(|a, b| b.1.0.cmp(&a.1.0)); // Sort by total size descending

    for (ext, (size, count)) in sorted_extensions {
        println!("  .{:<10} | Files: {:<8} | Size: {}", ext, count, format_size(size, DECIMAL));
    }

    if args.verbose {
        if !result.largest_files.is_empty() {
            println!("\n--- Top {} Largest Files (Min Size: {}) ---", args.top_n, args.min_size.map_or("0B".to_string(), |s| format_size(s, DECIMAL)));
            for (path, size) in result.largest_files {
                println!("  {} | {}", format_size(size, DECIMAL), path.display());
            }
        } else {
            println!("\n--- No files met the verbose criteria (min size or extension filter). ---");
        }
    }

    if !result.largest_dirs.is_empty() {
        println!("\n--- Top {} Largest Directories ---", args.top_n);
        for (path, size) in result.largest_dirs {
            println!("  {} | {}", format_size(size, DECIMAL), path.display());
        }
    }

    println!("\n--- End of Report ---");
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.path.exists() {
        return Err(format!("Error: Path '{}' does not exist.", args.path.display()).into());
    }
    if !args.path.is_dir() {
        return Err(format!("Error: Path '{}' is not a directory.", args.path.display()).into());
    }

    let result = run_audit(&args)?;
    print_report(&args, result);

    Ok(())
}
