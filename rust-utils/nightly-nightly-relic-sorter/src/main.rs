use clap::Parser;
use walkdir::WalkDir;
use std::path::PathBuf;
use std::fs;
use std::io::Read;
use std::collections::HashMap;

#[derive(Parser, Debug)]
#[command(author, version, about = "Categorizes scavenged files into whimsical 'relic' types.", long_about = None)]
struct Args {
    /// The directory to scan for relics
    #[arg(short, long, value_name = "PATH")]
    path: PathBuf,

    /// Be verbose, showing each file's path and detected type
    #[arg(short, long)]
    verbose: bool,
}

#[derive(Debug, Hash, PartialEq, Eq)]
enum RelicCategory {
    AncientScrolls,
    VisualGlyphs,
    SonicEchoes,
    MovingIllusions,
    BundledSecrets,
    ForbiddenRunes,
    DigitalArtifacts,
    UnidentifiedRelic,
}

impl RelicCategory {
    fn name(&self) -> &str {
        match self {
            RelicCategory::AncientScrolls => "Ancient Scrolls (Text)",
            RelicCategory::VisualGlyphs => "Visual Glyphs (Image)",
            RelicCategory::SonicEchoes => "Sonic Echoes (Audio)",
            RelicCategory::MovingIllusions => "Moving Illusions (Video)",
            RelicCategory::BundledSecrets => "Bundled Secrets (Archive)",
            RelicCategory::ForbiddenRunes => "Forbidden Runes (Executable/Script)",
            RelicCategory::DigitalArtifacts => "Digital Artifacts (Data/Code)",
            RelicCategory::UnidentifiedRelic => "Unidentified Relic",
        }
    }
}

fn classify_file(path: &PathBuf) -> RelicCategory {
    if path.is_dir() {
        return RelicCategory::UnidentifiedRelic;
    }

    let mut buffer = Vec::new();
    // Read up to 4KB for infer, or less if file is smaller
    if let Ok(mut file) = fs::File::open(path) {
        file.take(4096).read_to_end(&mut buffer).ok();
    }

    if !buffer.is_empty() {
        if let Some(kind) = infer::get(&buffer) {
            match kind.mime_type() {
                t if t.starts_with("text/") => return RelicCategory::AncientScrolls,
                t if t.starts_with("image/") => return RelicCategory::VisualGlyphs,
                t if t.starts_with("audio/") => return RelicCategory::SonicEchoes,
                t if t.starts_with("video/") => return RelicCategory::MovingIllusions,
                t if t.starts_with("application/zip") || t.starts_with("application/x-tar") || t.starts_with("application/gzip") || t.starts_with("application/vnd.rar") || t.starts_with("application/x-7z-compressed") => return RelicCategory::BundledSecrets,
                t if t.starts_with("application/x-executable") || t.starts_with("application/x-sh") || t.starts_with("application/x-msdownload") => return RelicCategory::ForbiddenRunes,
                t if t.starts_with("application/json") || t.starts_with("application/xml") || t.starts_with("application/yaml") || t.starts_with("application/sql") => return RelicCategory::DigitalArtifacts,
                _ => {}
            }
        }
    }

    // Fallback to extension-based classification if infer fails or doesn't match
    if let Some(ext) = path.extension().and_then(|s| s.to_str()) {
        match ext.to_lowercase().as_str() {
            "txt" | "md" | "log" => RelicCategory::AncientScrolls,
            "jpg" | "jpeg" | "png" | "gif" | "bmp" | "svg" | "webp" => RelicCategory::VisualGlyphs,
            "mp3" | "wav" | "ogg" | "flac" | "aac" => RelicCategory::SonicEchoes,
            "mp4" | "avi" | "mov" | "mkv" | "webm" => RelicCategory::MovingIllusions,
            "zip" | "tar" | "gz" | "rar" | "7z" => RelicCategory::BundledSecrets,
            "exe" | "sh" | "bat" | "bin" | "py" | "js" | "rb" | "go" | "rs" | "java" | "cpp" | "c" | "h" => RelicCategory::ForbiddenRunes,
            "json" | "csv" | "xml" | "yaml" | "yml" | "toml" | "ini" | "sql" => RelicCategory::DigitalArtifacts,
            _ => RelicCategory::UnidentifiedRelic,
        }
    } else {
        RelicCategory::UnidentifiedRelic
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.path.exists() {
        eprintln!("Error: Path '{}' does not exist.", args.path.display());
        std::process::exit(1);
    }
    if !args.path.is_dir() {
        eprintln!("Error: Path '{}' is not a directory.", args.path.display());
        std::process::exit(1);
    }

    println!("Scanning for relics in: {}", args.path.display());
    println!("------------------------------------");

    let mut categories: HashMap<RelicCategory, Vec<PathBuf>> = HashMap::new();

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path().to_path_buf();
        if path.is_file() {
            let category = classify_file(&path);
            if args.verbose {
                println!("  {} -> {}", path.display(), category.name());
            }
            categories.entry(category).or_default().push(path);
        }
    }

    println!("\nRelic Manifest:");
    println!("------------------------------------");
    let mut sorted_categories: Vec<_> = categories.iter().collect();
    sorted_categories.sort_by_key(|(cat, _)| cat.name());

    for (category, files) in sorted_categories {
        println!("{}: {} relics found", category.name(), files.len());
        for file in files {
            println!("  - {}", file.display());
        }
    }

    Ok(())
}
