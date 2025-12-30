use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};

/// Represents different quantum states
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum QuantumState {
    /// Spin up state
    Up,
    /// Spin down state
    Down,
    /// Left polarization state
    Left,
    /// Right polarization state
    Right,
    /// Diagonal polarization state
    Diagonal,
    /// Anti-diagonal polarization state
    AntiDiagonal,
}

impl QuantumState {
    /// Returns the symbolic representation of the quantum state
    pub fn to_symbol(&self) -> &'static str {
        match self {
            QuantumState::Up => "|↑⟩",
            QuantumState::Down => "|↓⟩",
            QuantumState::Left => "|←⟩",
            QuantumState::Right => "|→⟩",
            QuantumState::Diagonal => "|↗⟩",
            QuantumState::AntiDiagonal => "|↖⟩",
        }
    }

    /// Returns ASCII art representation of the quantum state
    pub fn to_ascii_art(&self) -> &'static str {
        match self {
            QuantumState::Up => "  /\  \n  ||  ",
            QuantumState::Down => "  ||  \n  \\\/  ",
            QuantumState::Left => "  <<  ",
            QuantumState::Right => "  >>  ",
            QuantumState::Diagonal => "  /   \n /    ",
            QuantumState::AntiDiagonal => "    \  \n   /   ",
        }
    }

    /// Returns the opposite state for entanglement correlation
    pub fn opposite(&self) -> Self {
        match self {
            QuantumState::Up => QuantumState::Down,
            QuantumState::Down => QuantumState::Up,
            QuantumState::Left => QuantumState::Right,
            QuantumState::Right => QuantumState::Left,
            QuantumState::Diagonal => QuantumState::AntiDiagonal,
            QuantumState::AntiDiagonal => QuantumState::Diagonal,
        }
    }
}

/// Represents a single quantum particle
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuantumParticle {
    /// Unique identifier for the particle
    pub id: u32,
    /// Current quantum state
    pub state: QuantumState,
    /// Whether this particle is entangled with another
    pub is_entangled: bool,
}

/// Represents a quantum system with multiple particles
#[derive(Debug, Serialize, Deserialize)]
pub struct QuantumSystem {
    /// Collection of particles in the system
    pub particles: Vec<QuantumParticle>,
    /// Pairs of entangled particle IDs
    pub entanglement_pairs: Vec<(u32, u32)>,
    /// Timestamp when the system was created or last modified
    pub timestamp: String,
}

impl QuantumSystem {
    /// Creates a new quantum system with the specified number of particles
    pub fn new(particle_count: u32) -> Self {
        let particles: Vec<QuantumParticle> = (0..particle_count)
            .map(|i| QuantumParticle {
                id: i,
                state: QuantumState::Up,
                is_entangled: false,
            })
            .collect();

        QuantumSystem {
            particles,
            entanglement_pairs: Vec::new(),
            timestamp: chrono::Utc::now().to_rfc3339(),
        }
    }

    /// Entangles two particles by their IDs
    pub fn entangle_particles(&mut self, id1: u32, id2: u32) {
        if let (Some(p1), Some(p2)) = (
            self.particles.iter_mut().find(|p| p.id == id1),
            self.particles.iter_mut().find(|p| p.id == id2),
        ) {
            p1.is_entangled = true;
            p2.is_entangled = true;
            self.entanglement_pairs.push((id1, id2));
            self.update_timestamp();
        }
    }

    /// Simulates quantum measurement on all particles
    /// Returns the measurement results for each particle
    pub fn simulate_measurement(&mut self) -> Vec<(u32, QuantumState)> {
        let mut results = Vec::new();
        let mut rng = rand::thread_rng();

        for particle in &mut self.particles {
            let new_state = if particle.is_entangled {
                // For entangled particles, use anti-correlation
                particle.state.opposite()
            } else {
                // For non-entangled particles, random measurement
                let states = [
                    QuantumState::Up,
                    QuantumState::Down,
                    QuantumState::Left,
                    QuantumState::Right,
                    QuantumState::Diagonal,
                    QuantumState::AntiDiagonal,
                ];
                states[rng.gen_range(0..states.len())]
            };

            particle.state = new_state;
            results.push((particle.id, particle.state));
        }

        self.update_timestamp();
        results
    }

    /// Displays ASCII art visualization of the current quantum states
    pub fn display_ascii_art(&self) {
        println!("=== Quantum State Visualization ===");
        for particle in &self.particles {
            println!("Particle {}: {}", particle.id, particle.state.to_symbol());
            println!("{}");
            println!("Entangled: {}", if particle.is_entangled { "✓" } else { "✗" });
            println!("---");
        }
    }

    /// Checks if two particles are entangled
    pub fn are_entangled(&self, id1: u32, id2: u32) -> bool {
        self.entanglement_pairs.iter().any(|&(a, b)| {
            (a == id1 && b == id2) || (a == id2 && b == id1)
        })
    }

    /// Gets the entanglement partner for a given particle ID
    pub fn get_entanglement_partner(&self, id: u32) -> Option<u32> {
        for &(a, b) in &self.entanglement_pairs {
            if a == id {
                return Some(b);
            } else if b == id {
                return Some(a);
            }
        }
        None
    }

    /// Updates the timestamp to the current time
    fn update_timestamp(&mut self) {
        self.timestamp = chrono::Utc::now().to_rfc3339();
    }

    /// Gets the number of entangled pairs in the system
    pub fn entanglement_count(&self) -> usize {
        self.entanglement_pairs.len()
    }

    /// Gets the number of particles in the system
    pub fn particle_count(&self) -> usize {
        self.particles.len()
    }
}

/// Educational content about quantum mechanics concepts
pub struct QuantumEducation;

impl QuantumEducation {
    /// Gets educational content about quantum superposition
    pub fn superposition_content() -> &'static str {
        "Quantum superposition is a fundamental principle of quantum mechanics.\n\nIt states that a quantum system can exist in multiple states simultaneously\nuntil it is measured. Only upon measurement does the system 'collapse'\ninto one of the possible states.\n\nExample:\nA quantum particle can be in a superposition of |↑⟩ and |↓⟩ states,\nmeaning it's both spin up AND spin down at the same time!"
    }

    /// Gets educational content about quantum measurement
    pub fn measurement_content() -> &'static str {
        "In quantum mechanics, measurement is the process that forces a quantum\nsystem to choose one of its possible states. Before measurement, the\nsystem exists in a superposition of states. After measurement, it exists\nin a single, definite state.\n\nThe Observer Effect:\nThe act of observation fundamentally changes the quantum system.\nThis is different from classical physics where observation doesn't\naffect the observed object."
    }

    /// Gets educational content about quantum non-locality
    pub fn nonlocality_content() -> &'static str {
        "Quantum non-locality refers to the phenomenon where entangled particles\naffect each other instantaneously, regardless of the distance between them.\nThis seems to violate the principle that nothing can travel faster than\nthe speed of light, but it's a well-established feature of quantum mechanics.\n\nSpooky Action at a Distance:\nEinstein famously called this 'spooky action at a distance' because it\nchallenged our classical understanding of how the universe works."
    }

    /// Gets general quantum entanglement explanation
    pub fn entanglement_content() -> &'static str {
        "Quantum entanglement is a physical phenomenon that occurs when pairs or\ngroups of particles are generated, interact, or share spatial proximity\nin ways such that the quantum state of each particle cannot be described\nindependently of the state of the others.\n\nKey Concepts:\n• Superposition: Particles can exist in multiple states simultaneously\n• Measurement: Observing a particle forces it into a definite state\n• Non-locality: Entangled particles affect each other instantaneously\n\nSimulation:\nParticle A: |↑⟩ + |↓⟩ (superposition)\nParticle B: |↑⟩ + |↓⟩ (superposition)\nEntanglement: ✓ Active\n\nWhen we measure Particle A and find it in state |↑⟩,\nParticle B instantly becomes |↓⟩!"
    }
}
