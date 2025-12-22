use std::env;
use std::fs;
use std::io::{self, Write};
use std::collections::HashMap;

mod quantum_simulator;
mod circuit_parser;
mod ascii_visualizer;

use quantum_simulator::{QuantumSimulator, QuantumState};
use circuit_parser::parse_circuit;
use ascii_visualizer::{draw_circuit, draw_state_vector, draw_entanglement};

#[derive(Debug)]
struct Config {
    qubits: usize,
    gates: Vec<String>,
    interactive: bool,
    file: Option<String>,
}

impl Config {
    fn new() -> Self {
        Self {
            qubits: 0,
            gates: Vec::new(),
            interactive: false,
            file: None,
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let config = parse_args(&args);

    if config.interactive {
        run_interactive_mode();
    } else if let Some(file_path) = &config.file {
        run_from_file(file_path);
    } else {
        run_circuit_simulation(config);
    }
}

fn parse_args(args: &[String]) -> Config {
    let mut config = Config::new();
    let mut i = 1;

    while i < args.len() {
        match args[i].as_str() {
            "--qubits" => {
                if i + 1 < args.len() {
                    config.qubits = args[i + 1].parse().expect("Invalid number of qubits");
                    i += 2;
                } else {
                    eprintln!("Error: --qubits requires a number");
                    std::process::exit(1);
                }
            }
            "--gates" => {
                if i + 1 < args.len() {
                    let gates_str = &args[i + 1];
                    config.gates = gates_str.split_whitespace().map(|s| s.to_string()).collect();
                    i += 2;
                } else {
                    eprintln!("Error: --gates requires a gate sequence");
                    std::process::exit(1);
                }
            }
            "--interactive" => {
                config.interactive = true;
                i += 1;
            }
            "--file" => {
                if i + 1 < args.len() {
                    config.file = Some(args[i + 1].clone());
                    i += 2;
                } else {
                    eprintln!("Error: --file requires a file path");
                    std::process::exit(1);
                }
            }
            _ => {
                eprintln!("Unknown argument: {}", args[i]);
                print_usage();
                std::process::exit(1);
            }
        }
    }

    if config.qubits == 0 && config.file.is_none() && !config.interactive {
        print_usage();
        std::process::exit(1);
    }

    config
}

fn print_usage() {
    println!("Quantum Entanglement Simulator");
    println!("Usage:");
    println!("  quantum_sim --qubits N --gates <gate_sequence>");
    println!("  quantum_sim --interactive");
    println!("  quantum_sim --file <circuit_file.json>");
    println!("\nExamples:");
    println!("  quantum_sim --qubits 2 --gates h(0) cx(0,1)");
    println!("  quantum_sim --qubits 3 --gates h(0) cx(0,1) cx(1,2)");
}

fn run_circuit_simulation(config: Config) {
    if config.qubits == 0 {
        eprintln!("Error: Number of qubits must be specified");
        std::process::exit(1);
    }

    let mut simulator = QuantumSimulator::new(config.qubits);

    println!("\n{}", "=".repeat(60));
    println!("  QUANTUM ENTANGLEMENT SIMULATOR");
    println!("{}", "=".repeat(60));

    // Parse and apply gates
    let gates = parse_circuit(&config.gates);
    
    println!("\nCircuit Definition:");
    println!("{}", config.gates.join(" "));

    // Draw initial circuit
    draw_circuit(&gates, config.qubits);

    // Apply gates
    for gate in &gates {
        simulator.apply_gate(gate);
    }

    // Display results
    println!("\n{}", "-".repeat(60));
    println!("  QUANTUM STATE ANALYSIS");
    println!("{}", "-".repeat(60));

    let state = simulator.get_state();
    draw_state_vector(&state, config.qubits);

    println!("\n{}", "-".repeat(60));
    println!("  ENTANGLEMENT ANALYSIS");
    println!("{}", "-".repeat(60));

    draw_entanglement(&state, config.qubits);

    // Measurement simulation
    println!("\n{}", "-".repeat(60));
    println!("  MEASUREMENT SIMULATION");
    println!("{}", "-".repeat(60));

    let measurements = simulator.measure(1000);
    println!("\nMeasurement Results (1000 trials):\n");
    for (outcome, count) in measurements {
        let probability = count as f64 / 1000.0;
        println!("  |{}⟩: {} times ({:.1}%)", outcome, count, probability * 100.0);
    }
}

fn run_interactive_mode() {
    println!("\n{}", "=".repeat(60));
    println!("  INTERACTIVE QUANTUM SIMULATOR");
    println!("{}", "=".repeat(60));
    println!("\nCommands:");
    println!("  qubits N     - Set number of qubits");
    println!("  gate GATE    - Add a gate (e.g., h(0), cx(0,1))");
    println!("  run          - Execute the circuit");
    println!("  reset        - Reset to initial state");
    println!("  help         - Show this help");
    println!("  quit         - Exit");

    let mut simulator = None;
    let mut gates = Vec::new();
    let mut qubits = 0;

    loop {
        print!("\nquantum> ");
        io::stdout().flush().unwrap();

        let mut input = String::new();
        if io::stdin().read_line(&mut input).is_err() {
            break;
        }

        let input = input.trim();
        let parts: Vec<&str> = input.split_whitespace().collect();

        if parts.is_empty() {
            continue;
        }

        match parts[0] {
            "quit" | "exit" => break,
            "help" => {
                println!("\nCommands:");
                println!("  qubits N     - Set number of qubits");
                println!("  gate GATE    - Add a gate (e.g., h(0), cx(0,1))");
                println!("  run          - Execute the circuit");
                println!("  reset        - Reset to initial state");
                println!("  help         - Show this help");
                println!("  quit         - Exit");
            },
            "qubits" => {
                if parts.len() != 2 {
                    println!("Usage: qubits N");
                    continue;
                }
                match parts[1].parse::<usize>() {
                    Ok(n) => {
                        qubits = n;
                        simulator = Some(QuantumSimulator::new(n));
                        gates.clear();
                        println!("Set {} qubits", n);
                    },
                    Err(_) => println!("Invalid number of qubits"),
                }
            },
            "gate" => {
                if parts.len() < 2 {
                    println!("Usage: gate GATE");
                    continue;
                }
                let gate_str = parts[1..].join(" ");
                gates.push(gate_str);
                println!("Added gate: {}", gate_str);
            },
            "run" => {
                if qubits == 0 {
                    println!("Set number of qubits first");
                    continue;
                }
                if let Some(ref mut sim) = simulator {
                    run_simulation(sim, &gates, qubits);
                }
            },
            "reset" => {
                simulator = None;
                gates.clear();
                qubits = 0;
                println!("Reset complete");
            },
            _ => println!("Unknown command: {}. Type 'help' for available commands.", parts[0]),
        }
    }
}

fn run_simulation(simulator: &mut QuantumSimulator, gates: &[String], qubits: usize) {
    println!("\n{}", "=".repeat(60));
    println!("  EXECUTING QUANTUM CIRCUIT");
    println!("{}", "=".repeat(60));

    // Parse gates
    let parsed_gates = parse_circuit(gates);
    
    println!("\nCircuit:");
    for gate in gates {
        println!("  {}", gate);
    }

    // Draw circuit
    draw_circuit(&parsed_gates, qubits);

    // Apply gates
    for gate in &parsed_gates {
        simulator.apply_gate(gate);
    }

    // Display results
    println!("\n{}", "-".repeat(60));
    println!("  QUANTUM STATE ANALYSIS");
    println!("{}", "-".repeat(60));

    let state = simulator.get_state();
    draw_state_vector(&state, qubits);

    println!("\n{}", "-".repeat(60));
    println!("  ENTANGLEMENT ANALYSIS");
    println!("{}", "-".repeat(60));

    draw_entanglement(&state, qubits);

    // Measurement simulation
    println!("\n{}", "-".repeat(60));
    println!("  MEASUREMENT SIMULATION");
    println!("{}", "-".repeat(60));

    let measurements = simulator.measure(1000);
    println!("\nMeasurement Results (1000 trials):\n");
    for (outcome, count) in measurements {
        let probability = count as f64 / 1000.0;
        println!("  |{}⟩: {} times ({:.1}%)", outcome, count, probability * 100.0);
    }
}

fn run_from_file(file_path: &str) {
    match fs::read_to_string(file_path) {
        Ok(content) => {
            match serde_json::from_str::<serde_json::Value>(&content) {
                Ok(json) => {
                    if let Some(circuit) = json.as_object() {
                        if let (Some(qubits_val), Some(gates_val)) = (circuit.get("qubits"), circuit.get("gates")) {
                            if let (Some(qubits), Some(gates)) = (qubits_val.as_u64(), gates_val.as_array()) {
                                let gates_str: Vec<String> = gates.iter()
                                    .filter_map(|g| g.as_str())
                                    .map(|s| s.to_string())
                                    .collect();
                                
                                let config = Config {
                                    qubits: qubits as usize,
                                    gates: gates_str,
                                    interactive: false,
                                    file: None,
                                };
                                run_circuit_simulation(config);
                            } else {
                                eprintln!("Invalid JSON format: qubits must be a number, gates must be an array of strings");
                            }
                        } else {
                            eprintln!("Invalid JSON format: expected {\"qubits\": N, \"gates\": [...] }");
                        }
                    } else {
                        eprintln!("Invalid JSON format");
                    }
                },
                Err(e) => eprintln!("Error parsing JSON: {}", e),
            }
        },
        Err(e) => eprintln!("Error reading file: {}", e),
    }
}
