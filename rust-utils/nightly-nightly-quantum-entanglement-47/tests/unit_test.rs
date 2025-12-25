use nightly_quantum_entanglement_simulator::quantum_simulator::*;

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    #[test]
    fn test_spin_state_opposites() {
        assert_ne!(SpinState::Up, SpinState::Down);
    }

    #[test]
    fn test_polarization_opposites() {
        assert_ne!(Polarization::Horizontal, Polarization::Vertical);
    }

    #[test]
    fn test_color_state_variety() {
        let colors = vec![ColorState::Red, ColorState::Green, ColorState::Blue];
        assert_eq!(colors.len(), 3);
        assert!(colors.contains(&ColorState::Red));
        assert!(colors.contains(&ColorState::Green));
        assert!(colors.contains(&ColorState::Blue));
    }

    #[test]
    fn test_position_state_variety() {
        let positions = vec![
            PositionState::Dimension1,
            PositionState::Dimension2,
            PositionState::Dimension3,
            PositionState::Dimension4,
        ];
        assert_eq!(positions.len(), 4);
        for pos in &positions {
            assert!(positions.contains(pos));
        }
    }

    #[test]
    fn test_quantum_particle_creation() {
        let particle = QuantumParticle {
            id: 1,
            spin: SpinState::Up,
            polarization: Polarization::Horizontal,
            color: ColorState::Red,
            position: PositionState::Dimension1,
            is_observed: false,
        };
        
        assert_eq!(particle.id, 1);
        assert_eq!(particle.spin, SpinState::Up);
        assert_eq!(particle.polarization, Polarization::Horizontal);
        assert_eq!(particle.color, ColorState::Red);
        assert_eq!(particle.position, PositionState::Dimension1);
        assert!(!particle.is_observed);
    }

    #[test]
    fn test_entangled_pair_creation() {
        let particle_a = QuantumParticle {
            id: 1,
            spin: SpinState::Up,
            polarization: Polarization::Horizontal,
            color: ColorState::Red,
            position: PositionState::Dimension1,
            is_observed: false,
        };
        
        let particle_b = QuantumParticle {
            id: 2,
            spin: SpinState::Down,
            polarization: Polarization::Vertical,
            color: ColorState::Blue,
            position: PositionState::Dimension4,
            is_observed: false,
        };
        
        let pair = EntangledPair {
            particle_a,
            particle_b,
            entanglement_strength: 0.95,
        };
        
        assert_eq!(pair.particle_a.id, 1);
        assert_eq!(pair.particle_b.id, 2);
        assert_eq!(pair.entanglement_strength, 0.95);
        assert_ne!(pair.particle_a.spin, pair.particle_b.spin);
        assert_ne!(pair.particle_a.polarization, pair.particle_b.polarization);
    }

    #[test]
    fn test_observation_creation() {
        let observation = Observation {
            pair_id: 1,
            observed_particle: 1,
            observed_state: "Particle 1 [Spin: Up, Pol: Horizontal, Color: Red, Pos: Dimension1]".to_string(),
            collapsed_state: "Particle 2 [Spin: Down, Pol: Vertical, Color: Blue, Pos: Dimension4]".to_string(),
            spooky_action: true,
        };
        
        assert_eq!(observation.pair_id, 1);
        assert_eq!(observation.observed_particle, 1);
        assert!(observation.spooky_action);
        assert!(observation.observed_state.contains("Particle 1"));
        assert!(observation.collapsed_state.contains("Particle 2"));
    }

    #[test]
    fn test_teleportation_creation() {
        let teleportation = Teleportation {
            source_particle: 1,
            target_particle: 3,
            success: true,
            fidelity: 0.85,
        };
        
        assert_eq!(teleportation.source_particle, 1);
        assert_eq!(teleportation.target_particle, 3);
        assert!(teleportation.success);
        assert_eq!(teleportation.fidelity, 0.85);
    }

    #[test]
    fn test_simulation_result_creation() {
        let observation = Observation {
            pair_id: 1,
            observed_particle: 1,
            observed_state: "test".to_string(),
            collapsed_state: "test".to_string(),
            spooky_action: true,
        };
        
        let teleportation = Teleportation {
            source_particle: 1,
            target_particle: 3,
            success: true,
            fidelity: 0.85,
        };
        
        let result = SimulationResult {
            timestamp: "2023-01-01T00:00:00Z".to_string(),
            pairs_generated: 1,
            observations: vec![observation],
            teleportations: vec![teleportation],
        };
        
        assert_eq!(result.pairs_generated, 1);
        assert_eq!(result.observations.len(), 1);
        assert_eq!(result.teleportations.len(), 1);
        assert_eq!(result.timestamp, "2023-01-01T00:00:00Z");
    }

    #[test]
    fn test_serialization_deserialization() {
        let particle = QuantumParticle {
            id: 1,
            spin: SpinState::Up,
            polarization: Polarization::Horizontal,
            color: ColorState::Red,
            position: PositionState::Dimension1,
            is_observed: false,
        };
        
        let serialized = serde_json::to_string(&particle).unwrap();
        let deserialized: QuantumParticle = serde_json::from_str(&serialized).unwrap();
        
        assert_eq!(particle.id, deserialized.id);
        assert_eq!(particle.spin, deserialized.spin);
        assert_eq!(particle.polarization, deserialized.polarization);
        assert_eq!(particle.color, deserialized.color);
        assert_eq!(particle.position, deserialized.position);
        assert_eq!(particle.is_observed, deserialized.is_observed);
    }
}
