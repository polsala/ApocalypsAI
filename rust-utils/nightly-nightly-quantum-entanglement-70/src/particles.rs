use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum QuantumState {
    SpinUp,
    SpinDown,
}

impl fmt::Display for QuantumState {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            QuantumState::SpinUp => write!(f, "↑"),
            QuantumState::SpinDown => write!(f, "↓"),
        }
    }
}

#[derive(Debug, Clone)]
pub struct Particle {
    pub particle_type: ParticleType,
    pub state: QuantumState,
    pub id: u64,
    pub coherence: f64,
    pub energy_level: f64,
}

#[derive(Debug, Clone, PartialEq)]
pub enum ParticleType {
    Photon,
    Electron,
    Neutron,
    Quark,
}

impl Particle {
    pub fn new(particle_type: ParticleType, state: QuantumState, id: u64) -> Self {
        let (coherence, energy_level) = match particle_type {
            ParticleType::Photon => (95.0, 100.0),
            ParticleType::Electron => (90.0, 80.0),
            ParticleType::Neutron => (85.0, 120.0),
            ParticleType::Quark => (80.0, 150.0),
        };
        
        Self {
            particle_type,
            state,
            id,
            coherence,
            energy_level,
        }
    }
    
    pub fn get_symbol(&self) -> &'static str {
        match self.particle_type {
            ParticleType::Photon => "⚛️",
            ParticleType::Electron => "⚡",
            ParticleType::Neutron => "⚪",
            ParticleType::Quark => "🔴",
        }
    }
    
    pub fn get_speed(&self) -> f64 {
        match self.particle_type {
            ParticleType::Photon => 299_792_458.0, // Speed of light
            ParticleType::Electron => 2_200_000.0, // Approximate electron drift velocity
            ParticleType::Neutron => 2_000_000.0,
            ParticleType::Quark => 1_500_000.0,
        }
    }
    
    pub fn decay(&mut self, time_factor: f64) {
        // Simulate quantum decoherence over time
        self.coherence -= time_factor * 0.1;
        self.energy_level -= time_factor * 0.05;
        
        if self.coherence < 0.0 {
            self.coherence = 0.0;
        }
        if self.energy_level < 0.0 {
            self.energy_level = 0.0;
        }
    }
    
    pub fn is_entangled(&self) -> bool {
        self.coherence > 50.0
    }
    
    pub fn measure(&self) -> QuantumState {
        // Quantum measurement collapses the wave function
        // For entangled particles, this should correlate with their partner
        self.state.clone()
    }
}

impl fmt::Display for Particle {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{} Particle #{} [State: {}, Coherence: {:.1}%, Energy: {:.1}%]",
            self.get_symbol(),
            self.id,
            self.state,
            self.coherence,
            self.energy_level,
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_particle_creation() {
        let particle = Particle::new(
            ParticleType::Photon,
            QuantumState::SpinUp,
            1,
        );
        
        assert_eq!(particle.particle_type, ParticleType::Photon);
        assert_eq!(particle.state, QuantumState::SpinUp);
        assert_eq!(particle.id, 1);
        assert_eq!(particle.coherence, 95.0);
        assert_eq!(particle.energy_level, 100.0);
    }
    
    #[test]
    fn test_particle_decay() {
        let mut particle = Particle::new(
            ParticleType::Electron,
            QuantumState::SpinDown,
            2,
        );
        
        let initial_coherence = particle.coherence;
        let initial_energy = particle.energy_level;
        
        particle.decay(10.0);
        
        assert!(particle.coherence < initial_coherence);
        assert!(particle.energy_level < initial_energy);
    }
    
    #[test]
    fn test_particle_entanglement() {
        let mut particle = Particle::new(
            ParticleType::Photon,
            QuantumState::SpinUp,
            3,
        );
        
        assert!(particle.is_entangled());
        
        // Decay until decoherence
        particle.decay(500.0);
        assert!(!particle.is_entangled());
    }
    
    #[test]
    fn test_particle_measurement() {
        let particle = Particle::new(
            ParticleType::Neutron,
            QuantumState::SpinDown,
            4,
        );
        
        let measured_state = particle.measure();
        assert_eq!(measured_state, QuantumState::SpinDown);
    }
}
