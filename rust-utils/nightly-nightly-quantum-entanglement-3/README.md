# Nightly Quantum Entanglement Checker

A whimsical-yet-useful quantum physics simulator that detects entanglement between particles. Perfect for understanding quantum mechanics concepts or adding some quantum fun to your day!

## Features

- Simulates quantum particles with spin states
- Detects quantum entanglement between particle pairs
- Visualizes quantum states with ASCII art
- Educational tool for learning quantum mechanics
- Blazing fast performance with Rust

## Installation

Requires Rust 1.70+ and Cargo:

```bash
# Clone the repository
# cd to the nightly-quantum-entanglement-checker directory
# Build the project
cargo build --release
```

## Usage

```bash
# Run the quantum entanglement checker
cargo run --release

# Or run with specific particle configurations
cargo run --release -- --particles 10 --entangled 3

# Generate quantum state visualization
cargo run --release -- --visualize
```

## Examples

### Basic Entanglement Detection

```rust
use nightly_quantum_entanglement_checker::*;

let mut simulator = QuantumSimulator::new();

// Create two particles
let particle1 = simulator.create_particle(SpinState::Up);
let particle2 = simulator.create_particle(SpinState::Down);

// Attempt to entangle them
if simulator.entangle_particles(particle1, particle2) {
    println!("Successfully entangled particles!");
    
    // Measure one particle (collapses the wave function)
    let result = simulator.measure_particle(particle1);
    println!("Particle 1 measured: {:?}", result);
    
    // The other particle will have the opposite spin!
    let result2 = simulator.measure_particle(particle2);
    println!("Particle 2 measured: {:?}", result2);
} else {
    println!("Failed to entangle particles");
}
```

### Quantum State Visualization

The tool provides ASCII art visualization of quantum states:

```
Particle 1: |↑⟩  (Spin Up)
Particle 2: |↓⟩  (Spin Down)

Entanglement Status: ✓ ENTANGLED

Bell State: |Ψ⁻⟩ = (|↑↓⟩ - |↓↑⟩)/√2
```

## Educational Value

This tool demonstrates key quantum mechanics concepts:

- **Superposition**: Particles exist in multiple states until measured
- **Entanglement**: Particles become correlated regardless of distance
- **Wave Function Collapse**: Measurement forces a definite state
- **Bell States**: Maximally entangled quantum states

## Performance

Built with Rust for maximum performance:

- Zero-cost abstractions
- Memory safety without garbage collection
- Concurrency without data races
- SIMD optimizations for large particle simulations

## Testing

Run the test suite:

```bash
cargo test
```

## License

MIT License - feel free to use for educational and entertainment purposes!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Submit a pull request

## Quantum Disclaimer

This is a simplified educational tool. Real quantum mechanics is much more complex and involves phenomena like decoherence, quantum tunneling, and relativistic effects. But hey, every quantum journey starts somewhere! 🌌
