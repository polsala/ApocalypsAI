use clap::Parser;
use rand::{rngs::StdRng, Rng, SeedableRng};
use std::time::{SystemTime, UNIX_EPOCH};

/// A whimsical CLI tool that generates quantum-themed programming jokes
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Custom seed for reproducible joke generation (optional)
    #[arg(short, long)]
    seed: Option<u64>,
}

/// Quantum-themed programming jokes
const QUANTUM_JOKES: &[&str] = &[
    "Why do quantum programmers never make decisions? Because they exist in a superposition of both committing and not committing until observed!",
    "How many quantum developers does it take to change a light bulb? None — they just tunnel through the uncertainty barrier!",
    "What's a quantum programmer's favorite git command? git push --force-with-quantum-entanglement!",
    "Why don't quantum jokes need punchlines? They exist in a superposition of funny and not funny until observed!",
    "What do you call a quantum computer that tells jokes? A superposition of a stand-up and a flop!",
    "Why did the quantum developer break up with classical code? It was too deterministic and lacked entanglement!",
    "How do quantum programmers debug their code? They observe the wave function collapse!",
    "What's the difference between a quantum joke and a classical joke? The quantum one has multiple interpretations until you measure it!",
    "Why do quantum algorithms make terrible comedians? Their punchlines are always in superposition!",
    "What do you get when you cross a quantum physicist with a programmer? Someone who can be in two places at once — debugging and writing new bugs!",
];

/// Generate a random seed if none provided
fn get_seed(seed_opt: Option<u64>) -> u64 {
    seed_opt.unwrap_or_else(|| {
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards")
            .as_secs()
    })
}

/// Generate a quantum quip using the provided seed
fn generate_quip(seed: u64) -> &'static str {
    let mut rng = StdRng::seed_from_u64(seed);
    let index = rng.gen_range(0..QUANTUM_JOKES.len());
    QUANTUM_JOKES[index]
}

fn main() {
    let args = Args::parse();
    let seed = get_seed(args.seed);
    let quip = generate_quip(seed);
    println!("{}
", quip);
    
    if args.seed.is_some() {
        println!("(Generated with seed: {})", seed);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use test_generator::TestCases;
    
    #[test]
    fn test_get_seed_with_provided_seed() {
        let seed = get_seed(Some(42));
        assert_eq!(seed, 42);
    }
    
    #[test]
    fn test_get_seed_without_provided_seed() {
        let seed = get_seed(None);
        assert!(seed > 0);
    }
    
    #[test]
    fn test_generate_quip_with_seed_0() {
        let quip = generate_quip(0);
        assert!(QUANTUM_JOKES.contains(&quip));
    }
    
    #[test]
    fn test_generate_quip_with_seed_1() {
        let quip = generate_quip(1);
        assert!(QUANTUM_JOKES.contains(&quip));
    }
    
    #[test]
    fn test_generate_quip_with_seed_42() {
        let quip = generate_quip(42);
        assert!(QUANTUM_JOKES.contains(&quip));
    }
    
    #[test]
    fn test_generate_quip_with_seed_999() {
        let quip = generate_quip(999);
        assert!(QUANTUM_JOKES.contains(&quip));
    }
    
    #[test]
    fn test_generate_quip_deterministic() {
        let seed = 123;
        let quip1 = generate_quip(seed);
        let quip2 = generate_quip(seed);
        assert_eq!(quip1, quip2);
    }
    
    #[test]
    fn test_generate_quip_different_seeds() {
        let quip1 = generate_quip(1);
        let quip2 = generate_quip(2);
        // While it's possible they could be the same joke, with 10 jokes the probability is low
        // This test mainly ensures the function works with different seeds
        assert!(QUANTUM_JOKES.contains(&quip1));
        assert!(QUANTUM_JOKES.contains(&quip2));
    }
    
    #[test]
    fn test_all_jokes_are_valid() {
        for joke in QUANTUM_JOKES {
            assert!(!joke.is_empty());
            assert!(joke.len() > 10); // Reasonable minimum length
        }
    }
    
    #[test]
    fn test_joke_count() {
        assert!(QUANTUM_JOKES.len() >= 5); // Ensure we have a reasonable number of jokes
    }
}
