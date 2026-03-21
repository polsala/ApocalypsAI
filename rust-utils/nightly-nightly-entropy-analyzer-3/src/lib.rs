pub fn compute_entropy(s: &str) -> f64 {
    let len = s.len() as f64;
    if len == 0.0 {
        return 0.0;
    }
    let mut freq = std::collections::HashMap::new();
    for ch in s.chars() {
        *freq.entry(ch).or_insert(0usize) += 1;
    }
    let mut entropy = 0.0;
    for (_ch, count) in freq {
        let p = (count as f64) / len;
        entropy -= p * p.log2();
    }
    entropy
}
