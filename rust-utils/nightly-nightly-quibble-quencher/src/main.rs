use clap::Parser;
use std::fs;
use std::io::{self, BufRead};
use std::str::FromStr;

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Clone)]
struct Quibble {
    score: u32,
    urgency: u8,
    complexity: u8,
    impact: u8,
    description: String,
}

impl Quibble {
    fn new(description: String, urgency: u8, complexity: u8, impact: u8, weights: &Weights) -> Self {
        let score = (urgency as u32 * weights.urgency)
            + (complexity as u32 * weights.complexity)
            + (impact as u32 * weights.impact);
        Quibble { description, urgency, complexity, impact, score }
    }
}

impl FromStr for Quibble {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split('|').map(|p| p.trim()).collect();
        if parts.len() != 4 {
            return Err(format!("Invalid quibble format: '{}'. Expected 'Description | Urgency | Complexity | Impact'.", s));
        }

        let description = parts[0].to_string();
        let urgency = parts[1].parse::<u8>().map_err(|e| format!("Invalid urgency value: {}. {}", parts[1], e))?;
        let complexity = parts[2].parse::<u8>().map_err(|e| format!("Invalid complexity value: {}. {}", parts[2], e))?;
        let impact = parts[3].parse::<u8>().map_err(|e| format!("Invalid impact value: {}. {}", parts[3], e))?;

        // Default weights for parsing, actual scoring happens in main
        let default_weights = Weights { urgency: 1, complexity: 1, impact: 1 };
        Ok(Quibble::new(description, urgency, complexity, impact, &default_weights))
    }
}

#[derive(Debug, Parser)]
#[clap(author, version, about = "Prioritize your quibbles with quantum precision!")]
struct Args {
    /// Path to a file containing quibbles. If not provided, reads from stdin.
    #[clap(short, long)]
    file: Option<String>,

    /// Weight for the urgency factor (default: 1)
    #[clap(long, default_value = "1")]
    weight_urgency: u32,

    /// Weight for the complexity factor (default: 1)
    #[clap(long, default_value = "1")]
    weight_complexity: u32,

    /// Weight for the impact factor (default: 1)
    #[clap(long, default_value = "1")]
    weight_impact: u32,
}

#[derive(Debug)]
struct Weights {
    urgency: u32,
    complexity: u32,
    impact: u32,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let weights = Weights {
        urgency: args.weight_urgency,
        complexity: args.weight_complexity,
        impact: args.weight_impact,
    };

    let mut quibbles: Vec<Quibble> = Vec::new();

    if let Some(file_path) = args.file {
        let content = fs::read_to_string(file_path)?;
        for line in content.lines() {
            if line.trim().is_empty() { continue; }
            let parsed_quibble = Quibble::from_str(line)?;
            quibbles.push(Quibble::new(
                parsed_quibble.description,
                parsed_quibble.urgency,
                parsed_quibble.complexity,
                parsed_quibble.impact,
                &weights,
            ));
        }
    } else {
        let stdin = io::stdin();
        for line_result in stdin.lock().lines() {
            let line = line_result?;
            if line.trim().is_empty() { continue; }
            let parsed_quibble = Quibble::from_str(&line)?;
            quibbles.push(Quibble::new(
                parsed_quibble.description,
                parsed_quibble.urgency,
                parsed_quibble.complexity,
                parsed_quibble.impact,
                &weights,
            ));
        }
    }

    quibbles.sort_by(|a, b| b.score.cmp(&a.score)); // Sort descending by score

    println!("Prioritized Quibbles:");
    println!("--------------------");
    for quibble in quibbles {
        println!("Score: {} - {} | {} | {} | {}",
            quibble.score,
            quibble.description,
            quibble.urgency,
            quibble.complexity,
            quibble.impact
        );
    }

    Ok(())
}
