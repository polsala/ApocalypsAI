use clap::{Arg, Command};
use color_eyre::eyre::Result;
use serde::{Deserialize, Serialize};
use std::time::SystemTime;

#[derive(Debug, Serialize, Deserialize)]
struct SystemInfo {
    rust_version: String,
    current_time: String,
    working_directory: String,
    platform: String,
}

fn main() -> Result<()> {
    color_eyre::install()?;
    
    let matches = Command::new("Rust Example")
        .version("1.0")
        .author("Nightly Docker DevBox")
        .about("A sample Rust application for the development environment")
        .arg(
            Arg::new("json")
                .short('j')
                .long("json")
                .help("Output in JSON format")
                .action(clap::ArgAction::SetTrue),
        )
        .get_matches();
    
    let info = get_system_info()?;
    
    if matches.get_flag("json") {
        println!("{}", serde_json::to_string_pretty(&info)?);
    } else {
        print_human_readable(&info);
    }
    
    Ok(())
}

fn get_system_info() -> Result<SystemInfo> {
    let rust_version = rustc_version_runtime::version();
    let current_time = SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)?
        .as_secs();
    let working_directory = std::env::current_dir()?.display().to_string();
    let platform = format!("{} {}", std::env::consts::OS, std::env::consts::ARCH);
    
    Ok(SystemInfo {
        rust_version: rust_version.to_string(),
        current_time: current_time.to_string(),
        working_directory,
        platform,
    })
}

fn print_human_readable(info: &SystemInfo) {
    println!("🦀 Welcome to the Rust Development Environment!");
    println!("Rust version: {}", info.rust_version);
    println!("Current time: {}", info.current_time);
    println!("Working directory: {}", info.working_directory);
    println!("Platform: {}", info.platform);
    
    println!("\n📊 Basic Rust functionality:");
    
    // Vector example
    let squares: Vec<i32> = (1..=10).map(|x| x * x).collect();
    println!("Squares 1-10: {:?}", squares);
    
    // HashMap example
    use std::collections::HashMap;
    let mut word_lengths = HashMap::new();
    for word in ["hello", "world", "rust", "devbox"] {
        word_lengths.insert(word, word.len());
    }
    println!("Word lengths: {:?}", word_lengths);
    
    println!("\n🎉 Rust environment is ready for development!");
}
