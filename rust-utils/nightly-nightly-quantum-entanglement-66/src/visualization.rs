use crate::quantum::{MeasurementBasis, QuantumState};

pub fn clear_screen() {
    print!("\x1b[2J\x1b[H");
}

pub fn print_header() {
    println!("=== Quantum Entanglement Simulation ===");
    println!("Spooky action at a distance in ASCII! 🎃⚛️");
    println!("");
}

pub fn print_particle_state(state: &QuantumState) {
    println!("  {}: {}", state.to_ascii_symbol(), state.to_string());
}

pub fn print_measurement_result(
    pair_num: usize,
    basis: MeasurementBasis,
    alice_result: &QuantumState,
    bob_result: &QuantumState,
    correlated: bool,
) {
    println!("  Pair {}:", pair_num);
    println!("    Alice measures in {} basis: {}", basis.to_string(), alice_result.to_string());
    println!("    Bob measures in {} basis:  {}", basis.to_string(), bob_result.to_string());
    
    if correlated {
        println!("    Correlation: ✓ Perfect (spooky action!)");
    } else {
        println!("    Correlation: ✗ Broken (decoherence detected)");
    }
    println!("");
}

pub fn progress_bar(percentage: f64) -> String {
    let filled = (percentage * 10.0).round() as usize;
    let empty = 10 - filled;
    format!("{}{}", "█".repeat(filled), "░".repeat(empty))
}
