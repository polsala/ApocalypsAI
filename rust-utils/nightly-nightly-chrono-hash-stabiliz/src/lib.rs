use std::collections::HashMap;

pub fn calculate_stability(hashes: &[String]) -> (String, f64) {
    let mut counts: HashMap<String, u32> = HashMap::new();
    for hash in hashes {
        *counts.entry(hash.clone()).or_insert(0) += 1;
    }

    let mut most_frequent_hash = String::new();
    let mut max_count = 0;

    // Find the most frequent hash. If ties, the first encountered wins.
    // HashMap iteration order is not guaranteed, but for this whimsical tool,
    // picking any of the tied most frequent hashes is acceptable.
    for (hash, count) in counts {
        if count > max_count {
            max_count = count;
            most_frequent_hash = hash;
        }
    }

    let total_observations = hashes.len() as f64;
    let stability_score = if total_observations > 0.0 {
        (max_count as f64 / total_observations) * 100.0
    } else {
        0.0
    };

    (most_frequent_hash, stability_score)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_stability_perfect() {
        // Mock rationale: Testing the core logic of stability calculation with predefined hash lists.
        // This test is deterministic as it uses fixed input data.
        let hashes = vec![
            "hash1".to_string(),
            "hash1".to_string(),
            "hash1".to_string(),
            "hash1".to_string(),
        ];
        let (hash, score) = calculate_stability(&hashes);
        assert_eq!(hash, "hash1");
        assert_eq!(score, 100.0);
    }

    #[test]
    fn test_calculate_stability_some_drift() {
        // Mock rationale: Testing the core logic of stability calculation with predefined hash lists.
        // This test is deterministic as it uses fixed input data.
        let hashes = vec![
            "hash1".to_string(),
            "hash2".to_string(),
            "hash1".to_string(),
            "hash1".to_string(),
        ];
        let (hash, score) = calculate_stability(&hashes);
        assert_eq!(hash, "hash1");
        assert_eq!(score, 75.0); // 3 out of 4 are "hash1"
    }

    #[test]
    fn test_calculate_stability_high_drift() {
        // Mock rationale: Testing the core logic of stability calculation with predefined hash lists.
        // This test is deterministic as it uses fixed input data.
        let hashes = vec![
            "hash1".to_string(),
            "hash2".to_string(),
            "hash3".to_string(),
            "hash1".to_string(),
            "hash2".to_string(),
            "hash1".to_string(),
        ];
        let (hash, score) = calculate_stability(&hashes);
        assert_eq!(hash, "hash1"); // "hash1" appears 3 times, "hash2" 2 times, "hash3" 1 time
        assert_eq!(score, 50.0); // 3 out of 6 are "hash1"
    }

    #[test]
    fn test_calculate_stability_empty() {
        // Mock rationale: Testing edge case with an empty hash list.
        // This test is deterministic as it uses fixed input data.
        let hashes: Vec<String> = vec![];
        let (hash, score) = calculate_stability(&hashes);
        assert_eq!(hash, "");
        assert_eq!(score, 0.0);
    }

    #[test]
    fn test_calculate_stability_single_hash() {
        // Mock rationale: Testing edge case with a single hash.
        // This test is deterministic as it uses fixed input data.
        let hashes = vec!["single_hash".to_string()];
        let (hash, score) = calculate_stability(&hashes);
        assert_eq!(hash, "single_hash");
        assert_eq!(score, 100.0);
    }

    #[test]
    fn test_calculate_stability_tie() {
        // Mock rationale: Testing a tie scenario. The implementation picks the first encountered.
        // This test is deterministic in that it asserts against *any* valid outcome for a tie,
        // acknowledging HashMap's non-guaranteed iteration order for the 'most frequent hash' selection.
        let hashes = vec![
            "hashA".to_string(),
            "hashB".to_string(),
            "hashA".to_string(),
            "hashB".to_string(),
        ];
        let (hash, score) = calculate_stability(&hashes);
        assert!(
            hash == "hashA" || hash == "hashB",
            "Expected hashA or hashB, got {}",
            hash
        );
        assert_eq!(score, 50.0);
    }
}
