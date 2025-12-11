use quantum_entanglement_checker::{QuantumEntanglementChecker, EntanglementResult};
use serde_json;
use std::env;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        print_usage();
        process::exit(1);
    }
    
    let command = &args[1];
    
    match command.as_str() {
        "check" => {
            if args.len() != 4 {
                eprintln!("Usage: {} check <file1> <file2>", args[0]);
                process::exit(1);
            }
            
            let file1 = &args[2];
            let file2 = &args[3];
            
            let checker = QuantumEntanglementChecker::new(0.5);
            
            match checker.check_entanglement(file1, file2) {
                Some(result) => {
                    let json = serde_json::to_string_pretty(&result).unwrap();
                    println!("{}
", json);
                    
                    println!("🔬 Quantum Entanglement Analysis:");
                    println!("  File 1: {}", result.file1);
                    println!("  File 2: {}", result.file2);
                    println!("  Entanglement Score: {:.2}", result.entanglement_score);
                    println!("  Quantum State:");
                    println!("    Amplitude: {:.3}", result.quantum_state.amplitude);
                    println!("    Phase: {:.3}", result.quantum_state.phase);
                    println!("    Probability: {:.3}", result.quantum_state.probability);
                    println!("  Correlation Details:");
                    println!("    Content Similarity: {:.2}", result.correlation_details.content_similarity);
                    println!("    Metadata Correlation: {:.2}", result.correlation_details.metadata_correlation);
                    println!("    Pattern Matching: {:.2}", result.correlation_details.pattern_matching);
                    println!("    Quantum Interference: {:.2}", result.correlation_details.quantum_interference);
                }
                None => {
                    eprintln!("❌ Could not analyze one or both files");
                    process::exit(1);
                }
            }
        }
        
        "network" => {
            if args.len() < 3 {
                eprintln!("Usage: {} network <directory> [threshold]", args[0]);
                process::exit(1);
            }
            
            let dir = &args[2];
            let threshold = if args.len() > 3 {
                args[3].parse().unwrap_or(0.5)
            } else {
                0.5
            };
            
            let checker = QuantumEntanglementChecker::new(threshold);
            let results = checker.find_entangled_files(dir, Some(threshold));
            
            if results.is_empty() {
                println!("No entangled files found in directory: {}", dir);
                return;
            }
            
            println!("🕸️  Found {} entangled file pairs:
", results.len());
            
            for result in results.iter().take(10) {
                println!("🔗 {} ↔ {} (Score: {:.2})", 
                    result.file1, result.file2, result.entanglement_score);
            }
            
            if results.len() > 10 {
                println!("... and {} more", results.len() - 10);
            }
            
            // Save results to JSON file
            let json = serde_json::to_string_pretty(&results).unwrap();
            std::fs::write("data/entanglement.json", json).unwrap();
            println!("\n💾 Results saved to data/entanglement.json");
        }
        
        "visualize" => {
            if args.len() != 3 {
                eprintln!("Usage: {} visualize <graph_file>", args[0]);
                process::exit(1);
            }
            
            let graph_file = &args[2];
            
            match std::fs::read_to_string(graph_file) {
                Ok(content) => {
                    let results: Vec<EntanglementResult> = serde_json::from_str(&content).unwrap();
                    
                    println!("📊 Entanglement Graph Visualization:");
                    println!("\nNodes: {} files", results.len() * 2);
                    println!("Edges: {} entanglements", results.len());
                    
                    for result in results.iter().take(5) {
                        println!("  {} --[ {:.2} ]--> {}", 
                            result.file1, result.entanglement_score, result.file2);
                    }
                    
                    if results.len() > 5 {
                        println!("  ... and {} more connections", results.len() - 5);
                    }
                }
                Err(e) => {
                    eprintln!("❌ Could not read graph file: {}", e);
                    process::exit(1);
                }
            }
        }
        
        _ => {
            eprintln!("Unknown command: {}", command);
            print_usage();
            process::exit(1);
        }
    }
}

fn print_usage() {
    println!("Quantum Entanglement Checker");
    println!("\nUsage:");
    println!("  quantum_entanglement_checker check <file1> <file2>     Check entanglement between two files");
    println!("  quantum_entanglement_checker network <dir> [threshold]  Generate entanglement network");
    println!("  quantum_entanglement_checker visualize <graph_file>     Visualize entanglement graph");
    println!("\nExamples:");
    println!("  quantum_entanglement_checker check README.md LICENSE");
    println!("  quantum_entanglement_checker network src --threshold 0.5");
    println!("  quantum_entanglement_checker visualize data/entanglement.json");
}
