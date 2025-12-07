use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use rand::Rng;
use std::time::{Duration, Instant};

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
enum SpinState {
    Up,
    Down,
}

#[derive(Debug, Clone)]
struct QuantumParticle {
    id: u64,
    spin: Option<SpinState>,
    is_entangled: bool,
    entangled_with: Option<u64>,
    creation_time: Instant,
}

#[derive(Debug, Clone)]
struct EntanglementRecord {
    particle1: u64,
    particle2: u64,
    bell_state: BellState,
    entanglement_time: Instant,
}

#[derive(Debug, Clone)]
enum BellState {
    /// |Φ⁺⟩ = (|↑↑⟩ + |↓↓⟩)/√2
    PhiPlus,
    /// |Φ⁻⟩ = (|↑↑⟩ - |↓↓⟩)/√2
    PhiMinus,
    /// |Ψ⁺⟩ = (|↑↓⟩ + |↓↑⟩)/√2
    PsiPlus,
    /// |Ψ⁻⟩ = (|↑↓⟩ - |↓↑⟩)/√2
    PsiMinus,
}

struct QuantumSimulator {
    particles: Arc<Mutex<HashMap<u64, QuantumParticle>>>,
    entanglements: Arc<Mutex<Vec<EntanglementRecord>>>,
    next_id: Arc<Mutex<u64>>,
}

impl QuantumSimulator {
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
            creation_time: Instant::now(),
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
        
        // Randomly choose a Bell state
        let bell_state = match rand::thread_rng().gen_range(0..4) {
            0 => BellState::PhiPlus,
            1 => BellState::PhiMinus,
            2 => BellState::PsiPlus,
            _ => BellState::PsiMinus,
        };
        
        self.entanglements.lock().unwrap().push(EntanglementRecord {
            particle1: particle1_id,
            particle2: particle2_id,
            bell_state: bell_state.clone(),
            entanglement_time: Instant::now(),
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
        
        // Collapse the wave function!
        let measured_spin = if rand::thread_rng().gen_bool(0.5) {
            SpinState::Up
        } else {
            SpinState::Down
        };
        
        particle.spin = Some(measured_spin);
        
        // Update entangled partner
        if let Some(entangled_id) = particle.entangled_with {
            if let Some(entangled_particle) = particles.get_mut(&entangled_id) {
                // Determine partner's spin based on Bell state
                let partner_spin = self.determine_partner_spin(particle_id, entangled_id, &measured_spin);
                entangled_particle.spin = Some(partner_spin);
            }
        }
        
        Some(measured_spin)
    }

    fn determine_partner_spin(&self, p1_id: u64, p2_id: u64, p1_spin: &SpinState) -> SpinState {
        let entanglements = self.entanglements.lock().unwrap();
        
        // Find the entanglement record
        for record in entanglements.iter() {
            if (record.particle1 == p1_id && record.particle2 == p2_id) ||
               (record.particle1 == p2_id && record.particle2 == p1_id) {
                
                return match record.bell_state {
                    BellState::PhiPlus | BellState::PhiMinus => p1_spin.clone(),
                    BellState::PsiPlus | BellState::PsiMinus => {
                        match p1_spin {
                            SpinState::Up => SpinState::Down,
                            SpinState::Down => SpinState::Up,
                        }
                    }
                };
            }
        }
        
        // Fallback: opposite spin (conservation)
        match p1_spin {
            SpinState::Up => SpinState::Down,
            SpinState::Down => SpinState::Up,
        }
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

    fn get_bell_state_description(&self, particle1_id: u64, particle2_id: u64) -> Option<String> {
        let entanglements = self.entanglements.lock().unwrap();
        
        for record in entanglements.iter() {
            if (record.particle1 == particle1_id && record.particle2 == particle2_id) ||
               (record.particle1 == particle2_id && record.particle2 == particle1_id) {
                
                return Some(match record.bell_state {
                    BellState::PhiPlus => "|Φ⁺⟩ = (|↑↑⟩ + |↓↓⟩)/√2".to_string(),
                    BellState::PhiMinus => "|Φ⁻⟩ = (|↑↑⟩ - |↓↓⟩)/√2".to_string(),
                    BellState::PsiPlus => "|Ψ⁺⟩ = (|↑↓⟩ + |↓↑⟩)/√2".to_string(),
                    BellState::PsiMinus => "|Ψ⁻⟩ = (|↑↓⟩ - |↓↑⟩)/√2".to_string(),
                });
            }
        }
        
        None
    }

    fn simulate_many_particles(&self, count: usize, entangled_pairs: usize) -> Duration {
        let start = Instant::now();
        
        // Create particles
        let mut particle_ids = Vec::new();
        for _ in 0..count {
            let spin = if rand::thread_rng().gen_bool(0.5) {
                SpinState::Up
            } else {
                SpinState::Down
            };
            particle_ids.push(self.create_particle(spin));
        }
        
        // Create entangled pairs
        let mut pairs_created = 0;
        for _ in 0..entangled_pairs {
            if particle_ids.len() >= 2 {
                let idx1 = rand::thread_rng().gen_range(0..particle_ids.len());
                let idx2 = rand::thread_rng().gen_range(0..particle_ids.len());
                
                if idx1 != idx2 {
                    if self.entangle_particles(particle_ids[idx1], particle_ids[idx2]) {
                        pairs_created += 1;
                    }
                }
            }
        }
        
        // Measure some particles
        for _ in 0..(count / 4) {
            if !particle_ids.is_empty() {
                let idx = rand::thread_rng().gen_range(0..particle_ids.len());
                self.measure_particle(particle_ids[idx]);
            }
        }
        
        start.elapsed()
    }
}

fn print_quantum_header() {
    println!("\n🌌 QUANTUM ENTANGLEMENT CHECKER 🌌");
    println!("=====================================");
}

fn print_ascii_particle(particle_id: u64, spin: Option<&SpinState>) {
    let spin_symbol = match spin {
        Some(SpinState::Up) => "↑",
        Some(SpinState::Down) => "↓",
        None => "?",
    };
    
    println!("\nParticle {}: |{}⟩", particle_id, spin_symbol);
    println!("    ┌─────────────────┐");
    println!("    │   Quantum     │");
    println!("    │   Particle    │");
    println!("    │     #{:02}       │", particle_id);
    println!("    └─────────────────┘");
}

fn print_entanglement_visual(p1_id: u64, p2_id: u64) {
    println!("\n    Entanglement Link:");
    println!("    {:>8} ──────── ──────── ──────── {:<8}", format!("Particle {}", p1_id), format!("Particle {}", p2_id));
    println!("              Quantum Entanglement Field");
}

fn main() {
    use std::env;
    
    let args: Vec<String> = env::args().collect();
    
    let simulator = QuantumSimulator::new();
    
    if args.contains(&"--visualize".to_string()) {
        print_quantum_header();
        println!("\nCreating a quantum visualization...");
        
        let p1 = simulator.create_particle(SpinState::Up);
        let p2 = simulator.create_particle(SpinState::Down);
        
        print_ascii_particle(p1, Some(&SpinState::Up));
        print_ascii_particle(p2, Some(&SpinState::Down));
        
        if simulator.entangle_particles(p1, p2) {
            println!("\n✨ Successfully entangled particles!");
            print_entanglement_visual(p1, p2);
            
            if let Some(bell_desc) = simulator.get_bell_state_description(p1, p2) {
                println!("\nBell State: {}", bell_desc);
            }
            
            println!("\n📡 Measuring Particle {}...", p1);
            if let Some(result) = simulator.measure_particle(p1) {
                println!("Particle {} measured: {:?}", p1, result);
                print_ascii_particle(p1, Some(&result));
            }
            
            println!("\n📡 Measuring Particle {}...", p2);
            if let Some(result) = simulator.measure_particle(p2) {
                println!("Particle {} measured: {:?}", p2, result);
                print_ascii_particle(p2, Some(&result));
            }
            
            println!("\n🎉 Quantum entanglement demonstrated!");
            println!("(No matter the distance, measuring one instantly determines the other)");
        } else {
            println!("❌ Failed to entangle particles");
        }
        
        return;
    }
    
    let particles = args.iter()
        .position(|arg| arg == "--particles")
        .and_then(|pos| args.get(pos + 1))
        .and_then(|s| s.parse::<usize>().ok())
        .unwrap_or(100);
    
    let entangled = args.iter()
        .position(|arg| arg == "--entangled")
        .and_then(|pos| args.get(pos + 1))
        .and_then(|s| s.parse::<usize>().ok())
        .unwrap_or(10);
    
    print_quantum_header();
    println!("\nSimulating {} particles with {} entangled pairs...", particles, entangled);
    
    let duration = simulator.simulate_many_particles(particles, entangled);
    
    println!("\n⏱️  Simulation completed in {:?}", duration);
    println!("\n🧪 Quantum mechanics is weird and wonderful!");
    println!("💡 Remember: this is a simplified educational model");
    println!("   Real quantum physics involves much more complexity");
    println!("\n🌌 Keep exploring the quantum realm! 🌌");
}
