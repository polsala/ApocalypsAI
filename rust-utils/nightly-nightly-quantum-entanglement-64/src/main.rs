use nightly_quantum_entanglement_simulator::*;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    // Parse command line arguments
    let mut circuit = QuantumCircuit::new(2);
    let mut show_help = false;
    let mut example_name = None;
    let mut num_qubits = 2;
    let mut depth = 3;
    let mut seed = None;
    
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--help" | "-h" => show_help = true,
            "--example" | "-e" => {
                if i + 1 < args.len() {
                    example_name = Some(args[i + 1].clone());
                    i += 1;
                }
            },
            "--qubits" | "-q" => {
                if i + 1 < args.len() {
                    num_qubits = args[i + 1].parse().unwrap_or(2);
                    i += 1;
                }
            },
            "--depth" | "-d" => {
                if i + 1 < args.len() {
                    depth = args[i + 1].parse().unwrap_or(3);
                    i += 1;
                }
            },
            "--seed" | "-s" => {
                if i + 1 < args.len() {
                    seed = Some(args[i + 1].parse().unwrap_or(42));
                    i += 1;
                }
            },
            _ => {},
        }
        i += 1;
    }
    
    if show_help {
        print_help();
        return;
    }
    
    // Handle examples
    if let Some(example) = example_name {
        match example.as_str() {
            "bell_state" => circuit = create_bell_state_circuit(),
            "ghz_state" => circuit = create_ghz_state_circuit(),
            "random_circuit" => {
                let mut rng = if let Some(s) = seed {
                    fastrand::Rng::with_seed(s)
                } else {
                    fastrand::Rng::new()
                };
                circuit = create_random_circuit(num_qubits, depth, &mut rng);
            },
            _ => {
                eprintln!("Unknown example: {}. Available: bell_state, ghz_state, random_circuit", example);
                std::process::exit(1);
            }
        }
    } else if num_qubits != 2 || depth != 3 || seed.is_some() {
        // Create custom circuit if parameters were specified
        let mut rng = if let Some(s) = seed {
            fastrand::Rng::with_seed(s)
        } else {
            fastrand::Rng::new()
        };
        circuit = create_random_circuit(num_qubits, depth, &mut rng);
    }
    
    // Run simulation
    println!("{}
", "=".repeat(60));
    println!("🧪 Quantum Entanglement Simulator");
    println!("{}
", "=".repeat(60));
    
    // Display circuit
    println!("{}
", circuit.visualize());
    
    // Simulate and measure
    let result = circuit.simulate();
    println!("{}
", result);
    
    // Check for entanglement
    let entanglement_info = circuit.detect_entanglement();
    if !entanglement_info.is_empty() {
        println!("🎉 Entanglement detected!");
        for (pair, concurrence) in entanglement_info {
            println!("   Qubits {:?}: concurrence = {:.3}", pair, concurrence);
        }
    } else {
        println!("😐 No entanglement detected.");
    }
}

fn print_help() {
    println!("Quantum Entanglement Simulator");
    println!("Usage: quantum_simulator [OPTIONS]");
    println!("");
    println!("OPTIONS:");
    println!("  --help, -h              Show this help message");
    println!("  --example, -e <NAME>    Run predefined example");
    println!("                          Available: bell_state, ghz_state, random_circuit");
    println!("  --qubits, -q <N>        Number of qubits (default: 2)");
    println!("  --depth, -d <N>         Circuit depth (default: 3)");
    println!("  --seed, -s <N>          Random seed for reproducible circuits");
    println!("");
    println!("EXAMPLES:");
    println!("  quantum_simulator --example bell_state");
    println!("  quantum_simulator --example ghz_state");
    println!("  quantum_simulator --example random_circuit --qubits 3 --depth 5");
    println!("  quantum_simulator --qubits 4 --depth 10 --seed 12345");
}

fn create_bell_state_circuit() -> QuantumCircuit {
    let mut circuit = QuantumCircuit::new(2);
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::CNOT(0, 1));
    circuit
}

fn create_ghz_state_circuit() -> QuantumCircuit {
    let mut circuit = QuantumCircuit::new(3);
    circuit.add_gate(Gate::Hadamard(0));
    circuit.add_gate(Gate::CNOT(0, 1));
    circuit.add_gate(Gate::CNOT(1, 2));
    circuit
}

fn create_random_circuit(num_qubits: usize, depth: usize, rng: &mut fastrand::Rng) -> QuantumCircuit {
    let mut circuit = QuantumCircuit::new(num_qubits);
    
    for _ in 0..depth {
        let gate_type = rng.u32(..100);
        
        match gate_type {
            0..=30 => {
                // Single qubit gates
                let qubit = rng.usize(..num_qubits);
                let gate = match rng.u32(..4) {
                    0 => Gate::Hadamard(qubit),
                    1 => Gate::PauliX(qubit),
                    2 => Gate::PauliY(qubit),
                    _ => Gate::PauliZ(qubit),
                };
                circuit.add_gate(gate);
            },
            31..=70 => {
                // Two qubit gates
                if num_qubits >= 2 {
                    let control = rng.usize(..num_qubits);
                    let target = loop {
                        let t = rng.usize(..num_qubits);
                        if t != control { break t; }
                    };
                    let gate = match rng.u32(..3) {
                        0 => Gate::CNOT(control, target),
                        1 => Gate::CZ(control, target),
                        _ => Gate::SWAP(control, target),
                    };
                    circuit.add_gate(gate);
                }
            },
            71..=100 => {
                // Multi-qubit gates
                if num_qubits >= 3 {
                    let control1 = rng.usize(..num_qubits);
                    let control2 = loop {
                        let c = rng.usize(..num_qubits);
                        if c != control1 { break c; }
                    };
                    let target = loop {
                        let t = rng.usize(..num_qubits);
                        if t != control1 && t != control2 { break t; }
                    };
                    circuit.add_gate(Gate::Toffoli(control1, control2, target));
                }
            },
        }
    }
    
    circuit
}
