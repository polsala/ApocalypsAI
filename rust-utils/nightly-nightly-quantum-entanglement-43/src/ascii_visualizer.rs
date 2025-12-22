use crate::quantum_simulator::{QuantumState, Gate};

pub fn draw_circuit(gates: &[Gate], num_qubits: usize) {
    println!("\nCircuit Diagram:");
    println!("{}");

    // Create a grid for the circuit
    let mut grid = vec![vec!["   ".to_string(); gates.len() + 2]; num_qubits];

    // Draw qubit lines
    for i in 0..num_qubits {
        grid[i][0] = format!("q{}: ", i);
        for j in 1..=gates.len() + 1 {
            grid[i][j] = "───".to_string();
        }
    }

    // Place gates
    for (gate_idx, gate) in gates.iter().enumerate() {
        match gate {
            Gate::Hadamard(qubit) => {
                if *qubit < num_qubits {
                    grid[*qubit][gate_idx + 1] = " H ".to_string();
                }
            },
            Gate::PauliX(qubit) => {
                if *qubit < num_qubits {
                    grid[*qubit][gate_idx + 1] = " X ".to_string();
                }
            },
            Gate::PauliY(qubit) => {
                if *qubit < num_qubits {
                    grid[*qubit][gate_idx + 1] = " Y ".to_string();
                }
            },
            Gate::PauliZ(qubit) => {
                if *qubit < num_qubits {
                    grid[*qubit][gate_idx + 1] = " Z ".to_string();
                }
            },
            Gate::CNOT(control, target) => {
                if *control < num_qubits && *target < num_qubits {
                    grid[*control][gate_idx + 1] = " ● ".to_string();
                    grid[*target][gate_idx + 1] = " X ".to_string();
                    // Draw connection line
                    let (min_q, max_q) = if control < target { (*control, *target) } else { (*target, *control) };
                    for q in (min_q + 1)..max_q {
                        grid[q][gate_idx + 1] = " │ ".to_string();
                    }
                }
            },
            Gate::CZ(control, target) => {
                if *control < num_qubits && *target < num_qubits {
                    grid[*control][gate_idx + 1] = " ● ".to_string();
                    grid[*target][gate_idx + 1] = " Z ".to_string();
                    // Draw connection line
                    let (min_q, max_q) = if control < target { (*control, *target) } else { (*target, *control) };
                    for q in (min_q + 1)..max_q {
                        grid[q][gate_idx + 1] = " │ ".to_string();
                    }
                }
            },
            Gate::SWAP(qubit1, qubit2) => {
                if *qubit1 < num_qubits && *qubit2 < num_qubits {
                    grid[*qubit1][gate_idx + 1] = " X ".to_string();
                    grid[*qubit2][gate_idx + 1] = " X ".to_string();
                    // Draw connection line
                    let (min_q, max_q) = if qubit1 < qubit2 { (*qubit1, *qubit2) } else { (*qubit2, *qubit1) };
                    for q in (min_q + 1)..max_q {
                        grid[q][gate_idx + 1] = " │ ".to_string();
                    }
                }
            },
        }
    }

    // Print the grid
    for row in grid {
        println!("{}", row.join(""));
    }

    println!("{}");
}

pub fn draw_state_vector(state: &QuantumState, num_qubits: usize) {
    println!("State Vector:");
    println!("{}");

    let probabilities = state.get_measurement_probabilities();
    let max_prob = probabilities.iter().fold(0.0, |a, &b| a.max(b));

    for (i, prob) in probabilities.iter().enumerate() {
        if *prob > 1e-10 {
            let binary = format!("{:0width$b}", i, width = num_qubits);
            let amplitude = state.amplitudes[i];
            let phase = if amplitude.im == 0.0 {
                if amplitude.re >= 0.0 { " + " } else { " - " }
            } else {
                " ∠ " // Phase indicator
            };

            let bar_length = if max_prob > 0.0 {
                (prob / max_prob * 40.0) as usize
            } else {
                0
            };

            let bar = "█".repeat(bar_length);

            println!("  |{}⟩: {}{}{:.4} + {:.4}i  [{}]",
                binary,
                phase,
                amplitude.re.abs(),
                amplitude.im,
                bar
            );
        }
    }

    println!("{}");
}

pub fn draw_entanglement(state: &QuantumState, num_qubits: usize) {
    println!("Entanglement Analysis:");
    println!("{}");

    if state.is_entangled() {
        println!("  🌀 QUANTUM ENTANGLEMENT DETECTED! 🌀");
        println!("  ");
        println!("  This quantum state cannot be separated into individual qubit states.");
        println!("  The qubits are quantumly correlated!\n");

        let entangled_pairs = state.get_entangled_qubits();
        if !entangled_pairs.is_empty() {
            println!("  Entangled Qubit Pairs:");
            for (q1, q2) in entangled_pairs {
                println!("    Qubit {} ⟷ Qubit {}", q1, q2);
            }
        }

        // Show some interesting state properties
        let non_zero_states: Vec<usize> = state.amplitudes
            .iter()
            .enumerate()
            .filter(|(_, amp)| amp.magnitude_squared() > 1e-10)
            .map(|(i, _)| i)
            .collect();

        if non_zero_states.len() > 1 {
            println!("\n  Superposition States:");
            for &state_idx in &non_zero_states {
                let binary = format!("{:0width$b}", state_idx, width = num_qubits);
                let prob = state.probability(state_idx);
                println!("    |{}⟩ (probability: {:.1}%)", binary, prob * 100.0);
            }
        }
    } else {
        println!("  ✨ No entanglement detected.");
        println!("  ");
        println!("  All qubits are in separable states.");
        println!("  This is a product state.\n");

        // Show individual qubit states
        if num_qubits == 1 {
            let prob_0 = state.probability(0);
            let prob_1 = state.probability(1);
            println!("  Qubit 0:");
            println!("    |0⟩: {:.1}%", prob_0 * 100.0);
            println!("    |1⟩: {:.1}%", prob_1 * 100.0);
        }
    }

    println!("{}");
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::quantum_simulator::{QuantumState, Complex, Gate};

    #[test]
    fn test_draw_circuit() {
        let gates = vec![Gate::Hadamard(0), Gate::CNOT(0, 1)];
        draw_circuit(&gates, 2);
        // This test just ensures the function runs without panicking
    }

    #[test]
    fn test_draw_state_vector() {
        let mut state = QuantumState::new(2);
        // Create a simple state
        state.amplitudes[0] = Complex::new(1.0, 0.0);
        draw_state_vector(&state, 2);
        // This test just ensures the function runs without panicking
    }

    #[test]
    fn test_draw_entanglement() {
        let state = QuantumState::new(2);
        draw_entanglement(&state, 2);
        // This test just ensures the function runs without panicking
    }
}
