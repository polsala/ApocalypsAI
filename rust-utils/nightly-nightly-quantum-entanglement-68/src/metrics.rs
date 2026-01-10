use std::time::Instant;

/// Quantum metrics for a single iteration
#[derive(Debug, Clone)]
pub struct IterationMetrics {
    pub iteration: usize,
    pub timestamp: Instant,
    pub entanglement_score: f64,
    pub coherence_score: f64,
}

/// Final aggregated quantum metrics
#[derive(Debug, Clone)]
pub struct FinalMetrics {
    pub iterations: usize,
    pub avg_entanglement: f64,
    pub avg_coherence: f64,
    pub peak_entanglement: f64,
    pub peak_coherence: f64,
    pub total_duration: std::time::Duration,
}

/// Collects and aggregates quantum metrics
pub struct QuantumMetrics {
    iterations: Vec<IterationMetrics>,
    start_time: Instant,
}

impl QuantumMetrics {
    pub fn new() -> Self {
        Self {
            iterations: Vec::new(),
            start_time: Instant::now(),
        }
    }

    /// Record metrics for an iteration
    pub fn record_iteration(&mut self, iteration: usize, entanglement_score: f64, coherence_score: f64) {
        let metrics = IterationMetrics {
            iteration,
            timestamp: Instant::now(),
            entanglement_score,
            coherence_score,
        };
        
        self.iterations.push(metrics);
    }

    /// Get final aggregated metrics
    pub fn get_final_metrics(&self) -> FinalMetrics {
        let total_iterations = self.iterations.len();
        
        if total_iterations == 0 {
            return FinalMetrics {
                iterations: 0,
                avg_entanglement: 0.0,
                avg_coherence: 0.0,
                peak_entanglement: 0.0,
                peak_coherence: 0.0,
                total_duration: self.start_time.elapsed(),
            };
        }

        let total_entanglement: f64 = self.iterations.iter().map(|m| m.entanglement_score).sum();
        let total_coherence: f64 = self.iterations.iter().map(|m| m.coherence_score).sum();
        
        let avg_entanglement = total_entanglement / total_iterations as f64;
        let avg_coherence = total_coherence / total_iterations as f64;
        
        let peak_entanglement = self.iterations.iter().map(|m| m.entanglement_score).fold(0.0, f64::max);
        let peak_coherence = self.iterations.iter().map(|m| m.coherence_score).fold(0.0, f64::max);

        FinalMetrics {
            iterations: total_iterations,
            avg_entanglement,
            avg_coherence,
            peak_entanglement,
            peak_coherence,
            total_duration: self.start_time.elapsed(),
        }
    }

    /// Get the number of recorded iterations
    pub fn iteration_count(&self) -> usize {
        self.iterations.len()
    }

    /// Get the average entanglement score
    pub fn average_entanglement(&self) -> f64 {
        if self.iterations.is_empty() {
            0.0
        } else {
            self.iterations.iter().map(|m| m.entanglement_score).sum::<f64>() / self.iterations.len() as f64
        }
    }

    /// Get the average coherence score
    pub fn average_coherence(&self) -> f64 {
        if self.iterations.is_empty() {
            0.0
        } else {
            self.iterations.iter().map(|m| m.coherence_score).sum::<f64>() / self.iterations.len() as f64
        }
    }
}
