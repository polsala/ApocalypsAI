use clap::{Parser, Subcommand};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::{HashMap, HashSet};
use std::fs;
use std::io::{self, BufRead};
use std::path::{Path, PathBuf};

#[derive(Parser, Debug)]
#[command(author, version, about = "Chrono-Shard Indexer: Index, search, and deduplicate fragmented text files.", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Indexes all text files in a directory and its subdirectories
    Index {
        /// The directory to scan for chrono-shards. Defaults to current directory.
        #[arg(default_value = ".")]
        path: PathBuf,
        /// Custom output path for the index file. Defaults to .chrono_index.json in the scanned directory.
        #[arg(short, long, default_value = ".chrono_index.json")]
        output: PathBuf,
    },
    /// Searches the index for shards containing a keyword
    Search {
        /// The keyword to search for in chrono-shards
        keyword: String,
        /// Path to the index file. Defaults to .chrono_index.json in the current directory.
        #[arg(short, long, default_value = ".chrono_index.json")]
        index: PathBuf,
    },
    /// Finds and lists duplicate shards based on content hash
    Deduplicate {
        /// Path to the index file. Defaults to .chrono_index.json in the current directory.
        #[arg(short, long, default_value = ".chrono_index.json")]
        index: PathBuf,
        /// Delete all but one instance of each duplicate file (USE WITH CAUTION!)
        #[arg(short, long)]
        delete: bool,
    },
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct ShardEntry {
    path: PathBuf,
    hash: String,
    first_line_snippet: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Index { path, output } => index_shards(path, output)?,
        Commands::Search { keyword, index } => search_shards(keyword, index)?,
        Commands::Deduplicate { index, delete } => deduplicate_shards(index, *delete)?,
    }

    Ok(())
}

fn index_shards(dir_path: &Path, output_path: &Path) -> Result<(), Box<dyn std::error::Error>> {
    println!("Indexing chrono-shards in: {}", dir_path.display());
    let mut shards = Vec::new();

    for entry in walkdir::WalkDir::new(dir_path) {
        let entry = entry?;
        let path = entry.path();

        if path.is_file() {
            // Basic check for text files, could be improved with MIME type detection
            if let Some(extension) = path.extension() {
                if !["txt", "log", "md", "json", "toml", "yaml", "conf", "ini", "csv", "xml", "html", "css", "js", "rs", "py", "go", "sh"].contains(&extension.to_str().unwrap_or("")) {
                    continue; // Skip non-text-like files for simplicity
                }
            }

            let content = fs::read(path)?;
            let hash = format!("{:x}", Sha256::digest(&content));

            let first_line_snippet = if let Ok(content_str) = String::from_utf8(content) {
                content_str.lines().next().unwrap_or("").to_string()
            } else {
                "[Binary or non-UTF8 content]".to_string()
            };

            shards.push(ShardEntry {
                path: path.to_path_buf(),
                hash,
                first_line_snippet,
            });
        }
    }

    let index_json = serde_json::to_string_pretty(&shards)?;
    fs::write(output_path, index_json)?;

    println!("Indexed {} shards to {}", shards.len(), output_path.display());
    Ok(())
}

fn load_index(index_path: &Path) -> Result<Vec<ShardEntry>, Box<dyn std::error::Error>> {
    let index_content = fs::read_to_string(index_path)?;
    let shards: Vec<ShardEntry> = serde_json::from_str(&index_content)?;
    Ok(shards)
}

fn search_shards(keyword: &str, index_path: &Path) -> Result<(), Box<dyn std::error::Error>> {
    println!("Searching for '{}' in index: {}", keyword, index_path.display());
    let shards = load_index(index_path)?;
    let keyword_lower = keyword.to_lowercase();

    let mut found_count = 0;
    for shard in shards {
        // Read the full file content for a more accurate search
        if let Ok(content) = fs::read_to_string(&shard.path) {
            if content.to_lowercase().contains(&keyword_lower) {
                println!("Found in: {}", shard.path.display());
                println!("  Snippet: {}", shard.first_line_snippet);
                found_count += 1;
            }
        }
    }

    println!("Found {} shards matching '{}'.", found_count, keyword);
    Ok(())
}

fn deduplicate_shards(index_path: &Path, delete: bool) -> Result<(), Box<dyn std::error::Error>> {
    println!("Checking for duplicate shards in index: {}", index_path.display());
    let shards = load_index(index_path)?;

    let mut hash_to_paths: HashMap<String, Vec<PathBuf>> = HashMap::new();
    for shard in shards {
        hash_to_paths.entry(shard.hash).or_insert_with(Vec::new).push(shard.path);
    }

    let mut duplicates_found = 0;
    for (hash, paths) in hash_to_paths {
        if paths.len() > 1 {
            duplicates_found += paths.len() - 1;
            println!("\nDuplicate content (Hash: {}):
  Original: {}", hash, paths[0].display());
            for i in 1..paths.len() {
                println!("  Duplicate: {}", paths[i].display());
                if delete {
                    fs::remove_file(&paths[i])?;
                    println!("    -> Deleted: {}", paths[i].display());
                }
            }
        }
    }

    if duplicates_found == 0 {
        println!("No duplicate shards found.");
    } else {
        println!("Found {} duplicate shards.", duplicates_found);
        if delete {
            println!("Deleted {} duplicate files.", duplicates_found);
            // Re-index after deletion to update the index file
            let parent_dir = index_path.parent().unwrap_or_else(|| Path::new("."));
            index_shards(parent_dir, index_path)?;
        }
    }

    Ok(())
}
