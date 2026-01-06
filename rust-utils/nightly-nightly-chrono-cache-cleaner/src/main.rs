use clap::Parser;
use std::path::PathBuf;
use nightly_chrono_cache_cleaner::find_stale_files; // Import from our lib

#[derive(Parser, Debug)]
#[clap(author, version, about = "Nightly Chrono-Cache Cleaner: Defragments digital detritus based on temporal echoes.", long_about = None)]
struct Args {
    /// Path to scan for digital detritus
    #[clap(short, long, default_value = ".")]
    path: PathBuf,

    /// Minimum age in days for a file to be considered stale (default: 90 days)
    #[clap(short, long, default_value_t = 90)]
    stale_days: u64,

    /// Do not actually suggest files, just print summary
    #[clap(short, long)]
    dry_run: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    println!("Scanning for temporal echoes in: {}", args.path.display());
    println!("Considering files older than {} days as stale.", args.stale_days);
    if args.dry_run {
        println!("(Dry run mode: no suggestions will be made, only summary)");
    }

    let stale_files = find_stale_files(&args.path, args.stale_days)?;

    if stale_files.is_empty() {
        println!("\n✨ The digital realm is pristine! No significant temporal echoes found.");
    } else {
        println!("\n🌌 The Chrono-Cache Cleaner whispers these files might be ready for the void:");
        for file_path in stale_files {
            println!("  - {}", file_path.display());
        }
        if !args.dry_run {
            println!("\nConsider reviewing these files for potential cleanup. Use `rm` with caution!");
        } else {
            println!("\n(This was a dry run. To get actual suggestions, remove the --dry-run flag.)");
        }
    }

    Ok(())
}
