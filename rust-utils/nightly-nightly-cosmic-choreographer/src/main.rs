use clap::Parser;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::io::{self, Read};
use std::fs::File;

/// A whimsical CLI tool that helps survivors prioritize their daily tasks
/// by aligning them with the whims of the cosmos.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to the file containing tasks, one per line. If not provided, reads from stdin.
    #[arg(short, long)]
    tasks_file: Option<String>,

    /// A numerical seed for cosmic alignment. Use the same seed for consistent results.
    /// Defaults to 0 if not provided.
    #[arg(short, long, default_value_t = 0)]
    seed: u64,
}

// Function to calculate a deterministic cosmic score
fn calculate_cosmic_score(task: &str, seed: u64) -> u64 {
    let mut hasher = DefaultHasher::new();
    task.hash(&mut hasher);
    seed.hash(&mut hasher); // Incorporate the seed
    hasher.finish()
}

// Main logic to process tasks from a reader
fn process_tasks<R: Read>(reader: R, seed: u64) -> Vec<(u64, String)> {
    let mut content = String::new();
    // It's okay to unwrap here for simplicity in this utility,
    // as file/stdin reading errors are typically handled at a higher level (main)
    // or are considered fatal for the utility's core function.
    reader.read_to_string(&mut content).expect("Failed to read tasks content");

    let mut tasks_with_scores: Vec<(u64, String)> = content
        .lines()
        .filter(|line| !line.trim().is_empty())
        .map(|line| {
            let score = calculate_cosmic_score(line, seed);
            (score, line.to_string())
        })
        .collect();

    tasks_with_scores.sort_by_key(|(score, _)| *score);
    tasks_with_scores
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let tasks_with_scores = if let Some(path) = args.tasks_file {
        let file = File::open(&path)
            .map_err(|e| io::Error::new(e.kind(), format!("Failed to open tasks file '{}': {}", path, e)))?;
        process_tasks(file, args.seed)
    } else {
        // Read from stdin if no file path is given
        let stdin = io::stdin();
        let handle = stdin.lock();
        process_tasks(handle, args.seed)
    };

    println!("--- Cosmic Choreographer's Nudge (Seed: {}) ---", args.seed);
    if tasks_with_scores.is_empty() {
        println!("The cosmos is silent. Perhaps there are no tasks to align today?");
    } else {
        for (i, (score, task)) in tasks_with_scores.iter().enumerate() {
            let nudge = match i {
                0 => "The cosmos whispers: This is your destiny!",
                1 => "A faint starlight guides you here.",
                2 => "The void suggests this path.",
                _ => "A minor celestial alignment points this way.",
            };
            println!("[Score: {:<19}] {} - {}", score, task, nudge); // Adjusted padding for u64
        }
    }

    Ok(())
}
