use std::collections::HashMap;
use rand::Rng;

/// Quantum Entanglement Simulator
/// Simulates quantum entanglement principles for distributed systems
pub struct QuantumSimulator {
    /// Internal state representing quantum connections between nodes
    entanglement_states: HashMap<String, HashMap<String, f64>>,
    /// Random number generator for quantum events
    rng: rand::rngs::ThreadRng,
}

impl QuantumSimulator {
    /// Create a new quantum simulator
    pub fn new() -> Self {
        QuantumSimulator {
            entanglement_states: HashMap::new(),
            rng: rand::thread_rng(),
        }
    }

    /// Check entanglement fidelity between two nodes
    /// Returns a value between 0.0 and 1.0 representing entanglement strength
    pub fn check_entanglement(&mut self, node_a: &str, node_b: &str) -> f64 {
        // Generate a unique key for this node pair
        let key = if node_a < node_b {
            format!("{}_{}", node_a, node_b)
        } else {
            format!("{}_{}", node_b, node_a)
        };

        // Check if we already have an entanglement state for this pair
        if let Some(existing_state) = self.entanglement_states.get(&key) {
            // Return the existing fidelity with some quantum fluctuation
            let base_fidelity = existing_state.get("fidelity").unwrap_or(&0.8);
            let fluctuation = self.rng.gen_range(-0.05..0.05);
            let new_fidelity = (base_fidelity + fluctuation).clamp(0.5, 1.0);
            
            // Update the state
            self.entanglement_states.get_mut(&key).unwrap().insert("fidelity".to_string(), new_fidelity);
            
            return new_fidelity;
        }

        // Generate a new entanglement state
        let fidelity = self.generate_entanglement_fidelity();
        let mut state = HashMap::new();
        state.insert("fidelity".to_string(), fidelity);
        state.insert("phase".to_string(), self.rng.gen_range(0.0..6.28)); // 2π
        state.insert("coherence".to_string(), self.rng.gen_range(0.7..1.0));
        
        self.entanglement_states.insert(key, state);
        
        fidelity
    }

    /// Generate a base entanglement fidelity
    fn generate_entanglement_fidelity(&mut self) -> f64 {
        // Generate a high-quality entanglement with some randomness
        // Most entanglements should be strong (0.7-1.0) with occasional weaker ones
        let quality_roll = self.rng.gen_range(0.0..1.0);
        
        if quality_roll > 0.2 {
            // 80% chance of strong entanglement
            self.rng.gen_range(0.75..1.0)
        } else {
            // 20% chance of weaker entanglement
            self.rng.gen_range(0.5..0.8)
        }
    }

    /// Simulate quantum events that might occur in a distributed system
    pub fn simulate_quantum_events(&mut self) -> Vec<String> {
        let mut events = Vec::new();
        
        // Determine how many events to simulate
        let event_count = self.rng.gen_range(0..4);
        
        for _ in 0..event_count {
            let event_type = self.rng.gen_range(0..6);
            
            match event_type {
                0 => events.push("Quantum superposition detected in node cluster".to_string()),
                1 => events.push("Wave function collapse observed in subsystem".to_string()),
                2 => events.push("Virtual particle pair creation event".to_string()),
                3 => events.push("Quantum tunneling bypass successful".to_string()),
                4 => events.push("Heisenberg uncertainty principle in effect".to_string()),
                5 => events.push("Schrödinger state transition completed".to_string()),
                _ => unreachable!(),
            }
        }
        
        events
    }

    /// Get the current entanglement state between two nodes
    pub fn get_entanglement_state(&self, node_a: &str, node_b: &str) -> Option<&HashMap<String, f64>> {
        let key = if node_a < node_b {
            format!("{}_{}", node_a, node_b)
        } else {
            format!("{}_{}", node_b, node_a)
        };
        
        self.entanglement_states.get(&key)
    }

    /// Reset all entanglement states (quantum reboot)
    pub fn reset_entanglements(&mut self) {
        self.entanglement_states.clear();
    }

    /// Get the number of entangled node pairs
    pub fn entanglement_count(&self) -> usize {
        self.entanglement_states.len()
    }
}
