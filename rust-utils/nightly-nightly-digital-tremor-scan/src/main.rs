use clap::{Parser, Subcommand};
use serde::{Serialize, Deserialize};
use std::{
    collections::HashMap,
    fs,
    path::{Path, PathBuf},
    time::SystemTime,
};
use chrono::{DateTime, Utc};

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Creates a baseline snapshot of a directory's file system metadata.
    Snapshot {
        /// The directory to snapshot.
        #[arg(short, long)]
        path: PathBuf,
        /// Output file for the snapshot (JSON format).
        #[arg(short, long)]
        output: PathBuf,
    },
    /// Detects "tremors" (metadata changes, new/missing files) by comparing current state to a snapshot.
    Detect {
        /// The directory to scan for tremors.
        #[arg(short, long)]
        path: PathBuf,
        /// Input snapshot file (JSON format) to compare against.
        #[arg(short, long)]
        snapshot: PathBuf,
    },
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq)]
enum FileType {
    File,
    Dir,
    Symlink,
    Other,
}

#[derive(Serialize, Deserialize, Debug, PartialEq, Eq)]
struct FileMetadata {
    path: String,
    file_type: FileType,
    size: u64,
    modified: DateTime<Utc>,
    accessed: DateTime<Utc>,
    permissions: u32, // Storing as u32 for simplicity, e.g., octal representation
}

impl FileMetadata {
    fn from_path(base_path: &Path, entry_path: &Path) -> Result<Self, std::io::Error> {
        let metadata = fs::metadata(entry_path)?;
        let relative_path = entry_path.strip_prefix(base_path).unwrap_or(entry_path);

        let file_type = if metadata.is_file() {
            FileType::File
        } else if metadata.is_dir() {
            FileType::Dir
        } else if metadata.is_symlink() {
            FileType::Symlink
        } else {
            FileType::Other
        };

        let modified: DateTime<Utc> = metadata.modified()?.into();
        let accessed: DateTime<Utc> = metadata.accessed()?.into();

        // Permissions: Convert to a u32. On Unix, this is straightforward.
        // On non-Unix systems, we use a placeholder as permissions are handled differently.
        #[cfg(unix)]
        let permissions = {
            use std::os::unix::fs::PermissionsExt;
            metadata.permissions().mode()
        };
        #[cfg(not(unix))]
        let permissions = 0; // Placeholder for non-Unix systems

        Ok(FileMetadata {
            path: relative_path.to_string_lossy().into_owned(),
            file_type,
            size: metadata.len(),
            modified,
            accessed,
            permissions,
        })
    }
}

type Snapshot = HashMap<String, FileMetadata>;

fn create_snapshot(dir_path: &Path) -> Result<Snapshot, std::io::Error> {
    let mut snapshot = HashMap::new();
    for entry in walkdir::WalkDir::new(dir_path) {
        let entry = entry?;
        let path = entry.path();
        if path == dir_path { // Skip the root directory itself
            continue;
        }
        if let Ok(metadata) = FileMetadata::from_path(dir_path, path) {
            snapshot.insert(metadata.path.clone(), metadata);
        }
    }
    Ok(snapshot)
}

#[derive(Debug, PartialEq, Eq)]
enum TremorType {
    NewFile,
    MissingFile,
    MetadataChange { field: String, old: String, new: String },
}

#[derive(Debug, PartialEq, Eq)]
struct Tremor {
    path: String,
    tremor_type: TremorType,
}

fn detect_tremors(dir_path: &Path, old_snapshot: &Snapshot) -> Result<Vec<Tremor>, std::io::Error> {
    let current_snapshot = create_snapshot(dir_path)?;
    let mut tremors = Vec::new();

    // Check for missing files and metadata changes
    for (path, old_meta) in old_snapshot {
        if let Some(current_meta) = current_snapshot.get(path) {
            // Compare metadata
            if old_meta.file_type != current_meta.file_type {
                tremors.push(Tremor {
                    path: path.clone(),
                    tremor_type: TremorType::MetadataChange {
                        field: "file_type".to_string(),
                        old: format!("{:?}", old_meta.file_type),
                        new: format!("{:?}", current_meta.file_type),
                    },
                });
            }
            if old_meta.size != current_meta.size {
                tremors.push(Tremor {
                    path: path.clone(),
                    tremor_type: TremorType::MetadataChange {
                        field: "size".to_string(),
                        old: old_meta.size.to_string(),
                        new: current_meta.size.to_string(),
                    },
                });
            }
            if old_meta.modified != current_meta.modified {
                tremors.push(Tremor {
                    path: path.clone(),
                    tremor_type: TremorType::MetadataChange {
                        field: "modified_time".to_string(),
                        old: old_meta.modified.to_string(),
                        new: current_meta.modified.to_string(),
                    },
                });
            }
            if old_meta.accessed != current_meta.accessed {
                tremors.push(Tremor {
                    path: path.clone(),
                    tremor_type: TremorType::MetadataChange {
                        field: "accessed_time".to_string(),
                        old: old_meta.accessed.to_string(),
                        new: current_meta.accessed.to_string(),
                    },
                });
            }
            if old_meta.permissions != current_meta.permissions {
                tremors.push(Tremor {
                    path: path.clone(),
                    tremor_type: TremorType::MetadataChange {
                        field: "permissions".to_string(),
                        old: format!("{:o}", old_meta.permissions),
                        new: format!("{:o}", current_meta.permissions),
                    },
                });
            }
        } else {
            // File is missing
            tremors.push(Tremor {
                path: path.clone(),
                tremor_type: TremorType::MissingFile,
            });
        }
    }

    // Check for new files
    for (path, _) in current_snapshot {
        if !old_snapshot.contains_key(&path) {
            tremors.push(Tremor {
                path: path.clone(),
                tremor_type: TremorType::NewFile,
            });
        }
    }

    Ok(tremors)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Snapshot { path, output } => {
            println!("Creating snapshot of '{}'...", path.display());
            let snapshot = create_snapshot(path)?;
            let json = serde_json::to_string_pretty(&snapshot)?;
            fs::write(output, json)?;
            println!("Snapshot saved to '{}'.", output.display());
        }
        Commands::Detect { path, snapshot } => {
            println!("Loading snapshot from '{}'...", snapshot.display());
            let snapshot_content = fs::read_to_string(snapshot)?;
            let old_snapshot: Snapshot = serde_json::from_str(&snapshot_content)?;

            println!("Detecting tremors in '{}'...", path.display());
            let tremors = detect_tremors(path, &old_snapshot)?;

            if tremors.is_empty() {
                println!("No tremors detected. The digital landscape is calm.");
            } else {
                println!("--- DIGITAL TREMORS DETECTED! ---");
                for tremor in tremors {
                    match tremor.tremor_type {
                        TremorType::NewFile => println!("  [NEW]    '{}'", tremor.path),
                        TremorType::MissingFile => println!("  [MISSING] '{}'", tremor.path),
                        TremorType::MetadataChange { field, old, new } => println!(
                            "  [CHANGE] '{}': Field '{}' changed from '{}' to '{}'",
                            tremor.path, field, old, new
                        ),
                    }
                }
                println!("---------------------------------");
            }
        }
    }

    Ok(())
}
