use clap::Parser;
use std::cmp::Ordering;
use std::error::Error;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

#[derive(Debug, PartialEq, Clone)]
struct Task {
    name: String,
    decay_rate: u8,
    survival_impact: u8,
    priority_score: f32,
}

impl Task {
    fn new(name: String, decay_rate: u8, survival_impact: u8) -> Result<Self, Box<dyn Error>> {
        if decay_rate > 10 || survival_impact > 10 {
            return Err(format!("Decay rate ({}) and survival impact ({}) must be between 0 and 10.", decay_rate, survival_impact).into());
        }
        let priority_score = (survival_impact as f32 + 1.0) / (decay_rate as f32 + 1.0);
        Ok(Task {
            name,
            decay_rate,
            survival_impact,
            priority_score,
        })
    }
}

impl Eq for Task {}

impl PartialOrd for Task {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        // We want to sort in descending order of priority_score
        other.priority_score.partial_cmp(&self.priority_score)
    }
}

impl Ord for Task {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap_or(Ordering::Equal)
    }
}

#[derive(Parser, Debug)]
#[command(author, version, about = "Prioritize survival tasks based on temporal decay and critical impact.", long_about = None)]
struct Args {
    /// Path to a file containing tasks. If not provided, reads from stdin.
    #[arg(name = "FILE")]
    file_path: Option<String>,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let reader: Box<dyn BufRead> = match args.file_path {
        Some(path) => Box::new(BufReader::new(File::open(path)?)),
        None => Box::new(BufReader::new(io::stdin())),
    };

    let mut tasks: Vec<Task> = Vec::new();

    for (line_num, line_result) in reader.lines().enumerate() {
        let line = line_result?;
        if line.trim().is_empty() { continue; }

        let parts: Vec<&str> = line.split(',').collect();
        if parts.len() != 3 {
            eprintln!("Warning: Skipping malformed line {}: '{}'. Expected 'Task Name,Decay Rate (0-10),Survival Impact (0-10)'.", line_num + 1, line);
            continue;
        }

        let name = parts[0].trim().to_string();
        let decay_rate = match parts[1].trim().parse::<u8>() {
            Ok(val) => val,
            Err(_) => {
                eprintln!("Warning: Skipping line {}: Invalid decay rate '{}'. Must be a number 0-10.", line_num + 1, parts[1]);
                continue;
            }
        };
        let survival_impact = match parts[2].trim().parse::<u8>() {
            Ok(val) => val,
            Err(_) => {
                eprintln!("Warning: Skipping line {}: Invalid survival impact '{}'. Must be a number 0-10.", line_num + 1, parts[2]);
                continue;
            }
        };

        match Task::new(name, decay_rate, survival_impact) {
            Ok(task) => tasks.push(task),
            Err(e) => eprintln!("Warning: Skipping line {}: {}.", line_num + 1, e),
        }
    }

    tasks.sort(); // Sorts in descending order of priority_score due to Ord implementation

    println!("Prioritized Tasks:");
    println!("------------------");
    if tasks.is_empty() {
        println!("No tasks to prioritize.");
    } else {
        for (i, task) in tasks.iter().enumerate() {
            println!("{}. {} (Priority: {:.2})", i + 1, task.name, task.priority_score);
        }
    }

    Ok(())
}
