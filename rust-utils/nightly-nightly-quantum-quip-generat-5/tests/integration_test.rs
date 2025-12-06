use nightly_quantum_quip_generator::*;
use std::fs;
use std::path::Path;

#[test]
fn test_joke_generation_deterministic() {
    let mut generator1 = JokeGenerator::new(42);
    let mut generator2 = JokeGenerator::new(42);
    
    // Generate jokes with same seed
    let joke1 = generator1.generate_joke(JokeCategory::Any);
    let joke2 = generator2.generate_joke(JokeCategory::Any);
    
    // Should be identical
    assert_eq!(joke1.setup, joke2.setup);
    assert_eq!(joke1.punchline, joke2.punchline);
    assert_eq!(joke1.explanation, joke2.explanation);
}

#[test]
fn test_joke_generation_different_seeds() {
    let mut generator1 = JokeGenerator::new(42);
    let mut generator2 = JokeGenerator::new(123);
    
    // Generate multiple jokes
    for _ in 0..10 {
        let joke1 = generator1.generate_joke(JokeCategory::Any);
        let joke2 = generator2.generate_joke(JokeCategory::Any);
        
        // Should be different (very unlikely to be the same)
        assert_ne!(joke1.setup, joke2.setup);
    }
}

#[test]
fn test_category_filtering() {
    let mut generator = JokeGenerator::new(42);
    
    // Test quantum category
    for _ in 0..10 {
        let joke = generator.generate_joke(JokeCategory::Quantum);
        assert_eq!(joke.category, JokeCategory::Quantum);
    }
    
    // Test programming category
    for _ in 0..10 {
        let joke = generator.generate_joke(JokeCategory::Programming);
        assert_eq!(joke.category, JokeCategory::Programming);
    }
    
    // Test AI category
    for _ in 0..10 {
        let joke = generator.generate_joke(JokeCategory::AI);
        assert_eq!(joke.category, JokeCategory::AI);
    }
}

#[test]
fn test_placeholder_replacement() {
    let mut generator = JokeGenerator::new(42);
    
    // Generate a joke that should have placeholders replaced
    let joke = generator.generate_joke(JokeCategory::Any);
    
    // Check that placeholders are replaced
    assert!(!joke.setup.contains("{name}"));
    assert!(!joke.setup.contains("{number}"));
    assert!(!joke.setup.contains("{quantum_term}"));
    assert!(!joke.setup.contains("{programming_term}"));
    assert!(!joke.setup.contains("{ai_term}"));
    
    assert!(!joke.punchline.contains("{name}"));
    assert!(!joke.punchline.contains("{number}"));
    assert!(!joke.punchline.contains("{quantum_term}"));
    assert!(!joke.punchline.contains("{programming_term}"));
    assert!(!joke.punchline.contains("{ai_term}"));
    
    assert!(!joke.explanation.contains("{name}"));
    assert!(!joke.explanation.contains("{number}"));
    assert!(!joke.explanation.contains("{quantum_term}"));
    assert!(!joke.explanation.contains("{programming_term}"));
    assert!(!joke.explanation.contains("{ai_term}"));
}

#[test]
fn test_export_json() {
    let mut generator = JokeGenerator::new(42);
    
    // Generate some jokes
    let jokes: Vec<Joke> = (0..5)
        .map(|_| {
            let joke_data = generator.generate_joke(JokeCategory::Any);
            Joke::new(
                joke_data.category,
                joke_data.setup,
                joke_data.punchline,
                joke_data.explanation,
            )
        })
        .collect();
    
    // Export to JSON
    let temp_file = "/tmp/test_jokes.json";
    export_jokes(&jokes, "json", Some(temp_file)).expect("Failed to export JSON");
    
    // Check file exists and can be read
    assert!(Path::new(temp_file).exists());
    
    let content = fs::read_to_string(temp_file).expect("Failed to read file");
    let parsed: Vec<Joke> = serde_json::from_str(&content).expect("Failed to parse JSON");
    
    assert_eq!(parsed.len(), 5);
    
    // Clean up
    fs::remove_file(temp_file).expect("Failed to remove temp file");
}

#[test]
fn test_export_text() {
    let mut generator = JokeGenerator::new(42);
    
    // Generate some jokes
    let jokes: Vec<Joke> = (0..3)
        .map(|_| {
            let joke_data = generator.generate_joke(JokeCategory::Any);
            Joke::new(
                joke_data.category,
                joke_data.setup,
                joke_data.punchline,
                joke_data.explanation,
            )
        })
        .collect();
    
    // Export to text
    let temp_file = "/tmp/test_jokes.txt";
    export_jokes(&jokes, "text", Some(temp_file)).expect("Failed to export text");
    
    // Check file exists and has content
    assert!(Path::new(temp_file).exists());
    
    let content = fs::read_to_string(temp_file).expect("Failed to read file");
    assert!(content.contains("Category:"));
    assert!(content.contains("Setup:"));
    assert!(content.contains("Punchline:"));
    assert!(content.contains("Explanation:"));
    
    // Clean up
    fs::remove_file(temp_file).expect("Failed to remove temp file");
}

#[test]
fn test_invalid_export_format() {
    let mut generator = JokeGenerator::new(42);
    let jokes: Vec<Joke> = vec![];
    
    // Test invalid format
    let result = export_jokes(&jokes, "invalid", None);
    assert!(result.is_err());
}

#[test]
fn test_joke_data_structure() {
    let mut generator = JokeGenerator::new(42);
    
    // Generate a joke
    let joke_data = generator.generate_joke(JokeCategory::Any);
    
    // Check that all fields are populated
    assert!(!format!("{:?}", joke_data.category).is_empty());
    assert!(!joke_data.setup.is_empty());
    assert!(!joke_data.punchline.is_empty());
    assert!(!joke_data.explanation.is_empty());
}

#[test]
fn test_multiple_joke_generation() {
    let mut generator = JokeGenerator::new(42);
    
    // Generate multiple jokes
    let jokes: Vec<_> = (0..100)
        .map(|_| generator.generate_joke(JokeCategory::Any))
        .collect();
    
    // Check we got the right number
    assert_eq!(jokes.len(), 100);
    
    // Check all jokes have content
    for joke in &jokes {
        assert!(!joke.setup.is_empty());
        assert!(!joke.punchline.is_empty());
        assert!(!joke.explanation.is_empty());
    }
}

#[test]
fn test_seed_setting() {
    let mut generator = JokeGenerator::new(42);
    
    // Generate a joke
    let joke1 = generator.generate_joke(JokeCategory::Any);
    
    // Change seed
    generator.set_seed(123);
    
    // Generate another joke
    let joke2 = generator.generate_joke(JokeCategory::Any);
    
    // Should be different
    assert_ne!(joke1.setup, joke2.setup);
    
    // Set back to original seed
    generator.set_seed(42);
    
    // Should generate same as first
    let joke3 = generator.generate_joke(JokeCategory::Any);
    assert_eq!(joke1.setup, joke3.setup);
    assert_eq!(joke1.punchline, joke3.punchline);
    assert_eq!(joke1.explanation, joke3.explanation);
}
