use clap::Parser;
use walkdir::WalkDir;
use std::time::{SystemTime, Duration};
use std::path::PathBuf;
use humantime::parse_duration;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Map file system 'echoes' by modification time.", long_about = None)]
struct Args {
    /// Path to scan for echoes (default: current directory)
    #[clap(short, long, value_parser, default_value = ".")]
    path: PathBuf,

    /// List files modified within this duration (e.g., "1h", "7d")
    #[clap(long, value_parser)]
    fresh: Option<String>,

    /// List files not modified for at least this duration (e.g., "30d", "2w")
    #[clap(long, value_parser)]
    stale: Option<String>,

    /// Maximum depth to traverse directories (0 for current dir only, 1 for current + direct children)
    #[clap(long, value_parser, default_value_t = usize::MAX)]
    max_depth: usize,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let now = SystemTime::now();
    let mut fresh_duration: Option<Duration> = None;
    let mut stale_duration: Option<Duration> = None;

    if let Some(d_str) = args.fresh {
        fresh_duration = Some(parse_duration(&d_str)?);
    }
    if let Some(d_str) = args.stale {
        stale_duration = Some(parse_duration(&d_str)?);
    }

    if fresh_duration.is_none() && stale_duration.is_none() {
        eprintln!("Error: Either --fresh or --stale duration must be specified.");
        std::process::exit(1);
    }
    if fresh_duration.is_some() && stale_duration.is_some() {
        eprintln!("Error: Cannot specify both --fresh and --stale.");
        std::process::exit(1);
    }

    for entry in WalkDir::new(&args.path)
        .max_depth(args.max_depth)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = path.metadata() {
                if let Ok(modified_time) = metadata.modified() {
                    let age = now.duration_since(modified_time).unwrap_or_default();

                    if let Some(fresh_d) = fresh_duration {
                        if age <= fresh_d {
                            println!("{}", path.display());
                        }
                    } else if let Some(stale_d) = stale_duration {
                        if age >= stale_d {
                            println!("{}", path.display());
                        }
                    }
                }
            }
        }
    }

    Ok(())
}
