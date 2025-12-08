use std::env;
use std::fs;
use std::path::Path;
use std::collections::HashMap;
use clap::{Arg, Command};
use colored::*;

mod analyzer;
mod quantum;

use analyzer::CodeAnalyzer;
use quantum::{QuantumState, QuantumAnalyzer};

fn main() {
    let matches = Command::new("Quantum Entanglement Checker")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Checks if two code snippets are quantum entangled")
        .arg(
            Arg::new("file_a")
                .help("First file to compare")
                .required(true)
                .index(1),
        )
        .arg(
            Arg::new("file_b")
                .help("Second file to compare")
                .required(true)
                .index(2),
        )
        .arg(
            Arg::new("threshold")
                .short('t')
                .long("threshold")
                .value_name("PROBABILITY")
                .help("Entanglement threshold (0.0-1.0)")
                .default_value("0.5"),
        )
        .arg(
            Arg::new("verbose")
                .short('v')
                .long("verbose")
                .help("Verbose output with quantum details")
                .action(clap::ArgAction::SetTrue),
        )
        .arg(
            Arg::new("function")
                .short('f')
                .long("function")
                .value_name("NAME")
                .help("Compare specific function names")
        )
        .get_matches();

    let file_a = matches.get_one::<String>("file_a").unwrap();
    let file_b = matches.get_one::<String>("file_b").unwrap();
    let threshold: f64 = matches.get_one::<String>("threshold").unwrap().parse().expect("Invalid threshold");
    let verbose = matches.get_flag("verbose");
    let function_name = matches.get_one::<String>("function");

    if let Err(e) = run_analysis(file_a, file_b, threshold, verbose, function_name) {
        eprintln!("{}: {}", "Error".red().bold(), e);
        std::process::exit(1);
    }
}

fn run_analysis(
    file_a: &str,
    file_b: &str,
    threshold: f64,
    verbose: bool,
    function_name: Option<&String>,
) -> Result<(), Box<dyn std::error::Error>> {
    println!("{}
{}", "🔬 Quantum Entanglement Analysis".cyan().bold(), "=".repeat(32).cyan());
    println!();
    
    // Read files
    let content_a = fs::read_to_string(file_a)?;
    let content_b = fs::read_to_string(file_b)?;
    
    println!("File A: {}", file_a.bold());
    println!("File B: {}", file_b.bold());
    println!();

    // Analyze code
    let analyzer = CodeAnalyzer::new();
    let metrics_a = analyzer.analyze(&content_a);
    let metrics_b = analyzer.analyze(&content_b);

    // Quantum analysis
    let quantum_analyzer = QuantumAnalyzer::new();
    let result = quantum_analyzer.analyze(&metrics_a, &metrics_b, function_name);

    // Display results
    display_results(&result, threshold, verbose);
    
    Ok(())
}

fn display_results(result: &quantum::EntanglementResult, threshold: f64, verbose: bool) {
    println!("{}: {:.1}%", "Entanglement Probability".yellow().bold(), result.probability * 100.0);
    
    let state_color = match result.state {
        QuantumState::Superposed => "yellow",
        QuantumState::Collapsed => "green",
        QuantumState::Decohered => "red",
    };
    
    println!("{}: {}", "Quantum State".cyan().bold(), format!("{:?}", result.state).color(state_color).bold());
    println!();

    if verbose {
        println!("{}: {:.2}", "Particle Correlation".magenta().bold(), result.particle_correlation);
        println!("{}: {:.2}", "Wave Function Overlap".magenta().bold(), result.wave_overlap);
        println!("{}: {:.2}", "Decoherence Factor".magenta().bold(), result.decoherence);
        println!();
    }

    // Conclusion
    let conclusion = if result.probability >= threshold {
        format!("The code exhibits {} quantum entanglement.", "moderate".yellow())
    } else {
        format!("The code shows {} quantum entanglement.", "weak".red())
    };
    
    println!("{}: {}", "Conclusion".blue().bold(), conclusion);
    
    if result.probability >= threshold {
        println!("{}: {}", "Recommendation".blue().bold(), "Observe with caution - collapse may occur during runtime.".italic());
    } else {
        println!("{}: {}", "Recommendation".blue().bold(), "No meaningful entanglement detected - safe to proceed.".italic());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_entanglement() {
        let content_a = "fn hello() { println!(\"world\"); }";
        let content_b = "fn hello() { println!(\"world\"); }";
        
        let analyzer = CodeAnalyzer::new();
        let metrics_a = analyzer.analyze(content_a);
        let metrics_b = analyzer.analyze(content_b);
        
        let quantum_analyzer = QuantumAnalyzer::new();
        let result = quantum_analyzer.analyze(&metrics_a, &metrics_b, None);
        
        assert!(result.probability > 0.8);
        assert_eq!(result.state, QuantumState::Collapsed);
    }
}
