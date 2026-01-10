use rand::Rng;
use std::time::SystemTime;

#[derive(Debug, Clone)]
pub enum QuantumState {
    Up,
    Down,
    Superposition,
}

impl std::fmt::Display for QuantumState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            QuantumState::Up => write!(f, "|↑⟩"),
            QuantumState::Down => write!(f, "|↓⟩"),
            QuantumState::Superposition => write!(f, "|ψ⟩"),
        }
    }
}

#[derive(Debug)]
pub struct Particle {
    pub state: QuantumState,
    pub coherence: f64,
}

#[derive(Debug)]
pub struct Measurement {
    pub state: QuantumState,
    pub probability: f64,
    pub fun_fact: String,
}

#[derive(Debug)]
pub struct SimulationResult {
    pub particles: Vec<Particle>,
    pub measurement_outcome: String,
    pub entanglement_strength: f64,
    pub coherence_time: f64,
    pub quantum_correlation: String,
    pub explanation: String,
    pub fun_facts: Vec<String>,
}

pub struct QuantumSimulator {
    rng: rand::rngs::ThreadRng,
}

impl QuantumSimulator {
    pub fn new(_particle_count: usize) -> Self {
        QuantumSimulator {
            rng: rand::thread_rng(),
        }
    }
    
    pub fn simulate_entanglement(&mut self) -> SimulationResult {
        let particle_count = 2; // Default for entanglement
        let mut particles = Vec::new();
        
        // Create entangled particles
        let first_state = if self.rng.gen_bool(0.5) {
            QuantumState::Up
        } else {
            QuantumState::Down
        };
        
        let second_state = match first_state {
            QuantumState::Up => QuantumState::Down,
            QuantumState::Down => QuantumState::Up,
            QuantumState::Superposition => QuantumState::Superposition,
        };
        
        particles.push(Particle {
            state: first_state,
            coherence: self.rng.gen_range(0.8..1.0),
        });
        
        particles.push(Particle {
            state: second_state,
            coherence: self.rng.gen_range(0.8..1.0),
        });
        
        let measurement_outcome = match (particles[0].state.clone(), particles[1].state.clone()) {
            (QuantumState::Up, QuantumState::Down) => "Both particles collapsed to opposite states!".to_string(),
            (QuantumState::Down, QuantumState::Up) => "Both particles collapsed to opposite states!".to_string(),
            _ => "Particles showed unexpected correlation!".to_string(),
        };
        
        let entanglement_strength = self.rng.gen_range(95.0..99.9);
        let coherence_time = self.rng.gen_range(100.0..1000.0);
        let quantum_correlation = "Perfect anti-correlation".to_string();
        
        let explanation = match measurement_outcome.as_str() {
            "Both particles collapsed to opposite states!" => {
                "When entangled particles are measured, they always show correlated results,\neven when separated by vast distances. Spooky action at a distance!".to_string()
            },
            _ => {
                "Quantum entanglement creates mysterious connections between particles\nthat defy classical intuition.".to_string()
            }
        };
        
        let fun_facts = vec![
            "Entanglement was called 'spooky action at a distance' by Einstein".to_string(),
            "Quantum teleportation relies on entanglement".to_string(),
            "Entangled particles can be separated by kilometers and still remain connected".to_string(),
        ];
        
        SimulationResult {
            particles,
            measurement_outcome,
            entanglement_strength,
            coherence_time,
            quantum_correlation,
            explanation,
            fun_facts,
        }
    }
    
    pub fn measure_particle(&mut self) -> Measurement {
        let probability = self.rng.gen_range(0.0..1.0);
        let state = if probability > 0.5 {
            QuantumState::Up
        } else {
            QuantumState::Down
        };
        
        let fun_fact = match state {
            QuantumState::Up => "Spin up particles are like tiny magnets pointing north!".to_string(),
            QuantumState::Down => "Spin down particles are like tiny magnets pointing south!".to_string(),
            QuantumState::Superposition => "Superposition means the particle is in multiple states at once!".to_string(),
        };
        
        Measurement {
            state,
            probability: 0.5, // Simplified for display
            fun_fact,
        }
    }
}
