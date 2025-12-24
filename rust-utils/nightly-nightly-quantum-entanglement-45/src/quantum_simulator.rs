use rand::Rng;
use std::time::Duration;
use tokio::time::sleep;

#[derive(Debug, Clone)]
pub struct QuantumState {
    coherence: f64,
    entanglement_fidelity: f64,
    correlation_matrix: Vec<Vec<f64>>,
}

pub struct QuantumSimulator {
    nodes: usize,
    initial_entanglement_strength: f64,
    decoherence_rate: f64,
    quantum_states: Vec<QuantumState>,
}

impl QuantumSimulator {
    pub fn new(nodes: usize, entanglement_strength: f64, decoherence_rate: f64) -> Self {
        QuantumSimulator {
            nodes,
            initial_entanglement_strength,
            decoherence_rate,
            quantum_states: Vec::new(),
        }
    }

    pub async fn run_simulation(&mut self, duration: Duration, verbose: bool) -> QuantumStateAnalysis {
        if verbose {
            println!("{}", "⚛️  Initializing quantum state preparation...".bright_magenta());
        }

        self.initialize_states();
        
        let start_time = std::time::Instant::now();
        let mut elapsed = Duration::ZERO;
        
        while elapsed < duration {
            self.evolve_quantum_states();
            
            if verbose && elapsed.as_secs() % 5 == 0 {
                self.print_state_progress(elapsed);
            }
            
            sleep(Duration::from_millis(100)).await;
            elapsed = start_time.elapsed();
        }

        self.calculate_final_metrics()
    }

    fn initialize_states(&mut self) {
        self.quantum_states.clear();
        
        for _ in 0..self.nodes {
            let coherence = self.initial_entanglement_strength + rand::thread_rng().gen_range(-0.1..0.1);
            let entanglement_fidelity = self.initial_entanglement_strength;
            
            let correlation_matrix = self.generate_correlation_matrix();
            
            self.quantum_states.push(QuantumState {
                coherence: coherence.max(0.0).min(1.0),
                entanglement_fidelity,
                correlation_matrix,
            });
        }
    }

    fn generate_correlation_matrix(&self) -> Vec<Vec<f64>> {
        let mut matrix = vec![vec![0.0; self.nodes]; self.nodes];
        let mut rng = rand::thread_rng();
        
        for i in 0..self.nodes {
            for j in 0..self.nodes {
                if i == j {
                    matrix[i][j] = 1.0; // Perfect correlation with self
                } else {
                    // Generate entanglement correlation between nodes
                    let base_correlation = self.initial_entanglement_strength;
                    let noise = rng.gen_range(-0.2..0.2);
                    matrix[i][j] = (base_correlation + noise).max(0.0).min(1.0);
                }
            }
        }
        
        matrix
    }

    fn evolve_quantum_states(&mut self) {
        let mut rng = rand::thread_rng();
        
        for state in &mut self.quantum_states {
            // Apply decoherence
            state.coherence *= 1.0 - self.decoherence_rate;
            
            // Apply quantum noise
            let noise = rng.gen_range(-0.05..0.05);
            state.entanglement_fidelity += noise;
            
            // Ensure values stay within valid ranges
            state.coherence = state.coherence.max(0.0).min(1.0);
            state.entanglement_fidelity = state.entanglement_fidelity.max(0.0).min(1.0);
            
            // Update correlation matrix with environmental effects
            for row in &mut state.correlation_matrix {
                for val in row.iter_mut() {
                    *val *= 1.0 - (self.decoherence_rate * 0.5);
                    *val = val.max(0.0).min(1.0);
                }
            }
        }
    }

    fn print_state_progress(&self, elapsed: Duration) {
        let avg_coherence = self.quantum_states.iter().map(|s| s.coherence).sum::<f64>() / self.nodes as f64;
        let avg_fidelity = self.quantum_states.iter().map(|s| s.entanglement_fidelity).sum::<f64>() / self.nodes as f64;
        
        println!(
            "{} {:.1}% | {} {:.1}% | {} {:.1}s",
            "🔬 Coherence:".bright_cyan(),
            avg_coherence * 100.0,
            "⚛️  Fidelity:".bright_magenta(),
            avg_fidelity * 100.0,
            "⏱️  Time:".bright_yellow(),
            elapsed.as_secs_f32()
        );
    }

    fn calculate_final_metrics(&self) -> QuantumStateAnalysis {
        let avg_coherence = self.quantum_states.iter().map(|s| s.coherence).sum::<f64>() / self.nodes as f64;
        let avg_fidelity = self.quantum_states.iter().map(|s| s.entanglement_fidelity).sum::<f64>() / self.nodes as f64;
        
        let quantum_correlation_score = self.calculate_correlation_score();
        let bell_inequality_violation = self.check_bell_inequality();
        
        QuantumStateAnalysis {
            coherence_level: avg_coherence,
            entanglement_fidelity: avg_fidelity,
            bell_inequality_violation,
            quantum_correlation_score,
        }
    }

    fn calculate_correlation_score(&self) -> f64 {
        let mut total_correlation = 0.0;
        let mut count = 0;
        
        for state in &self.quantum_states {
            for i in 0..self.nodes {
                for j in (i + 1)..self.nodes {
                    total_correlation += state.correlation_matrix[i][j];
                    count += 1;
                }
            }
        }
        
        if count > 0 {
            total_correlation / count as f64
        } else {
            0.0
        }
    }

    fn check_bell_inequality(&self) -> bool {
        // Simplified Bell inequality check
        // In quantum mechanics, Bell's inequality is violated when entanglement is present
        let avg_correlation = self.calculate_correlation_score();
        
        // If correlation is high enough, we consider Bell's inequality violated
        // This is a simplified simulation - real Bell tests are much more complex
        avg_correlation > 0.6
    }
}

#[derive(Debug, Clone)]
pub struct QuantumStateAnalysis {
    pub coherence_level: f64,
    pub entanglement_fidelity: f64,
    pub bell_inequality_violation: bool,
    pub quantum_correlation_score: f64,
}
