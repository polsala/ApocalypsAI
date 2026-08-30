use clap::{Parser, Subcommand};
use std::collections::HashMap;
use std::env;
use anyhow::Result;

mod profile_manager;

#[derive(Parser, Debug)]
#[command(author, version, about = "A Rust CLI tool to manage and switch between sets of environment variables, treating them as 'scavenged caches' for different project 'wasteland zones'.", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Store current environment variables as a named cache
    Store {
        /// Name of the environment cache to store
        name: String,
    },
    /// Load a named environment cache and output variables for 'eval'
    Load {
        /// Name of the environment cache to load
        name: String,
    },
    /// List all available environment caches
    List {},
    /// Remove a named environment cache
    Remove {
        /// Name of the environment cache to remove
        name: String,
    },
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    let config_dir = profile_manager::get_config_dir()?;

    match &cli.command {
        Commands::Store { name } => {
            let current_env: HashMap<String, String> = env::vars()
                .filter(|(key, _)| {
                    // Exclude common system environment variables that are usually not project-specific
                    !matches!(key.as_str(), "PATH" | "HOME" | "PWD" | "SHELL" | "USER" | "TERM" | "SHLVL" | "_" | "OLDPWD")
                })
                .collect();
            profile_manager::save_profile(&config_dir, name, current_env)?;
            println!("Scavenged cache '{}' stored successfully.", name);
        }
        Commands::Load { name } => {
            match profile_manager::load_profile(&config_dir, name)? {
                Some(profile) => {
                    for (key, value) in profile.vars {
                        // Output in a format suitable for 'eval'
                        println!("export {}=\"{}";", key, value.replace('"', "\\\""));
                    }
                }
                None => {
                    eprintln!("Error: Scavenged cache '{}' not found.", name);
                    std::process::exit(1);
                }
            }
        }
        Commands::List {} => {
            let profiles = profile_manager::list_profiles(&config_dir)?;
            if profiles.is_empty() {
                println!("No scavenged caches found. Start by 'store'ing one!");
            } else {
                println!("Available scavenged caches:");
                for profile_name in profiles {
                    println!("- {}", profile_name);
                }
            }
        }
        Commands::Remove { name } => {
            profile_manager::remove_profile(&config_dir, name)?;
            println!("Scavenged cache '{}' removed successfully.", name);
        }
    }

    Ok(())
}
