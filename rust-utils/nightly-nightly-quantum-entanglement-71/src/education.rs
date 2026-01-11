use std::io::{self, Write};

/// Learn about quantum mechanics concepts
pub fn learn_concept(concept: &str, interactive: bool) {
    match concept.to_lowercase().as_str() {
        "bell-inequality" | "bell" => explain_bell_inequality(interactive),
        "superposition" => explain_superposition(interactive),
        "decoherence" => explain_decoherence(interactive),
        "teleportation" => explain_teleportation(interactive),
        _ => {
            println!("📚 Available concepts:");
            println!("  • bell-inequality - Bell's theorem and CHSH inequality");
            println!("  • superposition - Quantum superposition principle");
            println!("  • decoherence - Quantum decoherence effects");
            println!("  • teleportation - Quantum teleportation protocol");
        },
    }
}

fn explain_bell_inequality(interactive: bool) {
    println!("⚛️  Bell's Inequality and Quantum Entanglement\n");
    
    println!("📖 Theory:");
    println!("   Bell's theorem shows that no physical theory based on local hidden variables");
    println!("   can reproduce all the predictions of quantum mechanics.");
    
    println!("\n🧪 CHSH Inequality:");
    println!("   |E(a,b) - E(a,b') + E(a',b) + E(a',b')| ≤ 2");
    println!("   \n   Where E represents correlation measurements with different settings.");
    
    println!("\n🔬 Quantum Prediction:");
    println!("   Quantum mechanics can achieve up to 2√2 ≈ 2.828");
    println!("   This violates the classical limit of 2!");
    
    if interactive {
        run_bell_quiz();
    }
}

fn explain_superposition(interactive: bool) {
    println!("⚛️  Quantum Superposition\n");
    
    println!("📖 Theory:");
    println!("   A quantum system can exist in multiple states simultaneously");
    println!("   until measured. This is the foundation of quantum computing.");
    
    println!("\n🔬 Mathematical Representation:");
    println!("   |ψ⟩ = α|0⟩ + β|1⟩");
    println!("   \n   Where |α|² + |β|² = 1 (normalization)");
    
    println!("\n💡 Example:");
    println!("   Schrödinger's cat is both alive AND dead until observed!");
    
    if interactive {
        run_superposition_quiz();
    }
}

fn explain_decoherence(interactive: bool) {
    println!("⚛️  Quantum Decoherence\n");
    
    println!("📖 Theory:");
    println!("   Decoherence is the loss of quantum coherence due to interaction");
    println!("   with the environment. It's why quantum effects are hard to observe.");
    
    println!("\n🔬 Mathematical Model:");
    println!("   ρ(t) = ρ(0) × e^(-γt)");
    println!("   \n   Where γ is the decoherence rate and t is time.");
    
    println!("\n💡 Real-world Impact:");
    println!("   • Quantum computers need extreme isolation");
    println!("   • Superconducting qubits operate near absolute zero");
    println!("   • Photons can maintain coherence over long distances");
    
    if interactive {
        run_decoherence_quiz();
    }
}

fn explain_teleportation(interactive: bool) {
    println!("⚛️  Quantum Teleportation\n");
    
    println!("📖 Theory:");
    println!("   Quantum teleportation transfers quantum information using");
    println!("   entanglement and classical communication. No matter is moved!");
    
    println!("\n🔬 Protocol Steps:");
    println!("   1. Create entangled pair (Alice & Bob)");
    println!("   2. Alice performs Bell measurement on her qubit + message");
    println!("   3. Alice sends classical results to Bob");
    println!("   4. Bob applies corrections to recover the message");
    
    println!("\n💡 Key Points:");
    println!("   • No faster-than-light communication");
    println!("   • Original state is destroyed (no cloning)");
    println!("   • Requires pre-shared entanglement");
    
    if interactive {
        run_teleportation_quiz();
    }
}

fn run_bell_quiz() {
    println!("\n🎯 Interactive Quiz: Bell's Inequality");
    println!("\nQuestion: What is the maximum CHSH value allowed by classical physics?");
    
    print!("Your answer: ");
    io::stdout().flush().unwrap();
    
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    
    match input.trim() {
        "2" => println!("✅ Correct! Classical physics limits CHSH to 2."),
        _ => println!("❌ The correct answer is 2. Classical correlations cannot exceed this limit."),
    }
    
    println!("\nQuestion: What CHSH value can quantum mechanics achieve?");
    
    print!("Your answer: ");
    io::stdout().flush().unwrap();
    
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    
    match input.trim() {
        "2.828" | "2.83" | "2√2" | "two root two" => {
            println!("✅ Excellent! Quantum mechanics can reach 2√2 ≈ 2.828.");
        },
        _ => println!("❌ The answer is 2√2 ≈ 2.828. This demonstrates quantum non-locality."),
    }
}

fn run_superposition_quiz() {
    println!("\n🎯 Interactive Quiz: Superposition");
    println!("\nQuestion: If a qubit is in state |+⟩ = (|0⟩ + |1⟩)/√2, what's the probability of measuring |0⟩?");
    
    print!("Your answer: ");
    io::stdout().flush().unwrap();
    
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    
    match input.trim() {
        "0.5" | "50%" | "1/2" => println!("✅ Correct! |+⟩ has equal probability for |0⟩ and |1⟩."),
        _ => println!("❌ The probability is 0.5 (50%). The amplitudes are both 1/√2."),
    }
}

fn run_decoherence_quiz() {
    println!("\n🎯 Interactive Quiz: Decoherence");
    println!("\nQuestion: What happens to quantum superposition over time due to decoherence?");
    
    println!("A) It gets stronger");
    println!("B) It becomes classical");
    println!("C) It oscillates");
    println!("D) Nothing changes");
    
    print!("Your choice (A/B/C/D): ");
    io::stdout().flush().unwrap();
    
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    
    match input.trim().to_uppercase().as_str() {
        "B" => println!("✅ Correct! Decoherence destroys quantum superposition, making it classical."),
        _ => println!("❌ The answer is B. Decoherence causes quantum-to-classical transition."),
    }
}

fn run_teleportation_quiz() {
    println!("\n🎯 Interactive Quiz: Quantum Teleportation");
    println!("\nQuestion: Can quantum teleportation transmit information faster than light?");
    
    println!("A) Yes, instantaneously");
    println!("B) No, requires classical communication");
    println!("C) Only for entangled particles");
    println!("D) Depends on distance");
    
    print!("Your choice (A/B/C/D): ");
    io::stdout().flush().unwrap();
    
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    
    match input.trim().to_uppercase().as_str() {
        "B" => println!("✅ Correct! Classical communication is required, limiting speed to light."),
        _ => println!("❌ The answer is B. No faster-than-light communication is possible."),
    }
}
