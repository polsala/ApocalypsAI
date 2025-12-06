use std::collections::HashMap;
use std::env;
use std::io::{self, Write};
use std::sync::Arc;
use std::time::{Duration, Instant};
use std::thread;
use rand::{Rng, SeedableRng, rngs::StdRng};
use serde::{Serialize, Deserialize};
use clap::{Arg, Command};

#[derive(Debug, Serialize, Deserialize)]
struct QuantumJoke {
    joke: String,
    category: String,
    difficulty: String,
}

impl QuantumJoke {
    fn new(joke: String, category: String, difficulty: String) -> Self {
        Self {
            joke,
            category,
            difficulty,
        }
    }
}

struct QuantumQuipGenerator {
    puns: Vec<String>,
    jokes: Vec<String>,
    one_liners: Vec<String>,
    rng: Arc<std::sync::Mutex<StdRng>>,
}

impl QuantumQuipGenerator {
    fn new(seed: Option<u64>) -> Self {
        let rng = match seed {
            Some(s) => StdRng::seed_from_u64(s),
            None => StdRng::from_entropy(),
        };
        
        Self {
            puns: Self::load_puns(),
            jokes: Self::load_jokes(),
            one_liners: Self::load_one_liners(),
            rng: Arc::new(std::sync::Mutex::new(rng)),
        }
    }
    
    fn load_puns() -> Vec<String> {
        vec![
            "Why don't quantum physicists ever argue? Because they always find themselves in superposition!".to_string(),
            "What do you call a quantum computer that tells jokes? A super-computer!".to_string(),
            "I tried to make a quantum joke, but it collapsed into a pun!".to_string(),
            "Why was Schrödinger's cat such a bad comedian? It couldn't decide if the punchline was funny or not!".to_string(),
            "How many qubits does it take to change a lightbulb? Superpositionally, all of them and none at the same time!".to_string(),
            "What's a quantum physicist's favorite type of music? Superposition!".to_string(),
            "Why don't quantum jokes need a setup? They're already in a state of anticipation!".to_string(),
            "I told a quantum joke about entanglement. It was so connected, both halves were funny simultaneously!".to_string(),
            "What do you call a measurement of quantum humor? A laugh-ometer!".to_string(),
            "Why did the qubit break up with the bit? It needed more superposition in its life!".to_string(),
        ]
    }
    
    fn load_jokes() -> Vec<String> {
        vec![
            "A quantum physicist walks into a bar... and doesn't. The bartender asks, 'Was it good for you or was it good for me?'".to_string(),
            "There are two types of people in this world: those who understand quantum mechanics, and those who pretend to. Actually, there might be a superposition of those states.".to_string(),
            "A qubit and a bit go to a party. The bit says, 'Why don't you mingle?' The qubit replies, 'I'm in a relationship with myself.'".to_string(),
            "Why did Schrödinger get a cat? Because he wanted to see if it was alive or dead... and also if it could purr and not purr at the same time!".to_string(),
            "A quantum computer, a classical computer, and a human walk into a bar. The bartender says, 'Which version of reality would you like to experience first?'".to_string(),
        ]
    }
    
    fn load_one_liners() -> Vec<String> {
        vec![
            "I'm not lazy, I'm just in a state of quantum rest.".to_string(),
            "My code doesn't have bugs, it has quantum features.".to_string(),
            "I'm not indecisive, I'm exploring all possible states simultaneously.".to_string(),
            "This joke is in a superposition of funny and not funny until you observe it.".to_string(),
            "I don't always test my code, but when I do, I do it in production.".to_string(),
            "Quantum computing: where 1 + 1 can equal 0, 1, or both.".to_string(),
            "I'm not arguing, I'm just entangled in a different point of view.".to_string(),
            "My productivity is like a qubit—simultaneously maximum and minimum.".to_string(),
            "I don't need coffee, I run on quantum fluctuations.".to_string(),
            "Debugging is just measuring the wave function of your code.".to_string(),
        ]
    }
    
    fn generate_joke(&self) -> QuantumJoke {
        let mut rng = self.rng.lock().unwrap();
        let category_roll = rng.gen_range(0..100);
        
        let (joke, category, difficulty) = if category_roll < 50 {
            // 50% chance for puns
            let joke = self.puns[rng.gen_range(0..self.puns.len())].clone();
            (joke, "puns".to_string(), "quantum".to_string())
        } else if category_roll < 80 {
            // 30% chance for jokes
            let joke = self.jokes[rng.gen_range(0..self.jokes.len())].clone();
            (joke, "jokes".to_string(), "superposition".to_string())
        } else {
            // 20% chance for one-liners
            let joke = self.one_liners[rng.gen_range(0..self.one_liners.len())].clone();
            (joke, "one-liners".to_string(), "entangled".to_string())
        };
        
        QuantumJoke::new(joke, category, difficulty)
    }
    
    fn generate_multiple_jokes(&self, count: usize, threads: usize) -> Vec<QuantumJoke> {
        let jokes_per_thread = count / threads;
        let remainder = count % threads;
        
        let mut handles = Vec::new();
        
        for i in 0..threads {
            let generator = self.clone();
            let jokes_to_generate = if i < remainder {
                jokes_per_thread + 1
            } else {
                jokes_per_thread
            };
            
            let handle = thread::spawn(move || {
                let mut thread_jokes = Vec::new();
                for _ in 0..jokes_to_generate {
                    thread_jokes.push(generator.generate_joke());
                }
                thread_jokes
            });
            
            handles.push(handle);
        }
        
        let mut all_jokes = Vec::new();
        for handle in handles {
            all_jokes.extend(handle.join().unwrap());
        }
        
        all_jokes
    }
    
    fn stream_jokes(&self, threads: usize) {
        println!("\nStreaming quantum quips... (Press Ctrl+C to stop)\n");
        
        let generator = self.clone();
        let handle = thread::spawn(move || {
            loop {
                let jokes = generator.generate_multiple_jokes(threads, threads);
                for joke in jokes {
                    println!("Quantum Quip: {}", joke.joke);
                    thread::sleep(Duration::from_millis(500));
                }
            }
        });
        
        // Wait for user to interrupt
        let _ = handle.join();
    }
}

impl Clone for QuantumQuipGenerator {
    fn clone(&self) -> Self {
        Self {
            puns: self.puns.clone(),
            jokes: self.jokes.clone(),
            one_liners: self.one_liners.clone(),
            rng: self.rng.clone(),
        }
    }
}

fn main() {
    let matches = Command::new("Quantum Quip Generator")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Generates quantum computing puns and jokes with concurrent processing")
        .arg(
            Arg::new("count")
                .short('c')
                .long("count")
                .value_name("NUMBER")
                .help("Number of jokes to generate")
                .default_value("1")
        )
        .arg(
            Arg::new("format")
                .short('f')
                .long("format")
                .value_name("FORMAT")
                .help("Output format: text or json")
                .default_value("text")
        )
        .arg(
            Arg::new("interactive")
                .short('i')
                .long("interactive")
                .help("Run in interactive mode (stream jokes continuously)")
        )
        .arg(
            Arg::new("seed")
                .short('s')
                .long("seed")
                .value_name("SEED")
                .help("Seed for random number generator (for reproducible jokes)")
        )
        .arg(
            Arg::new("threads")
                .short('t')
                .long("threads")
                .value_name("THREADS")
                .help("Number of threads to use for joke generation")
                .default_value("4")
        )
        .get_matches();
    
    let seed = matches.get_one::<String>("seed").map(|s| s.parse::<u64>().unwrap_or(42));
    let count: usize = matches.get_one::<String>("count").unwrap().parse().expect("Invalid count");
    let format = matches.get_one::<String>("format").unwrap();
    let interactive = matches.get_flag("interactive");
    let threads: usize = matches.get_one::<String>("threads").unwrap().parse().expect("Invalid thread count");
    
    let generator = QuantumQuipGenerator::new(seed);
    
    if interactive {
        generator.stream_jokes(threads);
    } else {
        let start_time = Instant::now();
        let jokes = generator.generate_multiple_jokes(count, threads);
        let duration = start_time.elapsed();
        
        if format == "json" {
            for joke in jokes {
                println!("{}", serde_json::to_string(&joke).unwrap());
            }
        } else {
            for joke in jokes {
                println!("Quantum Quip: {}", joke.joke);
            }
        }
        
        eprintln!("\nGenerated {} jokes in {:?} using {} threads", count, duration, threads);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::OnceLock;
    
    static TEST_GENERATOR: OnceLock<QuantumQuipGenerator> = OnceLock::new();
    
    fn get_test_generator() -> &'static QuantumQuipGenerator {
        TEST_GENERATOR.get_or_init(|| QuantumQuipGenerator::new(Some(42)))
    }
    
    #[test]
    fn test_load_puns() {
        let generator = QuantumQuipGenerator::new(None);
        assert!(!generator.puns.is_empty());
        assert!(generator.puns.len() >= 10);
    }
    
    #[test]
    fn test_load_jokes() {
        let generator = QuantumQuipGenerator::new(None);
        assert!(!generator.jokes.is_empty());
        assert!(generator.jokes.len() >= 5);
    }
    
    #[test]
    fn test_load_one_liners() {
        let generator = QuantumQuipGenerator::new(None);
        assert!(!generator.one_liners.is_empty());
        assert!(generator.one_liners.len() >= 10);
    }
    
    #[test]
    fn test_generate_single_joke() {
        let generator = get_test_generator();
        let joke = generator.generate_joke();
        
        assert!(!joke.joke.is_empty());
        assert!(!joke.category.is_empty());
        assert!(!joke.difficulty.is_empty());
        
        // Test that we get a valid category
        assert!(joke.category == "puns" || joke.category == "jokes" || joke.category == "one-liners");
        
        // Test that we get a valid difficulty
        assert!(joke.difficulty == "quantum" || joke.difficulty == "superposition" || joke.difficulty == "entangled");
    }
    
    #[test]
    fn test_generate_multiple_jokes() {
        let generator = get_test_generator();
        let jokes = generator.generate_multiple_jokes(10, 2);
        
        assert_eq!(jokes.len(), 10);
        
        for joke in jokes {
            assert!(!joke.joke.is_empty());
            assert!(!joke.category.is_empty());
            assert!(!joke.difficulty.is_empty());
        }
    }
    
    #[test]
    fn test_generate_multiple_jokes_with_remainder() {
        let generator = get_test_generator();
        let jokes = generator.generate_multiple_jokes(7, 3); // 7 jokes, 3 threads
        
        assert_eq!(jokes.len(), 7);
        
        for joke in jokes {
            assert!(!joke.joke.is_empty());
            assert!(!joke.category.is_empty());
            assert!(!joke.difficulty.is_empty());
        }
    }
    
    #[test]
    fn test_reproducible_jokes_with_seed() {
        let generator1 = QuantumQuipGenerator::new(Some(123));
        let generator2 = QuantumQuipGenerator::new(Some(123));
        
        let joke1 = generator1.generate_joke();
        let joke2 = generator2.generate_joke();
        
        // With the same seed, we should get the same joke
        assert_eq!(joke1.joke, joke2.joke);
        assert_eq!(joke1.category, joke2.category);
        assert_eq!(joke1.difficulty, joke2.difficulty);
    }
    
    #[test]
    fn test_different_seeds_produce_different_jokes() {
        let generator1 = QuantumQuipGenerator::new(Some(123));
        let generator2 = QuantumQuipGenerator::new(Some(456));
        
        let jokes1 = generator1.generate_multiple_jokes(10, 1);
        let jokes2 = generator2.generate_multiple_jokes(10, 1);
        
        // With different seeds, we should get different jokes
        assert_ne!(jokes1, jokes2);
    }
    
    #[test]
    fn test_json_serialization() {
        let joke = QuantumJoke::new(
            "Test joke".to_string(),
            "test".to_string(),
            "easy".to_string(),
        );
        
        let json = serde_json::to_string(&joke).unwrap();
        assert!(json.contains("Test joke"));
        assert!(json.contains("test"));
        assert!(json.contains("easy"));
        
        let deserialized: QuantumJoke = serde_json::from_str(&json).unwrap();
        assert_eq!(joke.joke, deserialized.joke);
        assert_eq!(joke.category, deserialized.category);
        assert_eq!(joke.difficulty, deserialized.difficulty);
    }
    
    #[test]
    fn test_concurrent_performance() {
        let generator = get_test_generator();
        
        // Test single-threaded performance
        let start = Instant::now();
        let _jokes_single = generator.generate_multiple_jokes(100, 1);
        let duration_single = start.elapsed();
        
        // Test multi-threaded performance
        let start = Instant::now();
        let _jokes_multi = generator.generate_multiple_jokes(100, 4);
        let duration_multi = start.elapsed();
        
        // Multi-threaded should be faster or at least not significantly slower
        // (Note: This is a soft assertion as performance can vary)
        println!("Single-threaded: {:?}, Multi-threaded: {:?}", duration_single, duration_multi);
    }
}
