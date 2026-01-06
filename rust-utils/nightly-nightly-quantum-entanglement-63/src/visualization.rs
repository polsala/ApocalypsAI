use crate::quantum_state::QuantumState;
use std::collections::HashSet;

pub struct QuantumVisualizer;

impl QuantumVisualizer {
    pub fn new() -> Self {
        Self
    }
    
    pub fn display_state(&self, circuit: &crate::circuit::QuantumCircuit) {
        let state = circuit.get_state();
        let num_qubits = circuit.get_num_qubits();
        
        println!("\n{}", "=".repeat(50));
        println!("🔮 QUANTUM STATE VISUALIZATION");
        println!("{}", "=".repeat(50));
        
        // Display individual qubit states
        self.display_individual_qubits(state, num_qubits);
        
        // Check for entanglement
        let entangled_pairs = self.detect_entanglement(state, num_qubits);
        if !entangled_pairs.is_empty() {
            self.display_entanglement_info(&entangled_pairs);
        }
        
        // Display probability cloud
        self.display_probability_cloud(state, num_qubits);
        
        // Display ASCII art
        self.display_quantum_ascii_art(state, num_qubits);
    }
    
    fn display_individual_qubits(&self, state: &QuantumState, num_qubits: usize) {
        println!("\n🧩 Individual Qubit States:");
        
        for qubit in 0..num_qubits {
            let (alpha, beta) = self.get_qubit_amplitudes(state, qubit);
            let prob_0 = alpha.norm_sqr();
            let prob_1 = beta.norm_sqr();
            
            let spin_indicator = if prob_0 > prob_1 { "↑" } else { "↓" };
            
            println!("  Qubit {}: |{}⟩  (α = {:.3} + {:.3}i, |α|² = {:.2})",
                     qubit, spin_indicator, alpha.re, alpha.im, prob_0);
            println!("           (β = {:.3} + {:.3}i, |β|² = {:.2})",
                     beta.re, beta.im, prob_1);
        }
    }
    
    fn get_qubit_amplitudes(&self, state: &QuantumState, qubit: usize) -> (num_complex::Complex<f64>, num_complex::Complex<f64>) {
        let mut alpha = num_complex::Complex::new(0.0, 0.0);
        let mut beta = num_complex::Complex::new(0.0, 0.0);
        
        for i in 0..state.amplitudes.len() {
            let amplitude = state.amplitudes[i];
            if (i >> qubit) & 1 == 0 {
                alpha += amplitude;
            } else {
                beta += amplitude;
            }
        }
        
        (alpha, beta)
    }
    
    fn detect_entanglement(&self, state: &QuantumState, num_qubits: usize) -> Vec<(usize, usize)> {
        let mut entangled_pairs = Vec::new();
        
        for i in 0..num_qubits {
            for j in (i + 1)..num_qubits {
                if self.is_entangled(state, i, j) {
                    entangled_pairs.push((i, j));
                }
            }
        }
        
        entangled_pairs
    }
    
    fn is_entangled(&self, state: &QuantumState, qubit1: usize, qubit2: usize) -> bool {
        // Simple entanglement detection: check if the state can be written as a product state
        // This is a simplified check for educational purposes
        
        let mut has_00 = false;
        let mut has_01 = false;
        let mut has_10 = false;
        let mut has_11 = false;
        
        for i in 0..state.amplitudes.len() {
            let prob = state.amplitudes[i].norm_sqr();
            if prob > 1e-10 {
                let bit1 = (i >> qubit1) & 1;
                let bit2 = (i >> qubit2) & 1;
                
                match (bit1, bit2) {
                    (0, 0) => has_00 = true,
                    (0, 1) => has_01 = true,
                    (1, 0) => has_10 = true,
                    (1, 1) => has_11 = true,
                }
            }
        }
        
        // If we have all four combinations or specific non-product patterns, likely entangled
        (has_00 && has_11 && !(has_01 || has_10)) ||
        (has_01 && has_10 && !(has_00 || has_11)) ||
        (has_00 && has_01 && has_10 && has_11)
    }
    
    fn display_entanglement_info(&self, entangled_pairs: &[(usize, usize)]) {
        println!("\n🌀 ENTANGLEMENT DETECTED!");
        println!("The following qubit pairs are quantumly entwined:");
        
        for &(q1, q2) in entangled_pairs {
            println!("  • Qubits {} and {} are in a quantum embrace! 🤝", q1, q2);
        }
        
        println!("\n💡 Quantum entanglement means measuring one qubit instantly\n   affects its partner, no matter the distance!");
    }
    
    fn display_probability_cloud(&self, state: &QuantumState, num_qubits: usize) {
        println!("\n☁️  PROBABILITY CLOUD:");
        
        let mut probabilities = Vec::new();
        for i in 0..state.amplitudes.len() {
            let prob = state.amplitudes[i].norm_sqr();
            if prob > 1e-6 {
                let binary = format!("{:0width$b}", i, width = num_qubits);
                probabilities.push((binary, prob));
            }
        }
        
        probabilities.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        
        for (state_str, prob) in probabilities {
            println!("  |{}⟩: {:.2}%", state_str, prob * 100.0);
        }
    }
    
    fn display_quantum_ascii_art(&self, state: &QuantumState, num_qubits: usize) {
        println!("\n🎨 QUANTUM VISUALIZATION:");
        
        // Simple ASCII representation of the quantum state
        let max_prob = state.amplitudes.iter().map(|a| a.norm_sqr()).fold(0.0, |a, b| a.max(b));
        
        for qubit in 0..num_qubits {
            let (alpha, beta) = self.get_qubit_amplitudes(state, qubit);
            let prob_0 = alpha.norm_sqr();
            let prob_1 = beta.norm_sqr();
            
            let bar_0 = "█".repeat((prob_0 / max_prob * 20.0) as usize);
            let bar_1 = "█".repeat((prob_1 / max_prob * 20.0) as usize);
            
            println!("  Qubit {}: |0⟩ [{}] {:.1}%", qubit, bar_0, prob_0 * 100.0);
            println!("           |1⟩ [{}] {:.1}%", bar_1, prob_1 * 100.0);
        }
        
        println!("\n🌌 Remember: observing changes the state!".cyan());
    }
}

// Add color support for terminal output
trait Colorize {
    fn cyan(&self) -> String;
    fn magenta(&self) -> String;
    fn green(&self) -> String;
    fn yellow(&self) -> String;
}

impl Colorize for str {
    fn cyan(&self) -> String {
        format!("\x1b[36m{}\x1b[0m", self)
    }
    
    fn magenta(&self) -> String {
        format!("\x1b[35m{}\x1b[0m", self)
    }
    
    fn green(&self) -> String {
        format!("\x1b[32m{}\x1b[0m", self)
    }
    
    fn yellow(&self) -> String {
        format!("\x1b[33m{}\x1b[0m", self)
    }
}
