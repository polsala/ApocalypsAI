use clap::Parser;
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance Rust CLI tool to identify and optionally remove files older than a specified duration.", long_about = None)]
pub struct Cli {
    /// The directory to scan for decayed files
    pub path: PathBuf,

    /// Files older than this duration will be considered for scrubbing (e.g., "30d", "1w", "2y")
    #[arg(short = 'd', long, default_value = "30d")]
    pub duration: String,

    /// Exclude files or directories matching this glob pattern (can be specified multiple times)
    #[arg(short = 'x', long)]
    pub exclude: Vec<String>,

    /// Only list files that would be scrubbed, do not delete them
    #[arg(short = 'n', long)]
    pub dry_run: bool,

    /// Skip interactive confirmation when deleting files
    #[arg(short = 'f', long)]
    pub force: bool,

    /// Enable verbose output
    #[arg(short = 'v', long)]
    pub verbose: bool,
}
