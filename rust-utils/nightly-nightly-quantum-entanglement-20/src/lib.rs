use std::collections::{HashMap, HashSet};
use std::hash::{Hash, Hasher};
use std::fs;
use std::path::Path;
use serde::{Serialize, Deserialize};
use md5;

#[derive(Debug, Serialize, Deserialize)]
pub struct QuantumState {
    pub amplitude: f64,
    pub phase: f64,
    pub probability: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct EntanglementResult {
    pub file1: String,
    pub file2: String,
    pub entanglement_score: f64,
    pub quantum_state: QuantumState,
    pub correlation_details: CorrelationDetails,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct CorrelationDetails {
    pub content_similarity: f64,
    pub metadata_correlation: f64,
    pub pattern_matching: f64,
    pub quantum_interference: f64,
}

pub struct QuantumEntanglementChecker {
    quantum_threshold: f64,
}

impl QuantumEntanglementChecker {
    pub fn new(threshold: f64) -> Self {
        QuantumEntanglementChecker {
            quantum_threshold: threshold,
        }
    }

    pub fn check_entanglement(&self, file1_path: &str, file2_path: &str) -> Option<EntanglementResult> {
        let content1 = match fs::read_to_string(file1_path) {
            Ok(content) => content,
            Err(_) => return None,
        };
        
        let content2 = match fs::read_to_string(file2_path) {
            Ok(content) => content,
            Err(_) => return None,
        };

        let content_similarity = self.calculate_content_similarity(&content1, &content2);
        let metadata_correlation = self.calculate_metadata_correlation(file1_path, file2_path);
        let pattern_matching = self.calculate_pattern_matching(&content1, &content2);
        let quantum_interference = self.calculate_quantum_interference(&content1, &content2);

        let entanglement_score = self.calculate_entanglement_score(
            content_similarity,
            metadata_correlation,
            pattern_matching,
            quantum_interference,
        );

        let quantum_state = self.generate_quantum_state(entanglement_score);

        Some(EntanglementResult {
            file1: file1_path.to_string(),
            file2: file2_path.to_string(),
            entanglement_score,
            quantum_state,
            correlation_details: CorrelationDetails {
                content_similarity,
                metadata_correlation,
                pattern_matching,
                quantum_interference,
            },
        })
    }

    pub fn find_entangled_files(&self, dir_path: &str, threshold: Option<f64>) -> Vec<EntanglementResult> {
        let threshold = threshold.unwrap_or(self.quantum_threshold);
        let mut results = Vec::new();
        
        let files: Vec<String> = match fs::read_dir(dir_path) {
            Ok(entries) => entries
                .filter_map(|entry| {
                    let path = entry.ok()?.path();
                    if path.is_file() {
                        path.to_str().map(|s| s.to_string())
                    } else {
                        None
                    }
                })
                .collect(),
            Err(_) => return results,
        };

        for i in 0..files.len() {
            for j in (i + 1)..files.len() {
                if let Some(result) = self.check_entanglement(&files[i], &files[j]) {
                    if result.entanglement_score >= threshold {
                        results.push(result);
                    }
                }
            }
        }

        results.sort_by(|a, b| b.entanglement_score.partial_cmp(&a.entanglement_score).unwrap());
        results
    }

    fn calculate_content_similarity(&self, content1: &str, content2: &str) -> f64 {
        let words1: HashSet<&str> = content1.split_whitespace().collect();
        let words2: HashSet<&str> = content2.split_whitespace().collect();
        
        let intersection = words1.intersection(&words2).count();
        let union = words1.union(&words2).count();
        
        if union == 0 {
            0.0
        } else {
            intersection as f64 / union as f64
        }
    }

    fn calculate_metadata_correlation(&self, file1_path: &str, file2_path: &str) -> f64 {
        let meta1 = fs::metadata(file1_path).ok()?;
        let meta2 = fs::metadata(file2_path).ok()?;
        
        let size1 = meta1.len();
        let size2 = meta2.len();
        
        let size_diff = (size1 as i64 - size2 as i64).abs() as f64;
        let max_size = size1.max(size2) as f64;
        
        if max_size == 0.0 {
            1.0
        } else {
            1.0 - (size_diff / max_size)
        }
    }

    fn calculate_pattern_matching(&self, content1: &str, content2: &str) -> f64 {
        let hash1 = format!("{:?}", md5::compute(content1.as_bytes()));
        let hash2 = format!("{:?}", md5::compute(content2.as_bytes()));
        
        let chars1: HashSet<char> = hash1.chars().collect();
        let chars2: HashSet<char> = hash2.chars().collect();
        
        let common_chars = chars1.intersection(&chars2).count();
        let total_chars = chars1.union(&chars2).count();
        
        if total_chars == 0 {
            0.0
        } else {
            common_chars as f64 / total_chars as f64
        }
    }

    fn calculate_quantum_interference(&self, content1: &str, content2: &str) -> f64 {
        let len1 = content1.len();
        let len2 = content2.len();
        
        let len_diff = (len1 as i64 - len2 as i64).abs() as f64;
        let max_len = len1.max(len2) as f64;
        
        if max_len == 0.0 {
            1.0
        } else {
            1.0 - (len_diff / max_len)
        }
    }

    fn calculate_entanglement_score(
        &self,
        content_similarity: f64,
        metadata_correlation: f64,
        pattern_matching: f64,
        quantum_interference: f64,
    ) -> f64 {
        // Quantum-inspired weighted average
        let weights = [0.4, 0.3, 0.2, 0.1];
        let values = [content_similarity, metadata_correlation, pattern_matching, quantum_interference];
        
        let mut score = 0.0;
        for (i, value) in values.iter().enumerate() {
            score += value * weights[i];
        }
        
        // Apply quantum superposition effect
        score * (1.0 + (content_similarity * metadata_correlation * 0.1))
    }

    fn generate_quantum_state(&self, entanglement_score: f64) -> QuantumState {
        let amplitude = entanglement_score.sqrt();
        let phase = (entanglement_score * std::f64::consts::PI) % (2.0 * std::f64::consts::PI);
        let probability = amplitude.powi(2);
        
        QuantumState {
            amplitude,
            phase,
            probability,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::NamedTempFile;

    #[test]
    fn test_quantum_entanglement_checker_creation() {
        let checker = QuantumEntanglementChecker::new(0.5);
        assert_eq!(checker.quantum_threshold, 0.5);
    }

    #[test]
    fn test_content_similarity_identical() {
        let checker = QuantumEntanglementChecker::new(0.5);
        let result = checker.calculate_content_similarity("hello world", "hello world");
        assert_eq!(result, 1.0);
    }

    #[test]
    fn test_content_similarity_no_overlap() {
        let checker = QuantumEntanglementChecker::new(0.5);
        let result = checker.calculate_content_similarity("hello", "world");
        assert_eq!(result, 0.0);
    }

    #[test]
    fn test_content_similarity_partial_overlap() {
        let checker = QuantumEntanglementChecker::new(0.5);
        let result = checker.calculate_content_similarity("hello world", "hello rust");
        assert_eq!(result, 0.5); // "hello" matches, "world" and "rust" don't
    }

    #[test]
    fn test_check_entanglement_with_temp_files() {
        // Create temporary files for testing
        let temp_file1 = NamedTempFile::new().unwrap();
        let temp_file2 = NamedTempFile::new().unwrap();
        
        let file1_path = temp_file1.path().to_str().unwrap();
        let file2_path = temp_file2.path().to_str().unwrap();
        
        fs::write(file1_path, "hello world content").unwrap();
        fs::write(file2_path, "hello rust content").unwrap();
        
        let checker = QuantumEntanglementChecker::new(0.1);
        let result = checker.check_entanglement(file1_path, file2_path);
        
        assert!(result.is_some());
        let result = result.unwrap();
        assert_eq!(result.file1, file1_path);
        assert_eq!(result.file2, file2_path);
        assert!(result.entanglement_score >= 0.0 && result.entanglement_score <= 1.0);
        assert!(result.quantum_state.probability >= 0.0 && result.quantum_state.probability <= 1.0);
    }

    #[test]
    fn test_check_entanglement_with_nonexistent_file() {
        let checker = QuantumEntanglementChecker::new(0.5);
        let result = checker.check_entanglement("nonexistent1.txt", "nonexistent2.txt");
        assert!(result.is_none());
    }

    #[test]
    fn test_generate_quantum_state() {
        let checker = QuantumEntanglementChecker::new(0.5);
        let quantum_state = checker.generate_quantum_state(0.25);
        
        assert!((quantum_state.amplitude - 0.5).abs() < 0.001);
        assert!(quantum_state.probability >= 0.0 && quantum_state.probability <= 1.0);
    }

    #[test]
    fn test_calculate_entanglement_score() {
        let checker = QuantumEntanglementChecker::new(0.5);
        let score = checker.calculate_entanglement_score(1.0, 1.0, 1.0, 1.0);
        assert!(score >= 1.0 && score <= 1.1); // Should be around 1.0 with quantum effect
    }
}
