use std::collections::HashMap;
use std::env;
use std::fs;
use std::io::{self, Write};
use std::time::{SystemTime, UNIX_EPOCH};

const QUANTUM_WORDS: &[&str] = &[
    "quantum", "superposition", "entanglement", "qubit", "decoherence",
    "wavefunction", "probability", "uncertainty", "observation", "collapse",
    "tunneling", "interference", "coherence", "measurement", "particle",
    "wave", "photon", "electron", "spin", "state", "operator", "observable",
    "Hamiltonian", "Schrödinger", "Heisenberg", "Planck", "Einstein",
    "Bohr", "Dirac", "Feynman", "Bell", "quantum", "computing",
    "algorithm", "circuit", "gate", "error", "correction", "noise",
    "teleportation", "cryptography", "key", "distribution", "protocol",
    "hardware", "software", "simulation", "optimization", "machine",
    "learning", "artificial", "intelligence", "neural", "network"
];

const EXPLANATION_WORDS: &[&str] = &[
    "because", "due", "since", "therefore", "thus", "hence", "consequently",
    "as", "result", "effect", "cause", "reason", "explanation",
    "means", "indicates", "shows", "demonstrates", "proves", "evidence",
    "theory", "principle", "law", "rule", "concept", "idea", "thought",
    "understanding", "knowledge", "wisdom", "insight", "comprehension",
    "interpretation", "analysis", "exposition", "clarification", "elucidation"
];

struct MarkovChain {
    transitions: HashMap<String, Vec<String>>,
    states: Vec<String>,
}

impl MarkovChain {
    fn new() -> Self {
        let mut transitions = HashMap::new();
        let mut states = Vec::new();
        
        // Initialize with some basic quantum joke patterns
        let patterns = vec![
            vec!["Why", "don't", "quantum", "physicists", "ever", "play", "hide", "and", "seek"],
            vec!["What", "do", "you", "call", "a", "quantum", "computer", "that", "breaks"],
            vec!["How", "many", "quantum", "programmers", "does", "it", "take", "to", "change", "a", "lightbulb"],
            vec!["Why", "did", "Schrödinger", "get", "a", "bad", "grade"],
            vec!["What's", "the", "difference", "between", "a", "classical", "bit", "and", "a", "qubit"],
        ];
        
        for pattern in patterns {
            for window in pattern.windows(2) {
                if window.len() == 2 {
                    let key = window[0].to_string();
                    let value = window[1].to_string();
                    transitions.entry(key).or_insert_with(Vec::new).push(value);
                    if !states.contains(&window[0].to_string()) {
                        states.push(window[0].to_string());
                    }
                }
            }
            if !states.contains(&pattern.last().unwrap().to_string()) {
                states.push(pattern.last().unwrap().to_string());
            }
        }
        
        Self { transitions, states }
    }
    
    fn generate(&self, length: usize) -> String {
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs() as u64;
        let mut rng = Xorshift::new(seed);
        
        let mut result = Vec::new();
        let mut current = self.states[rng.next() % self.states.len()].clone();
        
        for _ in 0..length {
            result.push(current.clone());
            
            if let Some(next_words) = self.transitions.get(&current) {
                if !next_words.is_empty() {
                    current = next_words[rng.next() % next_words.len()].clone();
                } else {
                    current = self.states[rng.next() % self.states.len()].clone();
                }
            } else {
                current = self.states[rng.next() % self.states.len()].clone();
            }
        }
        
        result.join(" ")
    }
}

struct Xorshift {
    state: u32,
}

impl Xorshift {
    fn new(seed: u64) -> Self {
        Self { state: seed as u32 | 1 }
    }
    
    fn next(&mut self) -> u32 {
        self.state ^= self.state << 13;
        self.state ^= self.state >> 17;
        self.state ^= self.state << 5;
        self.state
    }
}

struct QuantumQuipGenerator {
    joke_chain: MarkovChain,
    explanation_chain: MarkovChain,
}

impl QuantumQuipGenerator {
    fn new() -> Self {
        Self {
            joke_chain: MarkovChain::new(),
            explanation_chain: MarkovChain::new(),
        }
    }
    
    fn generate_joke(&self) -> String {
        let joke_patterns = vec![
            "Why don't quantum physicists ever play hide and seek? Because you can never truly find them in a superposition!",
            "What do you call a quantum computer that breaks? A decoherence machine!",
            "How many quantum programmers does it take to change a lightbulb? None, they just put it in a superposition of on and off!",
            "Why did Schrödinger get a bad grade? Because his cat kept interfering with his homework!",
            "What's the difference between a classical bit and a qubit? One is definite, the other is superpositionally challenged!",
            "Why don't quantum particles ever get lost? Because they're always in a state of quantum entanglement!",
            "What do you get when you cross a quantum computer with a philosopher? A machine that can think about thinking while simultaneously not thinking!",
            "Why was the quantum computer cold? It left its Windows open!",
            "How do quantum physicists organize their books? By quantum shelving!",
            "What's a qubit's favorite type of music? Quantum rock and roll!",
        ];
        
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs() as u64;
        let rng = seed as usize % joke_patterns.len();
        
        joke_patterns[rng].to_string()
    }
    
    fn generate_explanation(&self) -> String {
        let explanations = vec![
            "In quantum mechanics, particles can exist in multiple states simultaneously through superposition. This means a quantum physicist could theoretically be both hiding AND seeking at the same time, making the game rather confusing!",
            "Decoherence occurs when a quantum system loses its quantum properties due to interaction with the environment. A 'decoherence machine' would be one that constantly loses its quantum behavior!",
            "Superposition allows qubits to be in multiple states at once. So a lightbulb in superposition would be both on and off simultaneously, making traditional bulb-changing unnecessary!",
            "Schrödinger's famous thought experiment involves a cat in a box that's simultaneously alive and dead. The cat's quantum state would definitely interfere with any homework!",
            "Classical bits are binary (0 or 1), while qubits can be in superposition of both states. Being 'superpositionally challenged' is a playful way to describe this quantum property!",
            "Quantum entanglement creates correlations between particles regardless of distance. If two particles are entangled, knowing the state of one instantly tells you about the other!",
            "Quantum computers can exist in superposition of states, much like how philosophers think about abstract concepts. Combining them creates a system that can contemplate its own existence!",
            "This is a play on 'Windows' as both an operating system and literal windows. Quantum computers don't actually run Windows, but the joke works on multiple levels!",
            "Quantum shelving refers to storing quantum information in specific energy levels. It's also a pun on organizing physical books on shelves!",
            "Quantum rock and roll plays on the idea of quantum states 'rolling' between different possibilities, much like rock and roll music!",
        ];
        
        let seed = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs() as u64;
        let rng = seed as usize % explanations.len();
        
        explanations[rng].to_string()
    }
}

fn print_help() {
    println!("Quantum Quip Generator - Generate quantum computing jokes and explanations");
    println!("");
    println!("Usage:");
    println!("  nightly-quantum-quip-generator [OPTIONS]");
    println!("");
    println!("Options:");
    println!("  --format <FORMAT>    Output format: text, json, markdown (default: text)");
    println!("  --help               Show this help message");
    println!("");
    println!("Examples:");
    println!("  nightly-quantum-quip-generator");
    println!("  nightly-quantum-quip-generator --format json");
    println!("  nightly-quantum-quip-generator --format markdown");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() > 1 && (args[1] == "--help" || args[1] == "-h") {
        print_help();
        return;
    }
    
    let format = if args.len() > 2 && args[1] == "--format" {
        &args[2]
    } else {
        "text"
    };
    
    let generator = QuantumQuipGenerator::new();
    let joke = generator.generate_joke();
    let explanation = generator.generate_explanation();
    
    match format {
        "json" => {
            println!("{{");
            println!("  \"quip\": \"{}\",", joke);
            println!("  \"explanation\": \"{}\",", explanation);
            println!("  \"timestamp\": {},", SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs());
            println!("  \"category\": \"quantum-computing\"");
            println!("}}");
        }
        "markdown" => {
            println!("# 🔮 Quantum Quip of the Moment");
            println!("");
            println!("> {}", joke);
            println!("");
            println!("## 📚 Explanation");
            println!("");
            println!("{}", explanation);
            println!("");
            println!("*Generated at {}*", SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs());
        }
        _ => {
            println!("🔮 Quantum Quip of the Moment:");
            println!("");
            println!("{}", joke);
            println!("");
            println!("📚 Explanation:");
            println!("{}", explanation);
        }
    }
}
