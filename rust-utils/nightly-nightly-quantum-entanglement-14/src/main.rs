use std::env;
use std::fs;
use std::path::Path;
use std::process;
use std::collections::HashMap;

mod quantum_engine;
mod cli;

use quantum_engine::{QuantumEntanglementChecker, EntanglementReport};
use cli::{parse_args, Command, Args};

fn main() {
    let args = parse_args();
    
    match execute_command(&args) {
        Ok(_) => {
            println!("\n✅ Operation completed successfully!");
        }
        Err(e) => {
            eprintln!("\n❌ Error: {}", e);
            process::exit(1);
        }
    }
}

fn execute_command(args: &Args) -> Result<(), Box<dyn std::error::Error>> {
    match &args.command {
        Command::Check { file1, file2, decoherence } => {
            println!("\n🔬 Quantum Entanglement Analysis Report");
            println!("=====================================");
            
            let checker = QuantumEntanglementChecker::new();
            let report = checker.check_entanglement(file1, file2, *decoherence)?;
            
            print_entanglement_report(&report);
        }
        
        Command::Report { file1, file2, output } => {
            println!("\n📊 Generating quantum entanglement report...");
            
            let checker = QuantumEntanglementChecker::new();
            let report = checker.check_entanglement(file1, file2, 0.0)?;
            
            let json = serde_json::to_string_pretty(&report)?;
            fs::write(output, json)?;
            
            println!("\n📄 Report saved to: {}", output);
        }
    }
    
    Ok(())
}

fn print_entanglement_report(report: &EntanglementReport) {
    println!("\nFile 1: {}", report.file1_name);
    println!("File 2: {}", report.file2_name);
    
    if report.is_entangled {
        println!("\nQuantum State: Superposition Detected ✓");
    } else {
        println!("\nQuantum State: Classical Separation ✗");
    }
    
    println!("Entanglement Level: {:.1}%", report.entanglement_level * 100.0);
    println!("Quantum Coherence: {}", report.coherence_state);
    println!("Probability of Quantum Tunneling: {:.1}%", report.tunneling_probability * 100.0);
    println!("Decoherence Factor: {:.1}", report.decoherence_factor);
    
    if report.is_entangled {
        println!("\nConclusion: These code snippets are quantumly entangled!");
    } else {
        println!("\nConclusion: These code snippets are not quantumly entangled.");
    }
}
