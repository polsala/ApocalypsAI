use nightly_quantum_quip_generator::joke_generator::{Joke, JokeStyle, QuantumQuipGenerator};
use std::fs;
use tempfile::NamedTempFile;

#[test]
fn test_generate_joke_quantum_style() {
    let generator = QuantumQuipGenerator::new();
    let joke = generator.generate_joke(&JokeStyle::Quantum);
    
    assert!(joke.style == JokeStyle::Quantum || joke.style == JokeStyle::Mixed);
    assert!(!joke.text.is_empty());
    assert!(joke.id > 0);
}

#[test]
fn test_generate_joke_programming_style() {
    let generator = QuantumQuipGenerator::new();
    let joke = generator.generate_joke(&JokeStyle::Programming);
    
    assert!(joke.style == JokeStyle::Programming || joke.style == JokeStyle::Mixed);
    assert!(!joke.text.is_empty());
    assert!(joke.id > 0);
}

#[test]
fn test_generate_joke_mixed_style() {
    let generator = QuantumQuipGenerator::new();
    let joke = generator.generate_joke(&JokeStyle::Mixed);
    
    assert!(joke.style == JokeStyle::Mixed);
    assert!(!joke.text.is_empty());
    assert!(joke.id > 0);
}

#[test]
fn test_generate_multiple_jokes() {
    let generator = QuantumQuipGenerator::new();
    let jokes = generator.generate_multiple_jokes(3, &JokeStyle::Mixed);
    
    assert_eq!(jokes.len(), 3);
    for joke in jokes {
        assert!(!joke.text.is_empty());
        assert!(joke.id > 0);
    }
}

#[test]
fn test_export_to_json() {
    let generator = QuantumQuipGenerator::new();
    let jokes = generator.generate_multiple_jokes(2, &JokeStyle::Mixed);
    
    let temp_file = NamedTempFile::new().unwrap();
    let file_path = temp_file.path().to_str().unwrap();
    
    let result = generator.export_to_json(jokes, file_path);
    assert!(result.is_ok());
    
    let content = fs::read_to_string(file_path).unwrap();
    assert!(content.contains("text"));
    assert!(content.contains("id"));
    assert!(content.contains("style"));
}

#[test]
fn test_export_to_text() {
    let generator = QuantumQuipGenerator::new();
    let jokes = generator.generate_multiple_jokes(2, &JokeStyle::Mixed);
    
    let temp_file = NamedTempFile::new().unwrap();
    let file_path = temp_file.path().to_str().unwrap();
    
    let result = generator.export_to_text(jokes, file_path);
    assert!(result.is_ok());
    
    let content = fs::read_to_string(file_path).unwrap();
    assert!(content.contains(&jokes[0].text));
    assert!(content.contains(&jokes[1].text));
}

#[test]
fn test_joke_style_to_string() {
    assert_eq!(JokeStyle::Quantum.to_string(), "quantum");
    assert_eq!(JokeStyle::Programming.to_string(), "programming");
    assert_eq!(JokeStyle::Mixed.to_string(), "mixed");
}

#[test]
fn test_joke_equality() {
    let joke1 = Joke {
        id: 1,
        text: "Test joke".to_string(),
        style: JokeStyle::Mixed,
    };
    
    let joke2 = Joke {
        id: 1,
        text: "Test joke".to_string(),
        style: JokeStyle::Mixed,
    };
    
    assert_eq!(joke1, joke2);
}

#[test]
fn test_generator_has_jokes() {
    let generator = QuantumQuipGenerator::new();
    
    // Test that we can generate jokes without panicking
    let _joke1 = generator.generate_joke(&JokeStyle::Quantum);
    let _joke2 = generator.generate_joke(&JokeStyle::Programming);
    let _joke3 = generator.generate_joke(&JokeStyle::Mixed);
}
