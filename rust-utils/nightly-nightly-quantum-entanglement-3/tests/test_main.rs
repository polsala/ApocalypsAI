use nightly_quantum_entanglement_checker::*;
use std::sync::{Arc, Mutex};
use std::collections::HashMap;

// Mock QuantumSimulator for testing
struct MockQuantumSimulator {
    particles: Arc<Mutex<HashMap<u64, QuantumParticle>>>,
    entanglements: Arc<Mutex<Vec<EntanglementRecord>>>,
    next_id: Arc<Mutex<u64>>>,
}

impl MockQuantumSimulator {
    fn new() -> Self {
        Self {
            particles: Arc::new(Mutex::new(HashMap::new())),
            entanglements: Arc::new(Mutex::new(Vec::new())),
            next_id: Arc::new(Mutex::new(1)),
        }
    }

    fn create_particle(&self, initial_spin: SpinState) -> u64 {
        let id = {
            let mut next_id = self.next_id.lock().unwrap();
            let current = *next_id;
            *next_id += 1;
            current
        };

        let particle = QuantumParticle {
            id,
            spin: Some(initial_spin),
            is_entangled: false,
            entangled_with: None,
            creation_time: std::time::Instant::now(),
        };

        self.particles.lock().unwrap().insert(id, particle);
        id
    }

    fn entangle_particles(&self, particle1_id: u64, particle2_id: u64) -> bool {
        let mut particles = self.particles.lock().unwrap();
        
        let particle1 = particles.get_mut(&particle1_id);
        let particle2 = particles.get_mut(&particle2_id);
        
        if particle1.is_none() || particle2.is_none() {
            return false;
        }
        
        let p1 = particle1.unwrap();
        let p2 = particle2.unwrap();
        
        // Can't entangle already entangled particles
        if p1.is_entangled || p2.is_entangled {
            return false;
        }
        
        // Create superposition (remove definite spin)
        p1.spin = None;
        p2.spin = None;
        p1.is_entangled = true;
        p2.is_entangled = true;
        p1.entangled_with = Some(p2_id);
        p2.entangled_with = Some(p1_id);
        
        // For testing, use a fixed Bell state
        let bell_state = BellState::PsiMinus;
        
        self.entanglements.lock().unwrap().push(EntanglementRecord {
            particle1: particle1_id,
            particle2: particle2_id,
            bell_state: bell_state.clone(),
            entanglement_time: std::time::Instant::now(),
        });
        
        true
    }

    fn measure_particle(&self, particle_id: u64) -> Option<SpinState> {
        let mut particles = self.particles.lock().unwrap();
        let particle = particles.get_mut(&particle_id)?;
        
        // If already measured, return the result
        if let Some(spin) = particle.spin {
            return Some(spin);
        }
        
        // If not entangled, can't measure (superposition)
        if !particle.is_entangled {
            return None;
        }
        
        // For testing, use a deterministic measurement
        let measured_spin = SpinState::Up;
        
        particle.spin = Some(measured_spin);
        
        // Update entangled partner
        if let Some(entangled_id) = particle.entangled_with {
            if let Some(entangled_particle) = particles.get_mut(&entangled_id) {
                // For PsiMinus state, partner should have opposite spin
                let partner_spin = SpinState::Down;
                entangled_particle.spin = Some(partner_spin);
            }
        }
        
        Some(measured_spin)
    }

    fn get_particle_status(&self, particle_id: u64) -> Option<String> {
        let particles = self.particles.lock().unwrap();
        let particle = particles.get(&particle_id)?;
        
        let spin_str = match particle.spin {
            Some(SpinState::Up) => "|↑⟩ (Spin Up)",
            Some(SpinState::Down) => "|↓⟩ (Spin Down)",
            None => "|?⟩ (Superposition)",
        };
        
        let entangled_str = if particle.is_entangled {
            match particle.entangled_with {
                Some(other_id) => format!("✓ ENTANGLED with Particle {}", other_id),
                None => "✗ ENTANGLED (but no partner recorded)".to_string(),
            }
        } else {
            "○ Not Entangled".to_string()
        };
        
        Some(format!(
            "Particle {}: {}\nEntanglement Status: {}",
            particle_id, spin_str, entangled_str
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_particle() {
        let simulator = MockQuantumSimulator::new();
        
        let particle_id = simulator.create_particle(SpinState::Up);
        
        assert!(particle_id > 0);
        
        let status = simulator.get_particle_status(particle_id).unwrap();
        assert!(status.contains("Spin Up"));
        assert!(status.contains("Not Entangled"));
    }

    #[test]
    fn test_entangle_particles() {
        let simulator = MockQuantumSimulator::new();
        
        let p1 = simulator.create_particle(SpinState::Up);
        let p2 = simulator.create_particle(SpinState::Down);
        
        assert!(simulator.entangle_particles(p1, p2));
        
        let status1 = simulator.get_particle_status(p1).unwrap();
        let status2 = simulator.get_particle_status(p2).unwrap();
        
        assert!(status1.contains("ENTANGLED"));
        assert!(status2.contains("ENTANGLED"));
        assert!(status1.contains(&format!("Particle {}", p2)));
        assert!(status2.contains(&format!("Particle {}", p1)));
    }

    #[test]
    fn test_entangle_nonexistent_particles() {
        let simulator = MockQuantumSimulator::new();
        
        // Try to entangle non-existent particles
        assert!(!simulator.entangle_particles(999, 888));
    }

    #[test]
    fn test_entangle_already_entangled_particle() {
        let simulator = MockQuantumSimulator::new();
        
        let p1 = simulator.create_particle(SpinState::Up);
        let p2 = simulator.create_particle(SpinState::Down);
        let p3 = simulator.create_particle(SpinState::Up);
        
        // First entanglement
        assert!(simulator.entangle_particles(p1, p2));
        
        // Try to entangle p1 with another particle (should fail)
        assert!(!simulator.entangle_particles(p1, p3));
    }

    #[test]
    fn test_measure_particle() {
        let simulator = MockQuantumSimulator::new();
        
        let p1 = simulator.create_particle(SpinState::Up);
        let p2 = simulator.create_particle(SpinState::Down);
        
        assert!(simulator.entangle_particles(p1, p2));
        
        // Measure first particle
        let result1 = simulator.measure_particle(p1);
        assert_eq!(result1, Some(SpinState::Up));
        
        // Measure second particle (should be opposite due to PsiMinus state)
        let result2 = simulator.measure_particle(p2);
        assert_eq!(result2, Some(SpinState::Down));
    }

    #[test]
    fn test_measure_non_entangled_particle() {
        let simulator = MockQuantumSimulator::new();
        
        let p1 = simulator.create_particle(SpinState::Up);
        
        // Try to measure non-entangled particle
        let result = simulator.measure_particle(p1);
        assert_eq!(result, None);
    }

    #[test]
    fn test_measure_already_measured_particle() {
        let simulator = MockQuantumSimulator::new();
        
        let p1 = simulator.create_particle(SpinState::Up);
        let p2 = simulator.create_particle(SpinState::Down);
        
        assert!(simulator.entangle_particles(p1, p2));
        
        // First measurement
        let result1 = simulator.measure_particle(p1);
        assert_eq!(result1, Some(SpinState::Up));
        
        // Second measurement should return the same result
        let result2 = simulator.measure_particle(p1);
        assert_eq!(result2, Some(SpinState::Up));
    }

    #[test]
    fn test_particle_status_formatting() {
        let simulator = MockQuantumSimulator::new();
        
        let p1 = simulator.create_particle(SpinState::Up);
        
        let status = simulator.get_particle_status(p1).unwrap();
        
        assert!(status.contains("Particle "));
        assert!(status.contains("Spin Up"));
        assert!(status.contains("Not Entangled"));
    }

    #[test]
    fn test_spin_state_equality() {
        assert_eq!(SpinState::Up, SpinState::Up);
        assert_eq!(SpinState::Down, SpinState::Down);
        assert_ne!(SpinState::Up, SpinState::Down);
    }

    #[test]
    fn test_bell_state_variants() {
        let states = vec![
            BellState::PhiPlus,
            BellState::PhiMinus,
            BellState::PsiPlus,
            BellState::PsiMinus,
        ];
        
        assert_eq!(states.len(), 4);
    }

    #[test]
    fn test_multiple_particle_creation() {
        let simulator = MockQuantumSimulator::new();
        
        let mut particle_ids = Vec::new();
        for i in 0..10 {
            let spin = if i % 2 == 0 { SpinState::Up } else { SpinState::Down };
            particle_ids.push(simulator.create_particle(spin));
        }
        
        assert_eq!(particle_ids.len(), 10);
        
        // All should have unique IDs
        let unique_ids: std::collections::HashSet<u64> = particle_ids.iter().cloned().collect();
        assert_eq!(unique_ids.len(), 10);
    }

    #[test]
    fn test_concurrent_particle_access() {
        use std::sync::Arc;
        use std::thread;
        
        let simulator = Arc::new(MockQuantumSimulator::new());
        let mut handles = vec![];
        
        // Create particles from multiple threads
        for i in 0..5 {
            let simulator_clone = Arc::clone(&simulator);
            handles.push(thread::spawn(move || {
                simulator_clone.create_particle(
                    if i % 2 == 0 { SpinState::Up } else { SpinState::Down }
                )
            }));
        }
        
        let particle_ids: Vec<u64> = handles.into_iter()
            .map(|h| h.join().unwrap())
            .collect();
        
        assert_eq!(particle_ids.len(), 5);
    }
}
