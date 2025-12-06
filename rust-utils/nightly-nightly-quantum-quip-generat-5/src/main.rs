use clap::{Arg, Command};
use colored::*;
use serde::{Deserialize, Serialize};
use std::fs;
use std::io::{self, Write};

mod generator;
mod jokes;
mod pcg;

use generator::{JokeCategory, JokeGenerator};

#[derive(Debug, Serialize, Deserialize)]
struct Joke {
    category: String,
    setup: String,
    punchline: String,
    explanation: String,
}

impl Joke {
    fn new(category: JokeCategory, setup: String, punchline: String, explanation: String) -> Self {
        Self {
            category: format!("{:?}", category).to_lowercase(),
            setup,
            punchline,
            explanation,
        }
    }

    fn display(&self, detailed: bool) {
        println!("\n{}", "Quantum Quip Generator".bright_cyan().bold());
        println!("{}", "=".repeat(50).bright_cyan());
        println!("{}: {}", "Category".bright_yellow(), self.category.bright_green());
        println!("{}: {}", "Setup".bright_yellow(), self.setup.bright_white());
        println!("{}: {}", "Punchline".bright_yellow(), self.punchline.bright_magenta());
        
        if detailed {
            println!("{}: {}", "Explanation".bright_yellow(), self.explanation.bright_blue());
        }
        
        println!("{}", "=".repeat(50).bright_cyan());
    }
}

fn main() {
    let matches = Command::new("Quantum Quip Generator")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Generates quantum-themed programming jokes with deterministic randomness")
        .arg(
            Arg::new("seed")
                .short('s')
                .long("seed")
                .value_name("NUMBER")
                .help("Set a specific seed for deterministic randomness")
                .default_value("0")
        )
        .arg(
            Arg::new("category")
                .short('c')
                .long("category")
                .value_name("CATEGORY")
                .help("Filter jokes by category: quantum, programming, or ai")
                .possible_values(["quantum", "programming", "ai"])
        )
        .arg(
            Arg::new("count")
                .short('n')
                .long("count")
                .value_name("NUMBER")
                .help("Number of jokes to generate")
                .default_value("1")
        )
        .arg(
            Arg::new("export")
                .long("export")
                .value_name("FORMAT")
                .help("Export format: json or text")
                .possible_values(["json", "text"])
        )
        .arg(
            Arg::new("output")
                .short('o')
                .long("output")
                .value_name("FILE")
                .help("Output file path")
        )
        .arg(
            Arg::new("interactive")
                .short('i')
                .long("interactive")
                .help("Start interactive mode")
        )
        .arg(
            Arg::new("detailed")
                .short('d')
                .long("detailed")
                .help("Show detailed explanations")
        )
        .get_matches();

    let seed: u64 = matches
        .get_one::<String>("seed")
        .unwrap()
        .parse()
        .expect("Seed must be a valid number");

    let category = matches
        .get_one::<String>("category")
        .map(|c| match c.as_str() {
            "quantum" => JokeCategory::Quantum,
            "programming" => JokeCategory::Programming,
            "ai" => JokeCategory::AI,
            _ => JokeCategory::Any,
        })
        .unwrap_or(JokeCategory::Any);

    let count: usize = matches
        .get_one::<String>("count")
        .unwrap()
        .parse()
        .expect("Count must be a valid number");

    let export_format = matches.get_one::<String>("export").map(|s| s.clone());
    let output_file = matches.get_one::<String>("output").map(|s| s.clone());
    let interactive = matches.get_flag("interactive");
    let detailed = matches.get_flag("detailed");

    let mut generator = JokeGenerator::new(seed);

    if interactive {
        run_interactive_mode(&mut generator);
    } else {
        let jokes: Vec<Joke> = (0..count)
            .map(|_| {
                let joke_data = generator.generate_joke(category);
                Joke::new(
                    joke_data.category,
                    joke_data.setup,
                    joke_data.punchline,
                    joke_data.explanation,
                )
            })
            .collect();

        if let Some(format) = export_format {
            export_jokes(&jokes, &format, output_file.as_deref()).expect("Failed to export jokes");
        } else {
            for joke in jokes {
                joke.display(detailed);
            }
        }
    }
}

fn run_interactive_mode(generator: &mut JokeGenerator) {
    println!("{}", "Welcome to Quantum Quip Generator Interactive Mode!".bright_cyan().bold());
    println!("{}", "Type 'help' for available commands, 'quit' to exit.".bright_yellow());
    println!();

    loop {
        print!("{} ", "Quantum>".bright_green().bold());
        io::stdout().flush().unwrap();

        let mut input = String::new();
        io::stdin().read_line(&mut input).expect("Failed to read line");
        let input = input.trim();

        match input.to_lowercase().as_str() {
            "quit" | "exit" => {
                println!("{}", "Thanks for using Quantum Quip Generator!".bright_cyan());
                break;
            }
            "help" => show_help(),
            "random" | "generate" | "" => {
                let joke_data = generator.generate_joke(JokeCategory::Any);
                let joke = Joke::new(
                    joke_data.category,
                    joke_data.setup,
                    joke_data.punchline,
                    joke_data.explanation,
                );
                joke.display(true);
            }
            "quantum" => {
                let joke_data = generator.generate_joke(JokeCategory::Quantum);
                let joke = Joke::new(
                    joke_data.category,
                    joke_data.setup,
                    joke_data.punchline,
                    joke_data.explanation,
                );
                joke.display(true);
            }
            "programming" => {
                let joke_data = generator.generate_joke(JokeCategory::Programming);
                let joke = Joke::new(
                    joke_data.category,
                    joke_data.setup,
                    joke_data.punchline,
                    joke_data.explanation,
                );
                joke.display(true);
            }
            "ai" => {
                let joke_data = generator.generate_joke(JokeCategory::AI);
                let joke = Joke::new(
                    joke_data.category,
                    joke_data.setup,
                    joke_data.punchline,
                    joke_data.explanation,
                );
                joke.display(true);
            }
            cmd => {
                if cmd.starts_with("seed ") {
                    if let Some(seed_str) = cmd.split_whitespace().nth(1) {
                        match seed_str.parse::<u64>() {
                            Ok(seed) => {
                                generator.set_seed(seed);
                                println!("{}", format!("Seed set to: {}", seed).bright_green());
                            }
                            Err(_) => println!("{}", "Invalid seed value. Please provide a number.".bright_red()),
                        }
                    } else {
                        println!("{}", "Please specify a seed value. Usage: seed <number>".bright_yellow());
                    }
                } else {
                    println!("{}", "Unknown command. Type 'help' for available commands.".bright_red());
                }
            }
        }
    }
}

fn show_help() {
    println!("{}", "Available commands:".bright_cyan().bold());
    println!("  {} - Generate a random joke", "random".bright_green());
    println!("  {} - Generate a quantum physics joke", "quantum".bright_green());
    println!("  {} - Generate a programming joke", "programming".bright_green());
    println!("  {} - Generate an AI joke", "ai".bright_green());
    println!("  {} <number> - Set the random seed", "seed".bright_green());
    println!("  {} - Show this help message", "help".bright_green());
    println!("  {} - Exit interactive mode", "quit".bright_green());
    println!();
}

fn export_jokes(jokes: &[Joke], format: &str, output_file: Option<&str>) -> io::Result<()> {
    let output = match format {
        "json" => {
            let json = serde_json::to_string_pretty(jokes)?;
            json
        }
        "text" => {
            let mut text = String::new();
            for joke in jokes {
                text.push_str(&format!("Category: {}\n", joke.category));
                text.push_str(&format!("Setup: {}\n", joke.setup));
                text.push_str(&format!("Punchline: {}\n", joke.punchline));
                text.push_str(&format!("Explanation: {}\n", joke.explanation));
                text.push_str("\n");
            }
            text
        }
        _ => return Err(io::Error::new(io::ErrorKind::InvalidInput, "Unknown export format")),
    };

    if let Some(file_path) = output_file {
        fs::write(file_path, output)?;
        println!("{}", format!("Jokes exported to: {}", file_path).bright_green());
    } else {
        println!("{}", output);
    }

    Ok(())
}
