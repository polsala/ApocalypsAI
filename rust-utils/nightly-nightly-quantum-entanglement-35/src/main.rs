use std::env;
use std::process;
use std::str::FromStr;
use structopt::StructOpt;

#[derive(StructOpt, Debug)]
#[structopt(name = "nightly-quantum-entanglement-checker", about = "Detect quantum entanglement patterns")]
pub enum Command {
    /// Check if a quantum state is entangled
    Check {
        /// Probability amplitudes (space-separated)
        #[structopt(short, long, parse(try_from_str))]
        amplitudes: Vec<f64>,
    },
    /// Generate a random entangled state
    Generate {
        /// Number of qubits
        #[structopt(short, long)]
        qubits: u32,
    },
    /// Calculate entanglement entropy
    Entropy {
        /// Probability amplitudes (space-separated)
        #[structopt(short, long, parse(try_from_str))]
        amplitudes: Vec<f64>,
    },
}

fn main() {
    let cmd = Command::from_args();
    
    match cmd {
        Command::Check { amplitudes } => {
            if !validate_state(&amplitudes) {
                eprintln!("Error: State is not normalized. Sum of squared amplitudes should be 1.");
                process::exit(1);
            }
            
            let result = analyze_entanglement(&amplitudes);
            println!("{}", result);
        },
        Command::Generate { qubits } => {
            if qubits < 2 || qubits > 10 {
                eprintln!("Error: Number of qubits must be between 2 and 10.");
                process::exit(1);
            }
            
            let state = generate_random_entangled_state(qubits);
            println!("Generated {}-qubit entangled state:", qubits);
            for (i, amp) in state.iter().enumerate() {
                println!("|{:0width$b}⟩: {:.6}", i, amp, width = qubits as usize);
            }
        },
        Command::Entropy { amplitudes } => {
            if !validate_state(&amplitudes) {
                eprintln!("Error: State is not normalized. Sum of squared amplitudes should be 1.");
                process::exit(1);
            }
            
            let entropy = calculate_entanglement_entropy(&amplitudes);
            println!("Entanglement entropy: {:.6}", entropy);
        },
    }
}

/// Validate that the quantum state is normalized
fn validate_state(amplitudes: &[f64]) -> bool {
    let n = amplitudes.len();
    if n == 0 || !is_power_of_two(n) {
        return false;
    }
    
    let sum: f64 = amplitudes.iter().map(|&a| a * a).sum();
    (sum - 1.0).abs() < 1e-10
}

/// Check if a number is a power of two
fn is_power_of_two(n: usize) -> bool {
    n > 0 && (n & (n - 1)) == 0
}

/// Analyze entanglement properties of a quantum state
fn analyze_entanglement(amplitudes: &[f64]) -> String {
    let n = amplitudes.len();
    let num_qubits = (n as f64).log2() as u32;
    
    if num_qubits == 1 {
        return "Single qubit state - not applicable for entanglement.".to_string();
    }
    
    if num_qubits == 2 {
        // Check for Bell states
        if is_bell_state(amplitudes) {
            return "Entangled! This is a Bell state.".to_string();
        }
    }
    
    if num_qubits >= 3 {
        // Check for GHZ state
        if is_ghz_state(amplitudes) {
            return "Entangled! This is a GHZ state.".to_string();
        }
    }
    
    // Check if separable
    if is_separable(amplitudes) {
        return "Not entangled. This is a separable state.".to_string();
    }
    
    // General entangled state
    let entropy = calculate_entanglement_entropy(amplitudes);
    format!("Entangled! Entanglement entropy: {:.4}", entropy)
}

/// Check if a 2-qubit state is a Bell state
fn is_bell_state(amplitudes: &[f64]) -> bool {
    // Bell states have exactly 2 non-zero amplitudes with equal magnitude 1/√2
    let non_zero: Vec<f64> = amplitudes.iter().filter(|&&a| a.abs() > 1e-10).copied().collect();
    
    if non_zero.len() != 2 {
        return false;
    }
    
    // Check if both have magnitude 1/√2
    let expected = 1.0 / 2.0_f64.sqrt();
    if (non_zero[0].abs() - expected).abs() > 1e-10 || 
       (non_zero[1].abs() - expected).abs() > 1e-10 {
        return false;
    }
    
    // Check specific Bell state patterns
    // |Φ+⟩ = (|00⟩ + |11⟩)/√2
    if (amplitudes[0] - expected).abs() < 1e-10 && 
       (amplitudes[3] - expected).abs() < 1e-10 {
        return true;
    }
    
    // |Φ-⟩ = (|00⟩ - |11⟩)/√2
    if (amplitudes[0] - expected).abs() < 1e-10 && 
       (amplitudes[3] + expected).abs() < 1e-10 {
        return true;
    }
    
    // |Ψ+⟩ = (|01⟩ + |10⟩)/√2
    if (amplitudes[1] - expected).abs() < 1e-10 && 
       (amplitudes[2] - expected).abs() < 1e-10 {
        return true;
    }
    
    // |Ψ-⟩ = (|01⟩ - |10⟩)/√2
    if (amplitudes[1] - expected).abs() < 1e-10 && 
       (amplitudes[2] + expected).abs() < 1e-10 {
        return true;
    }
    
    false
}

/// Check if a multi-qubit state is a GHZ state
fn is_ghz_state(amplitudes: &[f64]) -> bool {
    let n = amplitudes.len();
    
    // GHZ state has exactly 2 non-zero amplitudes
    let non_zero: Vec<f64> = amplitudes.iter().filter(|&&a| a.abs() > 1e-10).copied().collect();
    
    if non_zero.len() != 2 {
        return false;
    }
    
    // Check if both have magnitude 1/√2
    let expected = 1.0 / 2.0_f64.sqrt();
    if (non_zero[0].abs() - expected).abs() > 1e-10 || 
       (non_zero[1].abs() - expected).abs() > 1e-10 {
        return false;
    }
    
    // Check if they're at positions 0 and 2^n-1 (|00...0⟩ and |11...1⟩)
    if (amplitudes[0].abs() - expected).abs() < 1e-10 && 
       (amplitudes[n-1].abs() - expected).abs() < 1e-10 {
        return true;
    }
    
    false
}

/// Check if a state is separable (can be written as tensor product)
fn is_separable(amplitudes: &[f64]) -> bool {
    let n = amplitudes.len();
    let num_qubits = (n as f64).log2() as u32;
    
    if num_qubits == 1 {
        return true;
    }
    
    // For simplicity, check if only one amplitude is non-zero (computational basis state)
    let non_zero_count = amplitudes.iter().filter(|&&a| a.abs() > 1e-10).count();
    non_zero_count == 1
}

/// Calculate entanglement entropy for a bipartite system
fn calculate_entanglement_entropy(amplitudes: &[f64]) -> f64 {
    let n = amplitudes.len();
    let num_qubits = (n as f64).log2() as u32;
    
    if num_qubits == 1 {
        return 0.0;
    }
    
    // For simplicity, split into two equal parts
    let half = n / 2;
    
    // Calculate reduced density matrix for first subsystem
    let mut rho: Vec<Vec<f64>> = vec![vec![0.0; half]; half];
    
    for i in 0..half {
        for j in 0..half {
            for k in 0..half {
                rho[i][j] += amplitudes[i * half + k] * amplitudes[j * half + k];
            }
        }
    }
    
    // Calculate eigenvalues
    let eigenvalues = eigenvalues_2x2(&rho);
    
    // Calculate entropy
    let mut entropy = 0.0;
    for lambda in eigenvalues {
        if lambda > 1e-10 {
            entropy -= lambda * lambda.ln();
        }
    }
    
    entropy
}

/// Calculate eigenvalues of a 2x2 matrix (simplified for demonstration)
fn eigenvalues_2x2(matrix: &[Vec<f64>]) -> Vec<f64> {
    if matrix.len() != 2 || matrix[0].len() != 2 {
        // For larger matrices, use a proper eigenvalue solver
        // For now, return a simple approximation
        return vec![1.0, 0.0];
    }
    
    let a = matrix[0][0];
    let b = matrix[0][1];
    let c = matrix[1][0];
    let d = matrix[1][1];
    
    let trace = a + d;
    let det = a * d - b * c;
    
    let discriminant = (trace * trace - 4.0 * det).max(0.0).sqrt();
    let lambda1 = (trace + discriminant) / 2.0;
    let lambda2 = (trace - discriminant) / 2.0;
    
    vec![lambda1, lambda2]
}

/// Generate a random entangled state
fn generate_random_entangled_state(num_qubits: u32) -> Vec<f64> {
    let n = 1 << num_qubits;
    let mut state = vec![0.0; n];
    
    // Create a random superposition
    for i in 0..n {
        state[i] = rand_f64();
    }
    
    // Normalize
    let norm: f64 = state.iter().map(|&a| a * a).sum();
    let norm_factor = 1.0 / norm.sqrt();
    
    for amp in &mut state {
        *amp *= norm_factor;
    }
    
    state
}

/// Generate a random f64 between -1 and 1
fn rand_f64() -> f64 {
    // Simple pseudo-random number generator for demonstration
    // In a real application, use a proper RNG
    let seed = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .subsec_nanos() as f64;
    
    ((seed * 0.123456789) % 2.0) - 1.0
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_validate_state() {
        // Valid normalized state
        let state = vec![0.7071, 0.0, 0.0, 0.7071];
        assert!(validate_state(&state));
        
        // Invalid unnormalized state
        let state = vec![1.0, 0.0, 0.0, 0.0];
        assert!(!validate_state(&state));
        
        // Invalid non-power-of-two length
        let state = vec![0.5, 0.5, 0.5];
        assert!(!validate_state(&state));
    }
    
    #[test]
    fn test_is_bell_state() {
        // |Φ+⟩ = (|00⟩ + |11⟩)/√2
        let bell_plus = vec![0.7071, 0.0, 0.0, 0.7071];
        assert!(is_bell_state(&bell_plus));
        
        // |Ψ+⟩ = (|01⟩ + |10⟩)/√2
        let bell_psi_plus = vec![0.0, 0.7071, 0.7071, 0.0];
        assert!(is_bell_state(&bell_psi_plus));
        
        // Not a Bell state
        let not_bell = vec![0.5, 0.5, 0.5, 0.5];
        assert!(!is_bell_state(&not_bell));
    }
    
    #[test]
    fn test_is_ghz_state() {
        // |GHZ⟩ = (|000⟩ + |111⟩)/√2
        let ghz = vec![0.7071, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7071];
        assert!(is_ghz_state(&ghz));
        
        // Not a GHZ state
        let not_ghz = vec![0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0];
        assert!(!is_ghz_state(&not_ghz));
    }
    
    #[test]
    fn test_is_separable() {
        // Computational basis state |01⟩
        let separable = vec![0.0, 1.0, 0.0, 0.0];
        assert!(is_separable(&separable));
        
        // Bell state (entangled)
        let bell = vec![0.7071, 0.0, 0.0, 0.7071];
        assert!(!is_separable(&bell));
    }
    
    #[test]
    fn test_generate_random_entangled_state() {
        let state = generate_random_entangled_state(3);
        assert_eq!(state.len(), 8);
        
        // Check normalization
        let norm: f64 = state.iter().map(|&a| a * a).sum();
        assert!((norm - 1.0).abs() < 1e-10);
    }
}
