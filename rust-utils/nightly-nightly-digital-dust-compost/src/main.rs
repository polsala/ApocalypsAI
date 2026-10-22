use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use humantime::format_duration;

#[derive(Parser, Debug)]
#[clap(
    author = "ApocalypsAI Nightly Integrator",
    version = "1.0",
    about = "Identify and 'compost' (delete) old, unused files, categorizing them as 'digital dust bunnies'."
)]
struct Args {
    /// The directory to scan for digital dust bunnies.
    path: PathBuf,

    /// Minimum age in days for a file to be considered a 'dust bunny'. Files older than this will be considered. Default is 30 days.
    #[clap(short = 'a', long, default_value = "30")]
    age: u64,

    /// Actually delete the identified files. Use with caution!
    #[clap(short = 'd', long)]
    delete: bool,

    /// Show individual files in each category.
    #[clap(short = 'v', long)]
    verbose: bool,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
enum DustCategory {
    FreshSprouts,   // < 7 days
    WiltingLeaves,  // 7-30 days
    AncientCompost, // 30-90 days
    PetrifiedRelics, // > 90 days
}

impl DustCategory {
    fn from_age_days(age_days: u64) -> Self {
        if age_days < 7 {
            DustCategory::FreshSprouts
        } else if age_days < 30 {
            DustCategory::WiltingLeaves
        } else if age_days < 90 {
            DustCategory::AncientCompost
        } else {
            DustCategory::PetrifiedRelics
        }
    }

    fn display_name(&self) -> &str {
        match self {
            DustCategory::FreshSprouts => "Fresh Sprouts",
            DustCategory::WiltingLeaves => "Wilting Leaves",
            DustCategory::AncientCompost => "Ancient Compost",
            DustCategory::PetrifiedRelics => "Petrified Relics",
        }
    }
}

struct DustBunny {
    path: PathBuf,
    size: u64,
    modified: SystemTime,
    age_days: u64,
    category: DustCategory,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.path.is_dir() {
        eprintln!("Error: Provided path is not a directory: {}", args.path.display());
        std::process::exit(1);
    }

    println!("\nScanning '{}' for digital dust bunnies older than {} days...\n", args.path.display(), args.age);

    let mut dust_bunnies: Vec<DustBunny> = Vec::new();
    let now = SystemTime::now();

    for entry in walkdir::WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                if let Ok(modified) = metadata.modified() {
                    let duration_since_modified = now.duration_since(modified).unwrap_or_else(|_| Duration::new(0,0)); // Handle future times gracefully
                    let age_days = duration_since_modified.as_secs() / (24 * 3600);

                    if age_days >= args.age {
                        dust_bunnies.push(DustBunny {
                            path: path.to_path_buf(),
                            size: metadata.len(),
                            modified,
                            age_days,
                            category: DustCategory::from_age_days(age_days),
                        });
                    }
                }
            }
        }
    }

    dust_bunnies.sort_by(|a, b| a.category.cmp(&b.category).then_with(|| a.age_days.cmp(&b.age_days)));

    if dust_bunnies.is_empty() {
        println!("No digital dust bunnies found older than {} days. Your digital garden is pristine!\n", args.age);
        return Ok(());
    }

    let mut total_size_all_categories = 0;
    let mut current_category: Option<&DustCategory> = None;

    for bunny in &dust_bunnies {
        if current_category.map_or(true, |cat| cat != &bunny.category) {
            if current_category.is_some() {
                println!("----------------------------------------");
            }
            println!("\n--- {} ---", bunny.category.display_name());
            current_category = Some(&bunny.category);
        }

        total_size_all_categories += bunny.size;

        if args.verbose {
            let duration = now.duration_since(bunny.modified).unwrap_or_else(|_| Duration::new(0,0));
            println!("  - {} ({} ago, {})", bunny.path.display(), format_duration(duration).to_string(), bytes_to_human_readable(bunny.size));
        }
    }

    println!("\n--- Summary ---");
    println!("Total digital dust bunnies found: {}", dust_bunnies.len());
    println!("Total size to compost: {}", bytes_to_human_readable(total_size_all_categories));

    if args.delete {
        println!("\nInitiating composting process... (deleting files)\n");
        for bunny in dust_bunnies {
            match fs::remove_file(&bunny.path) {
                Ok(_) => println!("  Composted: {}", bunny.path.display()),
                Err(e) => eprintln!("  Failed to compost {}: {}", bunny.path.display(), e),
            }
        }
        println!("\nComposting complete! Your digital garden is refreshed.\n");
    } else {
        println!("\nTo compost these digital dust bunnies, run with the `--delete` flag.\n");
    }

    Ok(())
}

fn bytes_to_human_readable(bytes: u64) -> String {
    const KIB: u64 = 1024;
    const MIB: u64 = KIB * 1024;
    const GIB: u64 = MIB * 1024;

    if bytes < KIB {
        format!("{} B", bytes)
    } else if bytes < MIB {
        format!("{:.2} KiB", bytes as f64 / KIB as f64)
    } else if bytes < GIB {
        format!("{:.2} MiB", bytes as f64 / MIB as f64)
    } else {
        format!("{:.2} GiB", bytes as f64 / GIB as f64)
    }
}
