use std::env;
use std::process;

mod circuit;
mod quantum_state;
mod visualization;
mod parser;

use crate::circuit::QuantumCircuit;
use crate::visualization::QuantumVisualizer;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() == 1 {
        print_usage();
        return;
    }
    
    let mut circuit = QuantumCircuit::new();
    let mut visualizer = QuantumVisualizer::new();
    
    match args[1].as_str() {
        "--interactive" => run_interactive_mode(&mut circuit, &mut visualizer),
        "--circuit" => {
            if args.len() < 3 {
                eprintln!("Error: --circuit requires a circuit specification");
                print_usage();
                process::exit(1);
            }
            run_circuit_mode(&mut circuit, &mut visualizer, &args[2]);
        },
        "--help" | "-h" => print_usage(),
        _ => {
            eprintln!("Unknown option: {}", args[1]);
            print_usage();
            process::exit(1);
        }
    }
}

fn print_usage() {
    println!("Nightly Quantum Entanglement Simulator");
    println!("=====================================");
    println!("");
    println!("Usage:");
    println!("  {} --interactive          # Launch interactive mode", env::args().next().unwrap_or_else(|| "quantum_simulator".to_string()));
    println!("  {} --circuit <circuit>    # Run a specific circuit", env::args().next().unwrap_or_else(|| "quantum_simulator".to_string()));
    println!("  {} --help                 # Show this help", env::args().next().unwrap_or_else(|| "quantum_simulator".to_string()));
    println!("");
    println!("Circuit syntax:");
    println!("  H(n)      - Hadamard gate on qubit n");
    println!("  X(n)      - Pauli-X (NOT) gate on qubit n");
    println!("  Y(n)      - Pauli-Y gate on qubit n");
    println!("  Z(n)      - Pauli-Z gate on qubit n");
    println!("  CNOT(c,t) - CNOT gate with control c and target t");
    println!("  S(n)      - Phase (S) gate on qubit n");
    println!("  T(n)      - T gate on qubit n");
    println!("  measure(n) - Measure qubit n");
    println!("");
    println!("Examples:");
    println!("  {} --circuit \"H(0), CNOT(0,1)\"", env::args().next().unwrap_or_else(|| "quantum_simulator".to_string()));
    println!("  {} --circuit \"H(0), X(1), CNOT(0,1), measure(0), measure(1)\"", env::args().next().unwrap_or_else(|| "quantum_simulator".to_string()));
}

fn run_interactive_mode(circuit: &mut QuantumCircuit, visualizer: &mut QuantumVisualizer) {
    println!("\n🧪 Welcome to the Quantum Entanglement Simulator!");
    println!("Type 'help' for available commands, 'exit' to quit.\n");
    
    loop {
        print!("\n> ");
        std::io::Write::flush(&mut std::io::stdout()).unwrap();
        
        let mut input = String::new();
        match std::io::stdin().read_line(&mut input) {
            Ok(_) => {
                let input = input.trim();
                if input.is_empty() {
                    continue;
                }
                
                match input {
                    "exit" | "quit" => {
                        println!("\n🌌 Thanks for exploring the quantum realm!");
                        break;
                    },
                    "help" => print_interactive_help(),
                    "status" | "state" => {
                        visualizer.display_state(circuit);
                    },
                    "reset" => {
                        *circuit = QuantumCircuit::new();
                        println!("\n🔄 System reset to |000...⟩");
                    },
                    _ => {
                        if let Err(e) = run_command(circuit, visualizer, input) {
                            println!("❌ Error: {}", e);
                        }
                    }
                }
            },
            Err(error) => {
                println!("\n❌ Error reading input: {}", error);
                break;
            }
        }
    }
}

fn print_interactive_help() {
    println!("\n📚 Interactive Mode Commands:");
    println!("  H(n)      - Apply Hadamard gate to qubit n");
    println!("  X(n)      - Apply Pauli-X gate to qubit n");
    println!("  Y(n)      - Apply Pauli-Y gate to qubit n");
    println!("  Z(n)      - Apply Pauli-Z gate to qubit n");
    println!("  CNOT(c,t) - Apply CNOT gate (control c, target t)");
    println!("  S(n)      - Apply Phase gate to qubit n");
    println!("  T(n)      - Apply T gate to qubit n");
    println!("  measure(n) - Measure qubit n");
    println!("  circuit   - Show current circuit");
    println!("  state     - Show current quantum state");
    println!("  reset     - Reset system to |000...⟩");
    println!("  help      - Show this help");
    println!("  exit      - Exit interactive mode");
}

fn run_command(circuit: &mut QuantumCircuit, visualizer: &mut QuantumVisualizer, command: &str) -> Result<(), String> {
    if command.starts_with("measure") {
        // Handle measurement
        if let Some(qubit_str) = command.strip_prefix("measure(").and_then(|s| s.strip_suffix(')')) {
            let qubit: usize = qubit_str.parse().map_err(|_| format!("Invalid qubit number: {}", qubit_str))?;
            let result = circuit.measure(qubit);
            println!("\n🔬 Measured qubit {}: {}", qubit, if result { "|1⟩" } else { "|0⟩" });
            visualizer.display_state(circuit);
        } else {
            return Err("Invalid measure command. Use: measure(n)".to_string());
        }
    } else {
        // Parse and apply circuit
        let parsed_circuit = parser::parse_circuit(command)
            .map_err(|e| format!("Failed to parse circuit '{}': {}", command, e))?;
        
        for gate in parsed_circuit {
            circuit.apply_gate(gate);
        }
        
        println!("\n✅ Applied circuit: {}", command);
        visualizer.display_state(circuit);
    }
    
    Ok(())
}

fn run_circuit_mode(circuit: &mut QuantumCircuit, visualizer: &mut QuantumVisualizer, circuit_spec: &str) {
    println!("\n🧪 Quantum Circuit Simulator");
    println!("=============================");
    println!("Circuit: {}", circuit_spec);
    println!("\nInitial state: |000...⟩");
    
    match parser::parse_circuit(circuit_spec) {
        Ok(gates) => {
            for gate in gates {
                circuit.apply_gate(gate);
            }
            
            println!("\n✅ Circuit execution completed!");
            visualizer.display_state(circuit);
        },
        Err(e) => {
            println!("❌ Failed to parse circuit '{}': {}", circuit_spec, e);
            process::exit(1);
        }
    }
}
