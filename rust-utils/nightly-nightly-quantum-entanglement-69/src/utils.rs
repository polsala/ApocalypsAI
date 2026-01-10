use rand::seq::SliceRandom;

pub fn display_ascii_art() -> String {
    let art = r#"
  ⚛️  QUANTUM ENTANGLEMENT SIMULATOR ⚛️
  
     ╔═════════════════════════════════╗
     ║    Spooky Action at a Distance  ║
     ║        Now with 100% more      ║
     ║           Whimsy!              ║
     ╚═════════════════════════════════╝
  "#;
    art.to_string()
}

pub fn display_measurement_result(measurement: &crate::quantum_simulator::Measurement) {
    println!("Random Particle State: {} = 0.707|↑⟩ + 0.707|↓⟩", measurement.state);
    println!("Measurement Outcome: {}", measurement.state);
    println!("\nProbability of this outcome: {:.2}%", measurement.probability * 100.0);
    println!("\nFun Fact: {}", measurement.fun_fact);
}

pub fn get_random_particle_name(index: usize) -> String {
    let names = [
        "Schrödinger's Sparkle",
        "Heisenberg's Hilarity", 
        "Pauli's Prankster",
        "Dirac's Doodle",
        "Bohr's Bubbler",
        "Einstein's Echo",
        "Feynman's Fizz",
        "Planck's Prancer",
        "Curie's Curiosity",
        "Tesla's Twinkle",
    ];
    
    let mut rng = rand::thread_rng();
    let name = names.choose(&mut rng).unwrap_or(&"Quantum Quirk");
    
    if index == 0 {
        format!("{} (Primary)", name)
    } else {
        format!("{} (Entangled)", name)
    }
}
