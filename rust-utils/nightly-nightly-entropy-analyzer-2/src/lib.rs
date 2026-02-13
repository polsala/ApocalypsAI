use std::collections::HashMap;

/// Compute the Shannon entropy of `input` in bits.
/// Returns 0.0 for an empty string.
pub fn compute_entropy(input: &str) -> f64 {
    let len = input.len() as f64;
    if len == 0.0 {
        return 0.0;
    }
    let mut freq: HashMap<u8, usize> = HashMap::new();
    for b in input.bytes() {
        *freq.entry(b).or_insert(0) += 1;
    }
    let mut entropy = 0.0;
    for &count in freq.values() {
        let p = count as f64 / len;
        entropy -= p * p.log2();
    }
    entropy
}
