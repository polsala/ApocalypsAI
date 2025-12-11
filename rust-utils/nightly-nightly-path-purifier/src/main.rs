use clap::{Arg, Command};
use std::collections::HashSet;
use std::env;
use std::path::{Path, PathBuf};
use std::io::{self, Write};

fn main() {
    let matches = Command::new("path-purifier")
        .version("0.1.0")
        .author("ApocalypsAI Nightly Integrator")
        .about("A high-performance Rust CLI tool to clean and optimize your system's PATH environment variable.")
        .arg(
            Arg::new("dry-run")
                .short('d')
                .long("dry-run")
                .action(clap::ArgAction::SetTrue)
                .help("Perform a dry run and show what changes would be made"),
        )
        .arg(
            Arg::new("apply")
                .short('a')
                .long("apply")
                .action(clap::ArgAction::SetTrue)
                .help("Apply the changes and print the new PATH to stdout"),
        )
        .arg(
            Arg::new("interactive")
                .short('i')
                .long("interactive")
                .action(clap::ArgAction::SetTrue)
                .help("Interactively choose which paths to keep or remove"),
        )
        .get_matches();

    let path_env = env::var_os("PATH").unwrap_or_default();
    // Path delimiter is handled by env::split_paths and env::join_paths automatically

    let original_paths: Vec<PathBuf> = env::split_paths(&path_env).collect();
    let mut cleaned_paths: Vec<PathBuf> = Vec::new();
    let mut seen_paths: HashSet<PathBuf> = HashSet::new();
    let mut removed_entries: Vec<String> = Vec::new();

    for path_buf in original_paths {
        let path_str = path_buf.to_string_lossy().to_string();
        let exists = path_buf.exists();
        let is_duplicate = seen_paths.contains(&path_buf);

        let mut should_keep = true;
        let mut reason = String::new();

        if !exists {
            reason = format!("(non-existent)");
            should_keep = false;
        } else if is_duplicate {
            reason = format!("(duplicate)");
            should_keep = false;
        }

        if matches.get_flag("interactive") && !should_keep {
            print!("Path '{}' {} - Keep? (y/N): ", path_str, reason);
            io::stdout().flush().unwrap();
            let mut input = String::new();
            io::stdin().read_line(&mut input).unwrap();
            if input.trim().to_lowercase() == "y" {
                should_keep = true;
            } else {
                removed_entries.push(path_str.clone());
            }
        }

        if should_keep {
            if !seen_paths.contains(&path_buf) {
                cleaned_paths.push(path_buf.clone());
                seen_paths.insert(path_buf);
            } else if matches.get_flag("interactive") && is_duplicate {
                // If interactive, and user chose to keep a duplicate, we still only add it once.
                // This branch handles the case where `should_keep` was set to true by interactive mode
                // for a duplicate, but we still don't add it again to `cleaned_paths`.
                // The `removed_entries` logic above handles if user chose not to keep.
            } else if !matches.get_flag("interactive") && is_duplicate {
                removed_entries.push(path_str.clone());
            }
        } else if !matches.get_flag("interactive") {
            removed_entries.push(path_str.clone());
        }
    }

    let new_path_env = env::join_paths(cleaned_paths).unwrap();

    if matches.get_flag("dry-run") || matches.get_flag("interactive") {
        println!("--- Original PATH ---");
        println!("{}", path_env.to_string_lossy());
        println!("\n--- Proposed Clean PATH ---");
        println!("{}", new_path_env.to_string_lossy());

        if !removed_entries.is_empty() {
            println!("\n--- Removed Entries ---");
            for entry in removed_entries {
                println!("- {}", entry);
            }
        } else {
            println!("\nNo entries removed.");
        }
    }

    if matches.get_flag("apply") {
        print!("{}", new_path_env.to_string_lossy());
    }
}
