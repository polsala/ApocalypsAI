use clap::{Arg, Command};
use serde::{Deserialize, Serialize};
use std::fs;
use std::io::{self, Write};
use rand::seq::SliceRandom;
use rand::thread_rng;
use colorize::AnsiColor;

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Joke {
    id: u32,
    text: String,
    style: JokeStyle,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
enum JokeStyle {
    Quantum,
    Programming,
    Mixed,
}

impl ToString for JokeStyle {
    fn to_string(&self) -> String {
        match self {
            JokeStyle::Quantum => "quantum".to_string(),
            JokeStyle::Programming => "programming".to_string(),
            JokeStyle::Mixed => "mixed".to_string(),
        }
    }
}

struct QuantumQuipGenerator {
    jokes: Vec<Joke>,
}

impl QuantumQuipGenerator {
    fn new() -> Self {
        let jokes = vec![
            Joke {
                id: 1,
                text: "Why don't quantum programmers ever make decisions? Because they exist in a superposition of states until observed!".to_string(),
                style: JokeStyle::Mixed,
            },
            Joke {
                id: 2,
                text: "What do you call a quantum computer that tells jokes? A qubit of humor!".to_string(),
                style: JokeStyle::Mixed,
            },
            Joke {
                id: 3,
                text: "Why did Schrödinger's cat start a coding blog? Because it wanted to share its thoughts on being both alive and dead in the tech world!".to_string(),
                style: JokeStyle::Mixed,
            },
            Joke {
                id: 4,
                text: "How many quantum programmers does it take to change a light bulb? None, they just observe it in the dark until it decides to be on!".to_string(),
                style: JokeStyle::Quantum,
            },
            Joke {
                id: 5,
                text: "Why do quantum algorithms make terrible comedians? Their punchlines are always in superposition until someone measures them!".to_string(),
                style: JokeStyle::Programming,
            },
            Joke {
                id: 6,
                text: "What's a quantum programmer's favorite type of music? Entangled harmonies!".to_string(),
                style: JokeStyle::Quantum,
            },
            Joke {
                id: 7,
                text: "Why don't quantum bugs ever get fixed? Because they exist in a superposition of being both fixed and unfixed until you test them!".to_string(),
                style: JokeStyle::Programming,
            },
            Joke {
                id: 8,
                text: "How do quantum computers apologize? They say 'I'm sorry, I was in a superposition of being right and wrong!'".to_string(),
                style: JokeStyle::Mixed,
            },
            Joke {
                id: 9,
                text: "Why did the quantum bit break up with the classical bit? Because it needed more space to be in multiple states at once!".to_string(),
                style: JokeStyle::Quantum,
            },
            Joke {
                id: 10,
                text: "What do you call a bug that only appears when you're not looking at it? A quantum observation bug!".to_string(),
                style: JokeStyle::Programming,
            },
            Joke {
                id: 11,
                text: "Why do quantum programmers love coffee? Because it helps them maintain their coherence!".to_string(),
                style: JokeStyle::Mixed,
            },
            Joke {
                id: 12,
                text: "How do you organize a quantum party? You don't plan it, you just observe it happening!".to_string(),
                style: JokeStyle::Quantum,
            },
            Joke {
                id: 13,
                text: "Why did the programmer learn quantum mechanics? To understand the uncertainty principle of his deadlines!".to_string(),
                style: JokeStyle::Programming,
            },
            Joke {
                id: 14,
                text: "What's the difference between a quantum programmer and a classical programmer? One embraces uncertainty, the other just debugs!".to_string(),
                style: JokeStyle::Mixed,
            },
            Joke {
                id: 15,
                text: "Why don't quantum algorithms ever get lost? Because they can be in multiple places at once!".to_string(),
                style: JokeStyle::Quantum,
            },
        ];
        
        Self { jokes }
    }

    fn generate_joke(&self, style: &JokeStyle) -> &Joke {
        let mut rng = thread_rng();
        
        let filtered_jokes: Vec<&Joke> = match style {
            JokeStyle::Quantum => self.jokes.iter().filter(|j| j.style == JokeStyle::Quantum || j.style == JokeStyle::Mixed).collect(),
            JokeStyle::Programming => self.jokes.iter().filter(|j| j.style == JokeStyle::Programming || j.style == JokeStyle::Mixed).collect(),
            JokeStyle::Mixed => self.jokes.iter().collect(),
        };
        
        filtered_jokes.choose(&mut rng).unwrap_or(&self.jokes[0])
    }

    fn generate_multiple_jokes(&self, count: usize, style: &JokeStyle) -> Vec<&Joke> {
        (0..count).map(|_| self.generate_joke(style)).collect()
    }

    fn export_to_json(&self, jokes: Vec<&Joke>, filename: &str) -> io::Result<()> {
        let jokes_data: Vec<&Joke> = jokes;
        let json = serde_json::to_string_pretty(&jokes_data)?;
        fs::write(filename, json)?;
        Ok(())
    }

    fn export_to_text(&self, jokes: Vec<&Joke>, filename: &str) -> io::Result<()> {
        let content = jokes.iter()
            .map(|j| format!"{}\n\n", j.text))
            .collect::<String>();
        fs::write(filename, content)?;
        Ok(())
    }

    fn print_joke(&self, joke: &Joke) {
        println!("{}", "=".repeat(60).green());
        println!("{}", joke.text.green());
        println!("{}", "=".repeat(60).green());
        println!("\nStyle: {} | ID: {}\n", joke.style.to_string().blue(), joke.id.to_string().yellow());
    }

    fn interactive_mode(&self, style: JokeStyle) {
        println!("{}", "Welcome to Quantum Quip Generator Interactive Mode!".bright_cyan().bold());
        println!("{}", "Type 'exit' to quit, 'help' for commands, or press Enter to generate a joke.".cyan());
        println!("\n{}
", "=".repeat(60).bright_magenta());
        
        loop {
            print!("{}", "Quantum> ".bright_yellow().bold());
            io::stdout().flush().unwrap();
            
            let mut input = String::new();
            io::stdin().read_line(&mut input).expect("Failed to read line");
            let input = input.trim();
            
            match input.to_lowercase().as_str() {
                "exit" | "quit" => {
                    println!("{}", "Thanks for using Quantum Quip Generator! Stay quantumly awesome!".bright_cyan());
                    break;
                },
                "help" => {
                    println!("{}", "Available commands:".bright_yellow());
                    println!("  - Press Enter: Generate a random joke");
                    println!("  - help: Show this help message");
                    println!("  - exit/quit: Exit interactive mode");
                    println!("  - style [quantum|programming|mixed]: Change joke style");
                },
                s if s.starts_with("style ") => {
                    let new_style = match s.split_whitespace().nth(1) {
                        Some("quantum") => JokeStyle::Quantum,
                        Some("programming") => JokeStyle::Programming,
                        _ => {
                            println!("{}", "Invalid style. Use: quantum, programming, or mixed".red());
                            continue;
                        }
                    };
                    style = new_style.clone();
                    println!("{}", format!("Style changed to: {}", style.to_string()).green());
                },
                "" => {
                    let joke = self.generate_joke(&style);
                    self.print_joke(joke);
                },
                _ => {
                    println!("{}", "Unknown command. Type 'help' for available commands.".red());
                }
            }
        }
    }
}

fn main() {
    let matches = Command::new("Nightly Quantum Quip Generator")
        .version("0.1.0")
        .author("ApocalypsAI Community")
        .about("Generates quantum-themed programming jokes and puns")
        .arg(
            Arg::new("count")
                .short('c')
                .long("count")
                .value_name("NUMBER")
                .help("Number of jokes to generate")
                .default_value("1")
        )
        .arg(
            Arg::new("style")
                .short('s')
                .long("style")
                .value_name("STYLE")
                .help("Joke style: quantum, programming, or mixed")
                .default_value("mixed")
        )
        .arg(
            Arg::new("export")
                .short('e')
                .long("export")
                .value_name("FORMAT")
                .help("Export format: json or text")
        )
        .arg(
            Arg::new("output")
                .short('o')
                .long("output")
                .value_name("FILE")
                .help("Output file name")
        )
        .arg(
            Arg::new("interactive")
                .short('i')
                .long("interactive")
                .help("Start interactive mode")
                .action(clap::ArgAction::SetTrue)
        )
        .get_matches();

    let generator = QuantumQuipGenerator::new();
    
    let style = match matches.get_one::<String>("style").map(String::as_str) {
        Some("quantum") => JokeStyle::Quantum,
        Some("programming") => JokeStyle::Programming,
        _ => JokeStyle::Mixed,
    };
    
    let count: usize = matches.get_one::<String>("count")
        .and_then(|s| s.parse().ok())
        .unwrap_or(1);
    
    if matches.get_flag("interactive") {
        generator.interactive_mode(style);
        return;
    }
    
    if let Some(export_format) = matches.get_one::<String>("export") {
        let output_file = matches.get_one::<String>("output")
            .unwrap_or(&format!("quantum_jokes.{}", export_format));
        
        let jokes = generator.generate_multiple_jokes(count, &style);
        
        match export_format.as_str() {
            "json" => {
                if let Err(e) = generator.export_to_json(jokes, output_file) {
                    eprintln!("{} Error exporting to JSON: {}", "ERROR".red(), e);
                    std::process::exit(1);
                }
                println!("{} Jokes exported to {}", "SUCCESS".green(), output_file.green());
            },
            "text" => {
                if let Err(e) = generator.export_to_text(jokes, output_file) {
                    eprintln!("{} Error exporting to text: {}", "ERROR".red(), e);
                    std::process::exit(1);
                }
                println!("{} Jokes exported to {}", "SUCCESS".green(), output_file.green());
            },
            _ => {
                eprintln!("{} Invalid export format. Use 'json' or 'text'.", "ERROR".red());
                std::process::exit(1);
            }
        }
    } else {
        let jokes = generator.generate_multiple_jokes(count, &style);
        for joke in jokes {
            generator.print_joke(joke);
        }
    }
}
