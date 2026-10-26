use clap::Parser;
use walkdir::WalkDir;
use std::path::PathBuf;
use std::fs;
use bytesize::ByteSize;

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance CLI tool that scans specified directories for small, forgotten 'cosmic dust' files and offers to delete them.", long_about = None)]
struct Args {
    /// Directory to scan for cosmic dust
    #[arg(short, long, default_value = ".")]
    path: PathBuf,

    /// Maximum file size to consider as 'cosmic dust' (e.g., 1KB, 10MB)
    #[arg(short, long, default_value = "1KB")]
    max_size: String,

    /// Perform a dry run without deleting any files
    #[arg(short, long)]
    dry_run: bool,

    /// Delete the identified cosmic dust files (requires confirmation)
    #[arg(short, long)]
    delete: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let max_size_bytes = ByteSize::from_str(&args.max_size)
        .map_err(|e| format!("Invalid max_size format: {}", e))?
        .as_u64();

    println!("Scanning '{}' for files smaller than {}...", args.path.display(), ByteSize(max_size_bytes));

    let mut dust_files = Vec::new();

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        if entry.file_type().is_file() {
            if let Ok(metadata) = entry.metadata() {
                if metadata.len() < max_size_bytes {
                    dust_files.push((entry.path().to_path_buf(), metadata.len()));
                }
            }
        }
    }

    if dust_files.is_empty() {
        println!("No cosmic dust found in '{}'. Your digital space is pristine!", args.path.display());
        return Ok(());
    }

    println!("\n--- Cosmic Dust Report ---");
    for (path, size) in &dust_files {
        println!("- {} ({}B)", path.display(), size);
    }
    println!("--------------------------");
    println!("Total cosmic dust files found: {}", dust_files.len());
    println!("Total size of cosmic dust: {}", ByteSize(dust_files.iter().map(|(_, s)| s).sum()));

    if args.dry_run {
        println!("\nDry run complete. No files were deleted.");
    } else if args.delete {
        println!("\nWARNING: You are about to delete {} cosmic dust files.", dust_files.len());
        println!("This action cannot be undone. Do you wish to proceed? (yes/no)");

        let mut confirmation = String::new();
        std::io::stdin().read_line(&mut confirmation)?;

        if confirmation.trim().to_lowercase() == "yes" {
            let mut deleted_count = 0;
            let mut deleted_size = 0;
            for (path, size) in dust_files {
                match fs::remove_file(&path) {
                    Ok(_) => {
                        println!("Deleted: {}", path.display());
                        deleted_count += 1;
                        deleted_size += size;
                    }
                    Err(e) => {
                        eprintln!("Error deleting {}: {}", path.display(), e);
                    }
                }
            }
            println!("\nSuccessfully deleted {} files, freeing up {}.", deleted_count, ByteSize(deleted_size));
        } else {
            println!("Deletion cancelled. Cosmic dust remains.");
        }
    } else {
        println!("\nTo delete these files, run with the --delete flag.");
        println!("To perform a dry run, use the --dry-run flag.");
    }

    Ok(())
}
