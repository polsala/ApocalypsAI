use std::collections::HashMap;
use std::env;
use std::process;

mod quantum_simulator;
mod cli;

use quantum_simulator::{QuantumEntanglementChecker, QuantumConfig};
use cli::{parse_args, CliArgs};

fn main() {
    let args = parse_args();
    
    if args.verbose {
        println!("🔬 Quantum Entanglement Verification Protocol");
        println!("==========================================");
        println!("");
    }
    
    if args.batch_mode {
        run_batch_mode(args);
    } else {
        run_single_check(args);
    }
}

fn run_single_check(args: CliArgs) {
    let config = QuantumConfig {
        decoherence: args.decoherence,
        measurements: args.measurements,
        verbose: args.verbose,
    };
    
    let mut checker = QuantumEntanglementChecker::new(config);
    
    match checker.verify_entanglement(&args.node_a, &args.node_b) {
        Ok(result) => {
            print_results(&args.node_a, &args.node_b, &result);
        }
        Err(e) => {
            eprintln!("❌ Quantum verification failed: {}", e);
            process::exit(1);
        }
    }
}

fn run_batch_mode(args: CliArgs) {
    let config = QuantumConfig {
        decoherence: args.decoherence,
        measurements: args.measurements,
        verbose: args.verbose,
    };
    
    let mut checker = QuantumEntanglementChecker::new(config);
    
    // For batch mode, we need to extract all node pairs from args
    // In a real implementation, this would parse multiple --node-a/--node-b pairs
    let node_pairs = vec![(args.node_a.clone(), args.node_b.clone())];
    
    let mut all_results = HashMap::new();
    
    for (node_a, node_b) in node_pairs {
        match checker.verify_entanglement(&node_a, &node_b) {
            Ok(result) => {
                all_results.insert(format!("{} ↔ {}", node_a, node_b), result);
            }
            Err(e) => {
                eprintln!("❌ Failed to verify entanglement between {} and {}: {}", 
                         node_a, node_b, e);
            }
        }
    }
    
    print_batch_results(&all_results);
}

fn print_results(node_a: &str, node_b: &str, result: &quantum_simulator::EntanglementResult) {
    println!("📡 Node A: \"{}\" (Qubit ID: {})", node_a, result.qubit_a_id);
    println!("📡 Node B: \"{}\"  (Qubit ID: {})", node_b, result.qubit_b_id);
    println!("");
    
    if result.verbose {
        println!("🧪 Initializing quantum superposition...");
        println!("✨ Entangling qubits via quantum teleportation...");
        println!("");
        println!("📊 Running {} quantum measurements...", result.measurements);
        println!("");
    }
    
    println!("Results:");
    println!("- Correlation coefficient: {:.3}", result.correlation);
    println!("- Bell inequality violation: {:.2} (threshold: 2.0)", result.bell_inequality);
    println!("- Decoherence factor: {:.2}", result.decoherence);
    
    let status_emoji = if result.entangled { "✅" } else { "❌" };
    let status_text = if result.entangled { "VERIFIED" } else { "FAILED" };
    println!("- Entanglement status: {} {}", status_emoji, status_text);
    println!("");
    
    if result.entangled {
        println!("🎉 Spooky action at a distance confirmed!");
    } else {
        println!("😞 Classical correlation detected. Try reducing decoherence.");
    }
}

fn print_batch_results(results: &HashMap<String, quantum_simulator::EntanglementResult>) {
    println!("\n📊 Batch Entanglement Verification Results");
    println!("=========================================");
    println!("");
    
    let mut entangled_count = 0;
    let total_count = results.len();
    
    for (pair, result) in results {
        let status = if result.entangled { "✅" } else { "❌" };
        println!("{} {}: {:.3}", status, pair, result.correlation);
        
        if result.entangled {
            entangled_count += 1;
        }
    }
    
    println!("");
    println!("Summary: {} out of {} pairs successfully entangled", 
             entangled_count, total_count);
    
    if entangled_count == total_count {
        println!("🎉 All quantum connections are spookily correlated!");
    } else {
        println!("⚠️  Some classical interference detected. Check your quantum isolation.");
    }
}
