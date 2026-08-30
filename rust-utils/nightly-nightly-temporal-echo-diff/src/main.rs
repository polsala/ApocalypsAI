use clap::{Parser, Subcommand};
use std::fs;
use std::io::{self, BufRead};
use std::path::{Path, PathBuf};
use sha2::{Sha256, Digest};
use hex;
use dirs;

const ECHO_DIR_NAME: &str = ".temporal_echoes";

#[derive(Parser, Debug)]
#[command(author, version, about = "A tool to create and diff files against their 'temporal echoes' (snapshots).", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Create a temporal echo (snapshot) of a file.
    Create { 
        /// The path to the file to echo.
        file_path: PathBuf 
    },
    /// Diff a file against its temporal echo.
    Diff { 
        /// The path to the file to diff.
        file_path: PathBuf 
    },
    /// List all files that have temporal echoes.
    List {},
    /// Clean (remove) a specific file's temporal echo.
    Clean {
        /// The path to the file whose echo should be removed.
        file_path: PathBuf,
    },
    /// Clean (remove) all temporal echoes.
    CleanAll {},
}

struct EchoManager {
    echo_root: PathBuf,
}

impl EchoManager {
    fn new() -> Result<Self, io::Error> {
        let home_dir = dirs::home_dir()
            .ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "Could not find home directory"))?;
        let echo_root = home_dir.join(ECHO_DIR_NAME);
        
        if !echo_root.exists() {
            fs::create_dir_all(&echo_root)?;
        }
        Ok(EchoManager { echo_root })
    }

    fn get_echo_path(&self, original_path: &Path) -> Result<PathBuf, io::Error> {
        let absolute_path = original_path.canonicalize()?;
        let mut hasher = Sha256::new();
        hasher.update(absolute_path.to_string_lossy().as_bytes());
        let hash = hasher.finalize();
        let hex_hash = hex::encode(hash);
        Ok(self.echo_root.join(format!("{}.echo", hex_hash)))
    }

    fn create_echo(&self, file_path: &Path) -> Result<(), io::Error> {
        if !file_path.exists() {
            return Err(io::Error::new(io::ErrorKind::NotFound, format!("File not found: {}", file_path.display())));
        }
        let echo_path = self.get_echo_path(file_path)?;
        fs::copy(file_path, &echo_path)?;
        println!("Echo created for: {}", file_path.display());
        Ok(())
    }

    fn diff_echo(&self, file_path: &Path) -> Result<(), io::Error> {
        if !file_path.exists() {
            return Err(io::Error::new(io::ErrorKind::NotFound, format!("File not found: {}", file_path.display())));
        }
        let echo_path = self.get_echo_path(file_path)?;

        if !echo_path.exists() {
            println!("No echo found for: {}", file_path.display());
            return Ok(());
        }

        let current_lines: Vec<String> = io::BufReader::new(fs::File::open(file_path)?)
            .lines()
            .filter_map(Result::ok)
            .collect();
        let echo_lines: Vec<String> = io::BufReader::new(fs::File::open(&echo_path)?)
            .lines()
            .filter_map(Result::ok)
            .collect();

        let mut i = 0;
        let mut j = 0;
        let mut changed = false;

        // Simple line-by-line diff. Not a full LCS algorithm, but sufficient for quick change detection.
        while i < current_lines.len() || j < echo_lines.len() {
            if i < current_lines.len() && j < echo_lines.len() {
                if current_lines[i] == echo_lines[j] {
                    println!("  {}", current_lines[i]);
                    i += 1;
                    j += 1;
                } else {
                    changed = true;
                    // Heuristic: If current line matches a later echo line, assume current line is new.
                    let mut found_match_in_echo = false;
                    for k in j+1..echo_lines.len() {
                        if current_lines[i] == echo_lines[k] {
                            println!("- {}", echo_lines[j]); // Echo line was removed
                            j += 1;
                            found_match_in_echo = true;
                            break;
                        }
                    }
                    if !found_match_in_echo {
                        // If no match found later in echo, assume current line is new
                        println!("+ {}", current_lines[i]);
                        i += 1;
                    }
                }
            } else if i < current_lines.len() {
                changed = true;
                println!("+ {}", current_lines[i]);
                i += 1;
            } else if j < echo_lines.len() {
                changed = true;
                println!("- {}", echo_lines[j]);
                j += 1;
            }
        }
        
        if !changed {
            println!("No changes detected for: {}", file_path.display());
        }

        Ok(())}

    fn list_echoes(&self) -> Result<(), io::Error> {
        let mut found_echoes = false;
        for entry in fs::read_dir(&self.echo_root)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_file() && path.extension().map_or(false, |ext| ext == "echo") {
                // Currently, we list the hash-based filename. To list original paths, 
                // we'd need to store metadata (e.g., in a separate file or DB).
                println!("Echo: {}", path.file_name().unwrap().to_string_lossy());
                found_echoes = true;
            }
        }
        if !found_echoes {
            println!("No temporal echoes found.");
        }
        Ok(())
    }

    fn clean_echo(&self, file_path: &Path) -> Result<(), io::Error> {
        let echo_path = self.get_echo_path(file_path)?;
        if echo_path.exists() {
            fs::remove_file(&echo_path)?;
            println!("Echo removed for: {}", file_path.display());
        } else {
            println!("No echo found for: {}", file_path.display());
        }
        Ok(())
    }

    fn clean_all_echoes(&self) -> Result<(), io::Error> {
        if self.echo_root.exists() {
            fs::remove_dir_all(&self.echo_root)?;
            println!("All temporal echoes removed.");
        } else {
            println!("No temporal echoes directory found.");
        }
        Ok(())
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    let manager = EchoManager::new()?;

    match cli.command {
        Commands::Create { file_path } => manager.create_echo(&file_path)?,
        Commands::Diff { file_path } => manager.diff_echo(&file_path)?,
        Commands::List {} => manager.list_echoes()?,
        Commands::Clean { file_path } => manager.clean_echo(&file_path)?,
        Commands::CleanAll {} => manager.clean_all_echoes()?,
    }

    Ok(())
}
