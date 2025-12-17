use sha2::{Digest, Sha256};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum EntanglementState {
    Entangled,
    Correlated,
    Independent,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum OutputFormat {
    Text,
    Json,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EntanglementConfig {
    pub uncertainty_threshold: f64,
    pub verbose: bool,
    pub output_format: OutputFormat,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct EntanglementResult {
    pub file1_path: String,
    pub file2_path: String,
    pub file1_hash: String,
    pub file2_hash: String,
    pub similarity: f64,
    pub entanglement_probability: f64,
    pub hash_distance: f64,
    pub quantum_coherence: f64,
    pub entanglement_state: EntanglementState,
    pub config: EntanglementConfig,
}

pub struct QuantumAnalyzer {
    // Configuration can be extended here
}

impl QuantumAnalyzer {
    pub fn new() -> Self {
        Self {}
    }

    pub async fn analyze_files(
        &self,
        file1_path: &str,
        file2_path: &str,
        config: EntanglementConfig,
    ) -> Result<EntanglementResult, Box<dyn std::error::Error>> {
        let file1_content = self.read_file(file1_path).await?;
        let file2_content = self.read_file(file2_path).await?;
        
        self.analyze_content(&file1_content, file1_path, file2_path, config).await
    }

    pub async fn analyze_content(
        &self,
        file1_content: &str,
        file1_path: &str,
        file2_path: &str,
        config: EntanglementConfig,
    ) -> Result<EntanglementResult, Box<dyn std::error::Error>> {
        // Compute quantum signatures (hashes)
        let file1_hash = self.compute_quantum_signature(file1_content);
        let file2_hash = self.compute_quantum_signature(file2_content);

        // Calculate quantum metrics
        let hash_distance = self.calculate_hash_distance(&file1_hash, &file2_hash);
        let similarity = self.calculate_similarity(hash_distance);
        let quantum_coherence = self.calculate_quantum_coherence(file1_content, file2_content);
        
        // Apply uncertainty principle
        let entanglement_probability = self.apply_uncertainty_principle(
            similarity,
            quantum_coherence,
            config.uncertainty_threshold,
        );

        // Determine entanglement state
        let entanglement_state = self.determine_entanglement_state(
            entanglement_probability,
            config.uncertainty_threshold,
        );

        Ok(EntanglementResult {
            file1_path: file1_path.to_string(),
            file2_path: file2_path.to_string(),
            file1_hash,
            file2_hash,
            similarity,
            entanglement_probability,
            hash_distance,
            quantum_coherence,
            entanglement_state,
            config,
        })
    }

    pub async fn read_file(&self, path: &str) -> Result<String, Box<dyn std::error::Error>> {
        if path == "-" {
            // Read from stdin
            let mut buffer = String::new();
            std::io::Read::read_to_string(&mut std::io::stdin(), &mut buffer)?;
            Ok(buffer)
        } else {
            let content = fs::read_to_string(path)?;
            Ok(content)
        }
    }

    fn compute_quantum_signature(&self, content: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(content.as_bytes());
        let hash = hasher.finalize();
        format!("{:x}", hash)
    }

    fn calculate_hash_distance(&self, hash1: &str, hash2: &str) -> f64 {
        if hash1.len() != hash2.len() {
            return 1.0; // Maximum distance for different length hashes
        }

        let mut differences = 0;
        for (c1, c2) in hash1.chars().zip(hash2.chars()) {
            if c1 != c2 {
                differences += 1;
            }
        }

        differences as f64 / hash1.len() as f64
    }

    fn calculate_similarity(&self, hash_distance: f64) -> f64 {
        1.0 - hash_distance
    }

    fn calculate_quantum_coherence(&self, content1: &str, content2: &str) -> f64 {
        // Simple word-based similarity for additional quantum coherence
        let words1: HashMap<&str, usize> = self.word_frequency(content1);
        let words2: HashMap<&str, usize> = self.word_frequency(content2);

        let all_words: std::collections::HashSet<&str> = 
            words1.keys().chain(words2.keys()).copied().collect();

        let mut dot_product = 0.0;
        let mut norm1_sq = 0.0;
        let mut norm2_sq = 0.0;

        for word in all_words {
            let freq1 = *words1.get(word).unwrap_or(&0) as f64;
            let freq2 = *words2.get(word).unwrap_or(&0) as f64;
            
            dot_product += freq1 * freq2;
            norm1_sq += freq1 * freq1;
            norm2_sq += freq2 * freq2;
        }

        let norm1 = norm1_sq.sqrt();
        let norm2 = norm2_sq.sqrt();

        if norm1 == 0.0 || norm2 == 0.0 {
            0.0
        } else {
            dot_product / (norm1 * norm2)
        }
    }

    fn word_frequency(&self, content: &str) -> HashMap<&str, usize> {
        let mut freq = HashMap::new();
        
        for word in content.split_whitespace() {
            let word = word.trim_matches(|c: char| !c.is_alphanumeric());
            if !word.is_empty() {
                *freq.entry(word).or_insert(0) += 1;
            }
        }
        
        freq
    }

    fn apply_uncertainty_principle(
        &self,
        similarity: f64,
        quantum_coherence: f64,
        uncertainty_threshold: f64,
    ) -> f64 {
        // Combine similarity and coherence with uncertainty
        let base_probability = (similarity + quantum_coherence) / 2.0;
        
        // Apply quantum uncertainty (Heisenberg compensation)
        let uncertainty_factor = 1.0 - uncertainty_threshold;
        let adjusted_probability = base_probability * uncertainty_factor;
        
        // Ensure probability is within bounds
        adjusted_probability.max(0.0).min(1.0)
    }

    fn determine_entanglement_state(
        &self,
        entanglement_probability: f64,
        uncertainty_threshold: f64,
    ) -> EntanglementState {
        let high_threshold = 0.8 + uncertainty_threshold;
        let low_threshold = 0.3 - uncertainty_threshold;

        if entanglement_probability >= high_threshold {
            EntanglementState::Entangled
        } else if entanglement_probability >= low_threshold {
            EntanglementState::Correlated
        } else {
            EntanglementState::Independent
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;

    #[tokio::test]
    async fn test_identical_files_entangled() {
        let analyzer = QuantumAnalyzer::new();
        let config = EntanglementConfig {
            uncertainty_threshold: 0.05,
            verbose: false,
            output_format: OutputFormat::Text,
        };

        let content = "fn hello() { println!(\"world\"); }";
        let result = analyzer
            .analyze_content(content, "file1.rs", "file2.rs", config)
            .await
            .unwrap();

        assert_eq!(result.entanglement_state, EntanglementState::Entangled);
        assert!(result.similarity > 0.9);
        assert!(result.entanglement_probability > 0.8);
    }

    #[tokio::test]
    async fn test_similar_files_correlated() {
        let analyzer = QuantumAnalyzer::new();
        let config = EntanglementConfig {
            uncertainty_threshold: 0.05,
            verbose: false,
            output_format: OutputFormat::Text,
        };

        let content1 = "fn add(a: i32, b: i32) -> i32 { a + b }";
        let content2 = "fn add_numbers(x: i32, y: i32) -> i32 { x + y }";
        
        let result = analyzer
            .analyze_content(content1, "file1.rs", "file2.rs", config)
            .await
            .unwrap();

        assert_eq!(result.entanglement_state, EntanglementState::Correlated);
        assert!(result.similarity > 0.5);
        assert!(result.entanglement_probability < 0.8);
    }

    #[tokio::test]
    async fn test_different_files_independent() {
        let analyzer = QuantumAnalyzer::new();
        let config = EntanglementConfig {
            uncertainty_threshold: 0.05,
            verbose: false,
            output_format: OutputFormat::Text,
        };

        let content1 = "fn add(a: i32, b: i32) -> i32 { a + b }";
        let content2 = "struct Point { x: f64, y: f64 }";
        
        let result = analyzer
            .analyze_content(content1, "file1.rs", "file2.rs", config)
            .await
            .unwrap();

        assert_eq!(result.entanglement_state, EntanglementState::Independent);
        assert!(result.similarity < 0.5);
        assert!(result.entanglement_probability < 0.5);
    }

    #[tokio::test]
    async fn test_hash_distance_calculation() {
        let analyzer = QuantumAnalyzer::new();
        
        // Identical hashes
        let hash1 = "a".repeat(64);
        let hash2 = "a".repeat(64);
        assert_eq!(analyzer.calculate_hash_distance(&hash1, &hash2), 0.0);
        
        // Completely different hashes
        let hash1 = "a".repeat(64);
        let hash2 = "b".repeat(64);
        assert_eq!(analyzer.calculate_hash_distance(&hash1, &hash2), 1.0);
    }

    #[tokio::test]
    async fn test_quantum_coherence_calculation() {
        let analyzer = QuantumAnalyzer::new();
        
        // Identical content
        let content1 = "hello world";
        let content2 = "hello world";
        let coherence = analyzer.calculate_quantum_coherence(content1, content2);
        assert!(coherence > 0.9);
        
        // Different content
        let content1 = "hello world";
        let content2 = "goodbye moon";
        let coherence = analyzer.calculate_quantum_coherence(content1, content2);
        assert!(coherence < 0.1);
    }

    #[tokio::test]
    async fn test_uncertainty_threshold_effects() {
        let analyzer = QuantumAnalyzer::new();
        
        let content = "fn test() {}";
        
        // High uncertainty should reduce probability
        let config_high_uncertainty = EntanglementConfig {
            uncertainty_threshold: 0.5,
            verbose: false,
            output_format: OutputFormat::Text,
        };
        
        let config_low_uncertainty = EntanglementConfig {
            uncertainty_threshold: 0.01,
            verbose: false,
            output_format: OutputFormat::Text,
        };
        
        let result_high = analyzer
            .analyze_content(content, "file1.rs", "file2.rs", config_high_uncertainty)
            .await
            .unwrap();
            
        let result_low = analyzer
            .analyze_content(content, "file1.rs", "file2.rs", config_low_uncertainty)
            .await
            .unwrap();
            
        // Low uncertainty should give higher probability for identical content
        assert!(result_low.entanglement_probability > result_high.entanglement_probability);
    }

    #[tokio::test]
    async fn test_file_reading() {
        let analyzer = QuantumAnalyzer::new();
        
        // Create temporary file
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "fn test() {{ println!(\"hello\"); }}").unwrap();
        
        let path = temp_file.path().to_str().unwrap();
        let content = analyzer.read_file(path).await.unwrap();
        
        assert!(content.contains("fn test()"));
    }

    #[tokio::test]
    async fn test_invalid_uncertainty_threshold() {
        let analyzer = QuantumAnalyzer::new();
        let config = EntanglementConfig {
            uncertainty_threshold: 1.5, // Invalid
            verbose: false,
            output_format: OutputFormat::Text,
        };

        let content = "fn test() {}";
        let result = analyzer
            .analyze_content(content, "file1.rs", "file2.rs", config)
            .await
            .unwrap();

        // Should clamp to valid range
        assert!(result.entanglement_probability >= 0.0 && result.entanglement_probability <= 1.0);
    }

    #[tokio::test]
    async fn test_empty_files() {
        let analyzer = QuantumAnalyzer::new();
        let config = EntanglementConfig {
            uncertainty_threshold: 0.05,
            verbose: false,
            output_format: OutputFormat::Text,
        };

        let result = analyzer
            .analyze_content("", "file1.rs", "file2.rs", config)
            .await
            .unwrap();

        assert!(result.similarity >= 0.0 && result.similarity <= 1.0);
        assert!(result.entanglement_probability >= 0.0 && result.entanglement_probability <= 1.0);
    }

    #[tokio::test]
    async fn test_unicode_content() {
        let analyzer = QuantumAnalyzer::new();
        let config = EntanglementConfig {
            uncertainty_threshold: 0.05,
            verbose: false,
            output_format: OutputFormat::Text,
        };

        let content1 = "fn こんにちは() { println!(\"世界\"); }";
        let content2 = "fn こんにちは() { println!(\"世界\"); }";
        
        let result = analyzer
            .analyze_content(content1, "file1.rs", "file2.rs", config)
            .await
            .unwrap();

        assert_eq!(result.entanglement_state, EntanglementState::Entangled);
    }

    #[tokio::test]
    async fn test_json_output_format() {
        let analyzer = QuantumAnalyzer::new();
        let config = EntanglementConfig {
            uncertainty_threshold: 0.05,
            verbose: true,
            output_format: OutputFormat::Json,
        };

        let content = "fn test() {}";
        let result = analyzer
            .analyze_content(content, "file1.rs", "file2.rs", config)
            .await
            .unwrap();

        // Should contain all detailed fields when verbose
        assert!(!result.file1_hash.is_empty());
        assert!(!result.file2_hash.is_empty());
        assert!(result.quantum_coherence >= 0.0 && result.quantum_coherence <= 1.0);
    }
}
