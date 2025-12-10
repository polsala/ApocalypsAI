use std::env;
use std::fs;
use std::process;
use sha2::{Sha256, Digest};
use colored::*;

mod quantum_checker;
mod utils;

use quantum_checker::QuantumChecker;
use utils::{read_file, show_usage, show_banner};

fn main() {
    show_banner();
    
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        show_usage();
        process::exit(1);
    }
    
    let command = &args[1];
    
    match command.as_str() {
        "check" => {
            if args.len() != 4 {
                eprintln!("{} Usage: {} check <file1> <file2>", "Error:".red().bold(), args[0]);
                process::exit(1);
            }
            
            let file1 = &args[2];
            let file2 = &args[3];
            
            match run_check(file1, file2) {
                Ok(_) => {},
                Err(e) => {
                    eprintln!("{} Failed to check entanglement: {}", "Error:".red().bold(), e);
                    process::exit(1);
                }
            }
        },
        "check-inline" => {
            if args.len() != 4 {
                eprintln!("{} Usage: {} check-inline <code1> <code2>", "Error:".red().bold(), args[0]);
                process::exit(1);
            }
            
            let code1 = &args[2];
            let code2 = &args[3];
            
            match run_inline_check(code1, code2) {
                Ok(_) => {},
                Err(e) => {
                    eprintln!("{} Failed to check inline entanglement: {}", "Error:".red().bold(), e);
                    process::exit(1);
                }
            }
        },
        "report" => {
            if args.len() != 4 {
                eprintln!("{} Usage: {} report <file1> <file2>", "Error:".red().bold(), args[0]);
                process::exit(1);
            }
            
            let file1 = &args[2];
            let file2 = &args[3];
            
            match run_report(file1, file2) {
                Ok(_) => {},
                Err(e) => {
                    eprintln!("{} Failed to generate report: {}", "Error:".red().bold(), e);
                    process::exit(1);
                }
            }
        },
        _ => {
            eprintln!("{} Unknown command: {}", "Error:".red().bold(), command);
            show_usage();
            process::exit(1);
        }
    }
}

fn run_check(file1: &str, file2: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("{} Checking quantum entanglement between '{}' and '{}'", "🔬".cyan(), file1.blue().bold(), file2.blue().bold());
    
    let content1 = read_file(file1)?;
    let content2 = read_file(file2)?;
    
    let checker = QuantumChecker::new();
    let result = checker.check_entanglement(&content1, &content2);
    
    display_result(&result);
    
    Ok(())
}

fn run_inline_check(code1: &str, code2: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("{} Checking quantum entanglement between inline code snippets", "🔬".cyan());
    
    let checker = QuantumChecker::new();
    let result = checker.check_entanglement(code1, code2);
    
    display_result(&result);
    
    Ok(())
}

fn run_report(file1: &str, file2: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("{} Generating quantum entanglement report for '{}' and '{}'", "📊".cyan(), file1.blue().bold(), file2.blue().bold());
    
    let content1 = read_file(file1)?;
    let content2 = read_file(file2)?;
    
    let checker = QuantumChecker::new();
    let result = checker.generate_report(&content1, &content2);
    
    display_report(&result);
    
    Ok(())
}

fn display_result(result: &quantum_checker::EntanglementResult) {
    println!("\n{} {}", "Status:".bold(), if result.is_entangled { "Entangled".green().bold() } else { "Not Entangled".red().bold() });
    println!("{} {:.2}{}", "Similarity:".bold(), result.similarity_percentage, "%".bold());
    println!("{} {}", "Hash 1:".bold(), result.hash1.bright_yellow());
    println!("{} {}", "Hash 2:".bold(), result.hash2.bright_yellow());
    
    if result.is_entangled {
        println!("{} {}", "🎉".green(), "Quantum entanglement detected! These code snippets are mysteriously connected!".bright_green());
    } else {
        println!("{} {}", "🌌".blue(), "No quantum entanglement found. These code snippets exist in separate quantum states.".bright_blue());
    }
    
    println!("\n{} {}", "🔮".purple(), result.quantum_message.bright_purple());
}

fn display_report(report: &quantum_checker::EntanglementReport) {
    println!("\n{} Quantum Entanglement Analysis Report", "📋".cyan().bold());
    println!("{} {}", "=".repeat(50).bright_cyan(), "=".repeat(50).bright_cyan());
    
    println!("\n{} {}", "Status:".bold(), if report.result.is_entangled { "Entangled".green().bold() } else { "Not Entangled".red().bold() });
    println!("{} {:.2}{}", "Similarity:".bold(), report.result.similarity_percentage, "%".bold());
    
    println!("\n{}", "Hash Signatures:".bold().underline());
    println!("{} {}", "Code 1:".bold(), report.result.hash1.bright_yellow());
    println!("{} {}", "Code 2:".bold(), report.result.hash2.bright_yellow());
    
    println!("\n{}", "Quantum Analysis:".bold().underline());
    println!("{} {}", "Entanglement Level:".bold(), report.entanglement_level.bright_magenta());
    println!("{} {}", "Quantum Signature:".bold(), report.quantum_signature.bright_cyan());
    
    println!("\n{} {}", "🔮".purple(), report.result.quantum_message.bright_purple());
    
    if report.result.is_entangled {
        println!("\n{} {}", "💡".yellow(), "Recommendation: These code snippets should be treated as a single quantum system.".bright_yellow());
    } else {
        println!("\n{} {}", "💡".yellow(), "Recommendation: These code snippets can be managed independently.".bright_yellow());
    }
}
