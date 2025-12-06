pub use joke_generator::{Joke, JokeStyle, QuantumQuipGenerator};

pub mod joke_generator {
    use rand::seq::SliceRandom;
    use rand::thread_rng;
    use serde::{Deserialize, Serialize};
    use std::io;
    use std::fs;

    #[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
    pub struct Joke {
        pub id: u32,
        pub text: String,
        pub style: JokeStyle,
    }

    #[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
    pub enum JokeStyle {
        Quantum,
        Programming,
        Mixed,
    }

    impl ToString for JokeStyle {
        fn to_string(&self) -> String {
            match self {
                JokeStyle::Quantum => "quantum".to_string(),
                JokeStyle::Programming => "programming".to_string(),
                JokeStyle::Mixed => "mixed".to_string(),
            }
        }
    }

    pub struct QuantumQuipGenerator {
        jokes: Vec<Joke>,
    }

    impl QuantumQuipGenerator {
        pub fn new() -> Self {
            let jokes = vec![
                Joke {
                    id: 1,
                    text: "Why don't quantum programmers ever make decisions? Because they exist in a superposition of states until observed!".to_string(),
                    style: JokeStyle::Mixed,
                },
                Joke {
                    id: 2,
                    text: "What do you call a quantum computer that tells jokes? A qubit of humor!".to_string(),
                    style: JokeStyle::Mixed,
                },
                Joke {
                    id: 3,
                    text: "Why did Schrödinger's cat start a coding blog? Because it wanted to share its thoughts on being both alive and dead in the tech world!".to_string(),
                    style: JokeStyle::Mixed,
                },
                Joke {
                    id: 4,
                    text: "How many quantum programmers does it take to change a light bulb? None, they just observe it in the dark until it decides to be on!".to_string(),
                    style: JokeStyle::Quantum,
                },
                Joke {
                    id: 5,
                    text: "Why do quantum algorithms make terrible comedians? Their punchlines are always in superposition until someone measures them!".to_string(),
                    style: JokeStyle::Programming,
                },
            ];
            
            Self { jokes }
        }

        pub fn generate_joke(&self, style: &JokeStyle) -> &Joke {
            let mut rng = thread_rng();
            
            let filtered_jokes: Vec<&Joke> = match style {
                JokeStyle::Quantum => self.jokes.iter().filter(|j| j.style == JokeStyle::Quantum || j.style == JokeStyle::Mixed).collect(),
                JokeStyle::Programming => self.jokes.iter().filter(|j| j.style == JokeStyle::Programming || j.style == JokeStyle::Mixed).collect(),
                JokeStyle::Mixed => self.jokes.iter().collect(),
            };
            
            filtered_jokes.choose(&mut rng).unwrap_or(&self.jokes[0])
        }

        pub fn generate_multiple_jokes(&self, count: usize, style: &JokeStyle) -> Vec<&Joke> {
            (0..count).map(|_| self.generate_joke(style)).collect()
        }

        pub fn export_to_json(&self, jokes: Vec<&Joke>, filename: &str) -> io::Result<()> {
            let jokes_data: Vec<&Joke> = jokes;
            let json = serde_json::to_string_pretty(&jokes_data)?;
            fs::write(filename, json)?;
            Ok(())
        }

        pub fn export_to_text(&self, jokes: Vec<&Joke>, filename: &str) -> io::Result<()> {
            let content = jokes.iter()
                .map(|j| format!("{}\n\n", j.text))
                .collect::<String>();
            fs::write(filename, content)?;
            Ok(())
        }
    }
}
