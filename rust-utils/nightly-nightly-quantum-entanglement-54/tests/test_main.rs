use nightly_quantum_entanglement_simulator::*;

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::NamedTempFile;

    #[test]
    fn test_quantum_state_to_symbol() {
        assert_eq!(QuantumState::Up.to_symbol(), "|↑⟩");
        assert_eq!(QuantumState::Down.to_symbol(), "|↓⟩");
        assert_eq!(QuantumState::Left.to_symbol(), "|←⟩");
        assert_eq!(QuantumState::Right.to_symbol(), "|→⟩");
        assert_eq!(QuantumState::Diagonal.to_symbol(), "|↗⟩");
        assert_eq!(QuantumState::AntiDiagonal.to_symbol(), "|↖⟩");
    }

    #[test]
    fn test_quantum_state_to_ascii_art() {
        let up_art = QuantumState::Up.to_ascii_art();
        assert!(up_art.contains("/\\"));
        assert!(up_art.contains("||"));

        let down_art = QuantumState::Down.to_ascii_art();
        assert!(down_art.contains("||"));
        assert!(down_art.contains("\\\\/"));
    }

    #[test]
    fn test_quantum_system_creation() {
        let system = QuantumSystem::new(3);
        assert_eq!(system.particles.len(), 3);
        assert_eq!(system.entanglement_pairs.len(), 0);

        for (i, particle) in system.particles.iter().enumerate() {
            assert_eq!(particle.id, i as u32);
            assert!(!particle.is_entangled);
        }
    }

    #[test]
    fn test_entangle_particles() {
        let mut system = QuantumSystem::new(4);
        system.entangle_particles(0, 1);
        system.entangle_particles(2, 3);

        assert_eq!(system.entanglement_pairs.len(), 2);
        assert_eq!(system.entanglement_pairs[0], (0, 1));
        assert_eq!(system.entanglement_pairs[1], (2, 3));

        // Check that particles are marked as entangled
        assert!(system.particles[0].is_entangled);
        assert!(system.particles[1].is_entangled);
        assert!(system.particles[2].is_entangled);
        assert!(system.particles[3].is_entangled);
    }

    #[test]
    fn test_entangle_nonexistent_particles() {
        let mut system = QuantumSystem::new(2);
        system.entangle_particles(0, 5); // Particle 5 doesn't exist

        // Should not create entanglement
        assert_eq!(system.entanglement_pairs.len(), 0);
        assert!(!system.particles[0].is_entangled);
    }

    #[test]
    fn test_save_and_load_quantum_state() {
        let mut system = QuantumSystem::new(4);
        system.entangle_particles(0, 1);
        system.entangle_particles(2, 3);

        // Create a temporary file
        let temp_file = NamedTempFile::new().unwrap();
        let file_path = temp_file.path().to_str().unwrap();

        // Save the system
        let json = serde_json::to_string_pretty(&system).unwrap();
        fs::write(file_path, json).unwrap();

        // Load the system
        let content = fs::read_to_string(file_path).unwrap();
        let loaded_system: QuantumSystem = serde_json::from_str(&content).unwrap();

        // Verify the loaded system
        assert_eq!(loaded_system.particles.len(), system.particles.len());
        assert_eq!(loaded_system.entanglement_pairs.len(), system.entanglement_pairs.len());
        assert_eq!(loaded_system.entanglement_pairs, system.entanglement_pairs);

        // Verify particles are entangled
        assert!(loaded_system.particles[0].is_entangled);
        assert!(loaded_system.particles[1].is_entangled);
        assert!(loaded_system.particles[2].is_entangled);
        assert!(loaded_system.particles[3].is_entangled);
    }

    #[test]
    fn test_simulate_measurement() {
        let mut system = QuantumSystem::new(2);
        system.entangle_particles(0, 1);

        // Initial states should be Up
        assert_eq!(system.particles[0].state, QuantumState::Up);
        assert_eq!(system.particles[1].state, QuantumState::Up);

        // After measurement, entangled particles should have opposite states
        let measurements = system.simulate_measurement();

        assert_eq!(measurements.len(), 2);
        assert_eq!(measurements[0].0, 0);
        assert_eq!(measurements[1].0, 1);

        // For entangled particles, states should be opposite
        match (measurements[0].1.clone(), measurements[1].1.clone()) {
            (QuantumState::Up, QuantumState::Down) => {},
            (QuantumState::Down, QuantumState::Up) => {},
            _ => panic!("Entangled particles should have opposite states"),
        }
    }

    #[test]
    fn test_non_entangled_measurement() {
        let mut system = QuantumSystem::new(1);
        // Don't entangle the particle

        let initial_state = system.particles[0].state.clone();
        let measurements = system.simulate_measurement();

        assert_eq!(measurements.len(), 1);
        assert_eq!(measurements[0].0, 0);

        // The state should change (random measurement)
        // We can't predict the exact state, but it should be one of the valid states
        match measurements[0].1 {
            QuantumState::Up | QuantumState::Down | QuantumState::Left | 
            QuantumState::Right | QuantumState::Diagonal | QuantumState::AntiDiagonal => {},
            _ => panic!("Invalid quantum state"),
        }
    }

    #[test]
    fn test_quantum_system_serialization() {
        let mut system = QuantumSystem::new(2);
        system.entangle_particles(0, 1);

        let serialized = serde_json::to_string(&system).unwrap();
        let deserialized: QuantumSystem = serde_json::from_str(&serialized).unwrap();

        assert_eq!(system.particles.len(), deserialized.particles.len());
        assert_eq!(system.entanglement_pairs, deserialized.entanglement_pairs);
    }

    #[test]
    fn test_empty_system() {
        let system = QuantumSystem::new(0);
        assert_eq!(system.particles.len(), 0);
        assert_eq!(system.entanglement_pairs.len(), 0);
    }

    #[test]
    fn test_single_particle_system() {
        let system = QuantumSystem::new(1);
        assert_eq!(system.particles.len(), 1);
        assert_eq!(system.entanglement_pairs.len(), 0);
        assert_eq!(system.particles[0].id, 0);
        assert!(!system.particles[0].is_entangled);
    }
}
