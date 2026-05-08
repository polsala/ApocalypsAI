use clap::{Parser, Subcommand};
use std::path::{Path, PathBuf};
use std::fs;
use std::time::{SystemTime, Duration};
use chrono::{Utc, DateTime};
use flate2::write::GzEncoder;
use flate2::Compression;
use tar::Builder;

#[derive(Parser, Debug)]
#[command(author, version, about = "Cosmic Dust Collector: Identify, analyze, and archive ephemeral system files.", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Scans a directory for 'cosmic dust' (old/large ephemeral files).
    Scan {
        /// Path to scan for cosmic dust.
        #[arg(short, long, default_value = ".")]
        path: PathBuf,

        /// Files older than this many days are considered dust.
        #[arg(short, long, default_value_t = 30)]
        age: u64,

        /// Files larger than this many megabytes are considered dust.
        #[arg(short, long, default_value_t = 10)]
        size_mb: u64,
    },
    /// Collects identified 'cosmic dust' into a stardust archive.
    Collect {
        /// Path to scan for cosmic dust.
        #[arg(short, long, default_value = ".")]
        path: PathBuf,

        /// Files older than this many days are considered dust.
        #[arg(short, long, default_value_t = 30)]
        age: u64,

        /// Files larger than this many megabytes are considered dust.
        #[arg(short, long, default_value_t = 10)]
        size_mb: u64,

        /// Output path for the stardust archive (e.g., dust_archive.tar.gz).
        #[arg(short, long)]
        output: PathBuf,
    },
}

#[derive(Debug)]
struct DustParticle {
    path: PathBuf,
    size: u64,
    modified: SystemTime,
}

pub trait DurationExt {
    fn from_days(days: u64) -> Self;
}

impl DurationExt for Duration {
    fn from_days(days: u64) -> Self {
        Duration::from_secs(days * 24 * 60 * 60)
    }
}

fn is_dust(entry: &fs::DirEntry, max_age_days: u64, min_size_bytes: u64) -> Option<DustParticle> {
    let metadata = entry.metadata().ok()?;
    if !metadata.is_file() {
        return None;
    }

    let modified_time = metadata.modified().ok()?;
    let now = SystemTime::now();
    let age = now.duration_since(modified_time).ok()?;

    let max_age_duration = DurationExt::from_days(max_age_days);

    if age > max_age_duration && metadata.len() >= min_size_bytes {
        Some(DustParticle {
            path: entry.path(),
            size: metadata.len(),
            modified: modified_time,
        })
    } else {
        None
    }
}

fn scan_for_dust_in_path(
    root_path: &Path,
    max_age_days: u64,
    min_size_bytes: u64,
) -> Vec<DustParticle> {
    let mut dust_particles = Vec::new();
    if let Ok(entries) = fs::read_dir(root_path) {
        for entry in entries.filter_map(|e| e.ok()) {
            if let Some(particle) = is_dust(&entry, max_age_days, min_size_bytes) {
                dust_particles.push(particle);
            }
        }
    }
    dust_particles
}

fn collect_dust_to_archive(
    dust_particles: &[DustParticle],
    output_path: &Path,
    root_path: &Path,
) -> Result<(), Box<dyn std::error::Error>> {
    let file = fs::File::create(output_path)?;
    let encoder = GzEncoder::new(file, Compression::default());
    let mut tar = Builder::new(encoder);

    for particle in dust_particles {
        let relative_path = particle.path.strip_prefix(root_path)?;
        tar.append_path_with_name(&particle.path, relative_path)?; // Append with relative path inside archive
    }

    tar.finish()?;
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Scan { path, age, size_mb } => {
            let min_size_bytes = size_mb * 1024 * 1024;
            println!("Scanning '{}' for cosmic dust (older than {} days, larger than {} MB)...",
                     path.display(), age, size_mb);

            let dust_particles = scan_for_dust_in_path(&path, age, min_size_bytes);

            if dust_particles.is_empty() {
                println!("No cosmic dust detected. Your system is sparkling clean!");
            } else {
                println!("Cosmic dust detected:");
                for particle in dust_particles {
                    let modified_dt: DateTime<Utc> = particle.modified.into();
                    println!(
                        "- {} ({} bytes, last modified: {})",
                        particle.path.display(),
                        particle.size,
                        modified_dt.format("%Y-%m-%d %H:%M:%S UTC")
                    );
                }
            }
        }
        Commands::Collect { path, age, size_mb, output } => {
            let min_size_bytes = size_mb * 1024 * 1024;
            println!("Scanning '{}' for cosmic dust (older than {} days, larger than {} MB) for collection...",
                     path.display(), age, size_mb);

            let dust_particles = scan_for_dust_in_path(&path, age, min_size_bytes);

            if dust_particles.is_empty() {
                println!("No cosmic dust detected. Nothing to collect.");
            } else {
                println!("Collecting {} cosmic dust particles into '{}'...", dust_particles.len(), output.display());
                collect_dust_to_archive(&dust_particles, &output, &path)?;
                println!("Stardust archive created successfully at '{}'.", output.display());
            }
        }
    }
    Ok(())
}
