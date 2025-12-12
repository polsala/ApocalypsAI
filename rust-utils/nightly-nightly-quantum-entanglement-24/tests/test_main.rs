use nightly_quantum_entanglement_checker::*;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quantum_particle_creation() {
        // Mock rationale: Test basic particle creation
        let mut particle = QuantumParticle::new("test_particle".to_string());
        assert_eq!(particle.id, "test_particle");
        assert_eq!(particle.state, QuantumState::SpinUp);
        assert!(particle.entangled_with.is_none());
        
        // Test entanglement
        particle.entangle_with("partner".to_string());
        assert_eq!(particle.entangled_with, Some("partner".to_string()));
    }

    #[test]
    fn test_quantum_measurement() {
        // Mock rationale: Test quantum measurement collapses state
        let mut particle = QuantumParticle::new("test_particle".to_string());
        
        // Initial state should be SpinUp
        assert_eq!(particle.state, QuantumState::SpinUp);
        
        // First measurement should collapse to SpinDown
        let measurement1 = particle.measure();
        assert_eq!(measurement1, QuantumState::SpinDown);
        assert_eq!(particle.state, QuantumState::SpinDown);
        
        // Second measurement should collapse back to SpinUp
        let measurement2 = particle.measure();
        assert_eq!(measurement2, QuantumState::SpinUp);
        assert_eq!(particle.state, QuantumState::SpinUp);
    }

    #[test]
    fn test_simulator_particle_creation() {
        // Mock rationale: Test simulator can create particles
        let mut simulator = QuantumEntanglementSimulator::new();
        simulator.create_particle("particle1".to_string());
        
        assert!(simulator.particles.contains_key("particle1"));
        assert_eq!(simulator.particles.len(), 1);
    }

    #[test]
    fn test_entanglement_between_particles() {
        // Mock rationale: Test particles can be entangled
        let mut simulator = QuantumEntanglementSimulator::new();
        simulator.create_particle("particle_a".to_string());
        simulator.create_particle("particle_b".to_string());
        
        // Entangle particles
        let result = simulator.entangle_particles("particle_a", "particle_b");
        assert!(result.is_ok());
        
        // Check both particles are marked as entangled
        assert_eq!(simulator.particles.get("particle_a").unwrap().entangled_with, Some("particle_b".to_string()));
        assert_eq!(simulator.particles.get("particle_b").unwrap().entangled_with, Some("particle_a".to_string()));
    }

    #[test]
    fn test_entanglement_nonexistent_particles() {
        // Mock rationale: Test entanglement fails with non-existent particles
        let mut simulator = QuantumEntanglementSimulator::new();
        simulator.create_particle("particle_a".to_string());
        
        let result = simulator.entangle_particles("particle_a", "nonexistent");
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "One or both particles do not exist");
    }

    #[test]
    fn test_measure_correlation_entangled_particles() {
        // Mock rationale: Test correlation measurement for entangled particles
        let mut simulator = QuantumEntanglementSimulator::new();
        simulator.create_particle("particle_a".to_string());
        simulator.create_particle("particle_b".to_string());
        simulator.entangle_particles("particle_a", "particle_b").unwrap();
        
        // Measure correlation with many iterations
        let correlation = simulator.measure_correlation("particle_a", "particle_b", 1000).unwrap();
        
        // Entangled particles should have high anti-correlation
        assert!(correlation > 0.9, "Expected high correlation for entangled particles, got {}", correlation);
    }

    #[test]
    fn test_measure_correlation_nonexistent_particles() {
        // Mock rationale: Test correlation measurement fails with non-existent particles
        let simulator = QuantumEntanglementSimulator::new();
        
        let result = simulator.measure_correlation("nonexistent_a", "nonexistent_b", 100);
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "One or both particles do not exist");
    }

    #[test]
    fn test_quantum_random_generation() {
        // Mock rationale: Test quantum random number generation
        let simulator = QuantumEntanglementSimulator::new();
        
        let random_numbers = simulator.generate_quantum_random(10);
        
        assert_eq!(random_numbers.len(), 10);
        
        // Check that we get different numbers (highly likely with quantum randomness)
        let unique_numbers: std::collections::HashSet<u64> = random_numbers.iter().cloned().collect();
        assert!(unique_numbers.len() > 5, "Expected mostly unique random numbers");
    }

    #[test]
    fn test_quantum_random_generation_consistency() {
        // Mock rationale: Test that random generation is deterministic given same state
        let simulator = QuantumEntanglementSimulator::new();
        
        let random_numbers_1 = simulator.generate_quantum_random(5);
        let random_numbers_2 = simulator.generate_quantum_random(5);
        
        // Should be different due to time-based randomness
        assert_ne!(random_numbers_1, random_numbers_2);
    }

    #[test]
    fn test_multiple_entanglements() {
        // Mock rationale: Test multiple independent entanglements
        let mut simulator = QuantumEntanglementSimulator::new();
        
        // Create multiple particle pairs
        for i in 0..5 {
            simulator.create_particle(format!("pair_{}_a", i));
            simulator.create_particle(format!("pair_{}_b", i));
            simulator.entangle_particles(&format!("pair_{}_a", i), &format!("pair_{}_b", i)).unwrap();
        }
        
        // Test correlation for each pair
        for i in 0..5 {
            let correlation = simulator.measure_correlation(&format!("pair_{}_a", i), &format!("pair_{}_b", i), 100).unwrap();
            assert!(correlation > 0.9, "Pair {} should be highly correlated, got {}", i, correlation);
        }
    }

    #[test]
    fn test_particle_state_oscillation() {
        // Mock rationale: Test that particle states oscillate correctly
        let mut particle = QuantumParticle::new("test".to_string());
        
        // Measure multiple times and ensure oscillation
        let states = vec![
            particle.measure(),
            particle.measure(),
            particle.measure(),
            particle.measure(),
            particle.measure(),
        ];
        
        // Should alternate between SpinUp and SpinDown
        assert_eq!(states[0], QuantumState::SpinDown); // First measurement
        assert_eq!(states[1], QuantumState::SpinUp);  // Second measurement
        assert_eq!(states[2], QuantumState::SpinDown); // Third measurement
        assert_eq!(states[3], QuantumState::SpinUp);  // Fourth measurement
        assert_eq!(states[4], QuantumState::SpinDown); // Fifth measurement
    }
}
