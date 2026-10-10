use clap::{Parser, Subcommand};
use std::{
    collections::HashMap,
    fs,
    io::{self, Write},
    path::{Path, PathBuf},
};
use walkdir::WalkDir;
use sha2::{Digest, Sha256};
use serde::{Serialize, Deserialize};

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Cli {
    #[clap(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Creates a temporal echo snapshot of the specified directory.
    Snapshot {
        /// The directory to snapshot.
        #[clap(parse(from_os_str))] // Use parse(from_os_str) for PathBuf arguments
        path: PathBuf,
        /// Output file for the snapshot (default: .echo_snapshot.json).
        #[clap(short, long, parse(from_os_str), default_value = ".echo_snapshot.json")]
        output: PathBuf,
    },
    /// Compares the current state of the specified directory against a temporal echo snapshot.
    Compare {
        /// The directory to compare.
        #[clap(parse(from_os_str))] // Use parse(from_os_str) for PathBuf arguments
        path: PathBuf,
        /// Input snapshot file (default: .echo_snapshot.json).
        #[clap(short, long, parse(from_os_str), default_value = ".echo_snapshot.json")]
        input: PathBuf,
    },
}

#[derive(Serialize, Deserialize, Debug, PartialEq)]
struct FileEntry {
    hash: String,
    size: u64,
}

#[derive(Serialize, Deserialize, Debug, PartialEq)]
struct Snapshot {
    #[serde(flatten)]
    files: HashMap<PathBuf, FileEntry>,
}

fn calculate_file_hash(path: &Path) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    io::copy(&mut file, &mut hasher)?;
    Ok(format!("{:x}", hasher.finalize()))
}

// Internal function to create a snapshot, returning the Snapshot struct
fn create_snapshot_internal(dir_path: &Path) -> io::Result<Snapshot> {
    let mut snapshot_files = HashMap::new();
    let base_path = dir_path.canonicalize()?;

    for entry in WalkDir::new(dir_path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            let relative_path = path.strip_prefix(&base_path)
                .map_err(|e| io::Error::new(io::ErrorKind::InvalidInput, e.to_string()))?
                .to_path_buf();
            let hash = calculate_file_hash(path)?;
            let metadata = fs::metadata(path)?;
            snapshot_files.insert(relative_path, FileEntry { hash, size: metadata.len() });
        }
    }
    Ok(Snapshot { files: snapshot_files })
}

// CLI-facing function for snapshot creation
fn create_snapshot_cli(dir_path: &Path, output_path: &Path) -> io::Result<()> {
    let snapshot = create_snapshot_internal(dir_path)?;
    let json = serde_json::to_string_pretty(&snapshot)?;
    fs::write(output_path, json)?;
    println!("Snapshot created successfully at {:?}", output_path);
    Ok(())
}

#[derive(Debug, PartialEq)]
enum ChangeType {
    New,
    Modified,
    Deleted,
}

#[derive(Debug)]
struct DetectedChange {
    change_type: ChangeType,
    path: PathBuf,
}

// Internal function to compare snapshots, returning a vector of changes
fn compare_snapshot_internal(old_snapshot: &Snapshot, new_snapshot: &Snapshot) -> Vec<DetectedChange> {
    let mut changes = Vec::new();

    // Check for modified or deleted files
    for (path, old_entry) in &old_snapshot.files {
        if let Some(new_entry) = new_snapshot.files.get(path) {
            if old_entry != new_entry {
                changes.push(DetectedChange {
                    change_type: ChangeType::Modified,
                    path: path.clone(),
                });
            }
        } else {
            changes.push(DetectedChange {
                change_type: ChangeType::Deleted,
                path: path.clone(),
            });
        }
    }

    // Check for new files
    for (path, _new_entry) in &new_snapshot.files {
        if !old_snapshot.files.contains_key(path) {
            changes.push(DetectedChange {
                change_type: ChangeType::New,
                path: path.clone(),
            });
        }
    }
    changes
}

// CLI-facing function for snapshot comparison
fn compare_snapshot_cli(dir_path: &Path, input_path: &Path) -> io::Result<()> {
    let snapshot_json = fs::read_to_string(input_path)?;
    let old_snapshot: Snapshot = serde_json::from_str(&snapshot_json)?;

    let new_snapshot = create_snapshot_internal(dir_path)?;
    let changes = compare_snapshot_internal(&old_snapshot, &new_snapshot);

    if changes.is_empty() {
        println!("No temporal distortions detected. All files are in sync with the echo.");
    } else {
        println!("Temporal distortions detected!");
        for change in changes {
            match change.change_type {
                ChangeType::New => println!("NEW: {:?}", change.path),
                ChangeType::Modified => println!("MODIFIED: {:?}", change.path),
                ChangeType::Deleted => println!("DELETED: {:?}", change.path),
            }
        }
    }
    Ok(())
}

fn main() -> io::Result<()> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Snapshot { path, output } => create_snapshot_cli(path, output),
        Commands::Compare { path, input } => compare_snapshot_cli(path, input),
    }
}
