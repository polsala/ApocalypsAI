use clap::{Parser, Subcommand};
use std::path::PathBuf;
use std::process;
use nightly_reality_anchor::{calculate_file_hash, store_anchor, load_anchor, get_anchor_path};

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance CLI tool to calculate and verify 'reality anchors' (SHA256 hashes) for files, ensuring their temporal stability.", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Calculate and store a reality anchor for a file.
    Anchor {
        /// The path to the file to anchor.
        file: PathBuf,
    },
    /// Verify a file against its stored reality anchor.
    Verify {
        /// The path to the file to verify.
        file: PathBuf,
    },
    /// Calculate and print a file's reality anchor without storing it.
    Check {
        /// The path to the file to check.
        file: PathBuf,
    },
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Anchor { file } => {
            if !file.exists() {
                eprintln!("Error: File not found at {:?}", file);
                process::exit(1);
            }
            let hash = calculate_file_hash(file)?;
            store_anchor(file, &hash)?;
            println!("Reality anchor created for {:?}: {}", file, hash);
        }
        Commands::Verify { file } => {
            if !file.exists() {
                eprintln!("Error: File not found at {:?}", file);
                process::exit(1);
            }
            let stored_hash = match load_anchor(file) {
                Ok(h) => h,
                Err(e) => {
                    eprintln!("Error loading anchor for {:?}: {}", file, e);
                    process::exit(1);
                }
            };
            let current_hash = calculate_file_hash(file)?;

            if stored_hash.trim() == current_hash {
                println!("Reality check PASSED for {:?}. Anchor is stable.", file);
            } else {
                println!("Reality check FAILED for {:?}. Temporal drift detected!", file);
                println!("  Stored anchor: {}", stored_hash.trim());
                println!("  Current reality: {}", current_hash);
                process::exit(1);
            }
        }
        Commands::Check { file } => {
            if !file.exists() {
                eprintln!("Error: File not found at {:?}", file);
                process::exit(1);
            }
            let hash = calculate_file_hash(file)?;
            println!("Current reality anchor for {:?}: {}", file, hash);
        }
    }
    Ok(())
}
