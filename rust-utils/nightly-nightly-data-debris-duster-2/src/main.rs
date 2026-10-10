use clap::Parser;
use std::path::PathBuf;
use std::io;
use nightly_data_debris_duster::{find_duplicate_files};

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Directory to scan for duplicate files
    #[arg(short, long)]
    path: PathBuf,
}

fn main() -> io::Result<()> {
    let args = Args::parse();
    let target_path = args.path;

    println!("Scanning '{}' for data debris...", target_path.display());

    match find_duplicate_files(&target_path) {
        Ok(duplicates) => {
            if duplicates.is_empty() {
                println!("\nNo duplicate data debris found. Your digital wasteland is pristine!");
            } else {
                for (hash, paths) in duplicates {
                    println!("\n--- Duplicate Debris (Hash: {}) ---", hash);
                    for p in paths {
                        println!("  - {}", p.display());
                    }
                }
                println!("\nDusting complete! Consider clearing this debris to reclaim space.");
            }
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }

    Ok(())
}
