use crate::jokes::*;
use crate::pcg::Pcg32;
use std::collections::HashMap;

#[derive(Debug, Clone, Copy)]
pub enum JokeCategory {
    Quantum,
    Programming,
    AI,
    Any,
}

pub struct JokeData {
    pub category: JokeCategory,
    pub setup: String,
    pub punchline: String,
    pub explanation: String,
}

pub struct JokeGenerator {
    rng: Pcg32,
    quantum_jokes: Vec<QuantumJoke>,
    programming_jokes: Vec<ProgrammingJoke>,
    ai_jokes: Vec<AIJoke>,
}

impl JokeGenerator {
    pub fn new(seed: u64) -> Self {
        Self {
            rng: Pcg32::new(seed),
            quantum_jokes: QUANTUM_JOKES.to_vec(),
            programming_jokes: PROGRAMMING_JOKES.to_vec(),
            ai_jokes: AI_JOKES.to_vec(),
        }
    }

    pub fn set_seed(&mut self, seed: u64) {
        self.rng = Pcg32::new(seed);
    }

    pub fn generate_joke(&mut self, category: JokeCategory) -> JokeData {
        let chosen_category = if category == JokeCategory::Any {
            self.select_random_category()
        } else {
            category
        };

        match chosen_category {
            JokeCategory::Quantum => self.generate_quantum_joke(),
            JokeCategory::Programming => self.generate_programming_joke(),
            JokeCategory::AI => self.generate_ai_joke(),
            _ => unreachable!(),
        }
    }

    fn select_random_category(&mut self) -> JokeCategory {
        let roll = self.rng.next_u32() % 3;
        match roll {
            0 => JokeCategory::Quantum,
            1 => JokeCategory::Programming,
            _ => JokeCategory::AI,
        }
    }

    fn generate_quantum_joke(&mut self) -> JokeData {
        let joke = &self.quantum_jokes[self.rng.next_u32() as usize % self.quantum_jokes.len()];
        let setup = self.replace_placeholders(&joke.setup);
        let punchline = self.replace_placeholders(&joke.punchline);
        let explanation = self.replace_placeholders(&joke.explanation);

        JokeData {
            category: JokeCategory::Quantum,
            setup,
            punchline,
            explanation,
        }
    }

    fn generate_programming_joke(&mut self) -> JokeData {
        let joke = &self.programming_jokes[self.rng.next_u32() as usize % self.programming_jokes.len()];
        let setup = self.replace_placeholders(&joke.setup);
        let punchline = self.replace_placeholders(&joke.punchline);
        let explanation = self.replace_placeholders(&joke.explanation);

        JokeData {
            category: JokeCategory::Programming,
            setup,
            punchline,
            explanation,
        }
    }

    fn generate_ai_joke(&mut self) -> JokeData {
        let joke = &self.ai_jokes[self.rng.next_u32() as usize % self.ai_jokes.len()];
        let setup = self.replace_placeholders(&joke.setup);
        let punchline = self.replace_placeholders(&joke.punchline);
        let explanation = self.replace_placeholders(&joke.explanation);

        JokeData {
            category: JokeCategory::AI,
            setup,
            punchline,
            explanation,
        }
    }

    fn replace_placeholders(&mut self, text: &str) -> String {
        let mut result = text.to_string();
        
        // Replace {name} placeholders
        if result.contains("{name}") {
            result = result.replace("{name}", &self.generate_name());
        }
        
        // Replace {number} placeholders
        if result.contains("{number}") {
            result = result.replace("{number}", &self.generate_number().to_string());
        }
        
        // Replace {quantum_term} placeholders
        if result.contains("{quantum_term}") {
            result = result.replace("{quantum_term}", &self.generate_quantum_term());
        }
        
        // Replace {programming_term} placeholders
        if result.contains("{programming_term}") {
            result = result.replace("{programming_term}", &self.generate_programming_term());
        }
        
        // Replace {ai_term} placeholders
        if result.contains("{ai_term}") {
            result = result.replace("{ai_term}", &self.generate_ai_term());
        }
        
        result
    }

    fn generate_name(&mut self) -> String {
        let first_names = ["Schrödinger", "Heisenberg", "Dirac", "Pauli", "Bohr", "Einstein", "Feynman", "Planck", "Curie", "Newton"];
        let last_names = ["Quantum", "Bit", "Byte", "Code", "Logic", "Syntax", "Compile", "Debug", "Runtime", "Variable"];
        
        let first = &first_names[self.rng.next_u32() as usize % first_names.len()];
        let last = &last_names[self.rng.next_u32() as usize % last_names.len()];
        
        format!("{} {}", first, last)
    }

    fn generate_number(&mut self) -> u32 {
        self.rng.next_u32() % 1000
    }

    fn generate_quantum_term(&mut self) -> String {
        let terms = ["superposition", "entanglement", "quantum tunneling", "wave function", "quantum foam", "quantum leap", "quantum state", "quantum field", "quantum particle", "quantum fluctuation"];
        terms[self.rng.next_u32() as usize % terms.len()].to_string()
    }

    fn generate_programming_term(&mut self) -> String {
        let terms = ["function", "variable", "loop", "recursion", "algorithm", "debugger", "compiler", "interpreter", "framework", "library"];
        terms[self.rng.next_u32() as usize % terms.len()].to_string()
    }

    fn generate_ai_term(&mut self) -> String {
        let terms = ["neural network", "machine learning", "deep learning", "artificial intelligence", "algorithm", "training data", "neural pathway", "cognitive computing", "pattern recognition", "natural language processing"];
        terms[self.rng.next_u32() as usize % terms.len()].to_string()
    }
}
