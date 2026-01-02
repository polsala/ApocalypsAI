#[cfg(test)]
mod tests {
    use super::super::compute_entropy;

    fn approx_eq(a: f64, b: f64, eps: f64) -> bool {
        (a - b).abs() < eps
    }

    #[test]
    fn test_entropy_all_same() {
        let data = b"aaaaaaaaaa"; // all identical bytes
        let ent = compute_entropy(data);
        assert!(approx_eq(ent, 0.0, 1e-9), "entropy should be 0 for uniform data");
    }

    #[test]
    fn test_entropy_uniform_five_symbols() {
        let data = b"abcde"; // each symbol appears once
        let ent = compute_entropy(data);
        // Expected entropy = log2(5) ≈ 2.321928094887362
        let expected = 5f64.log2();
        assert!(approx_eq(ent, expected, 1e-9), "entropy mismatch");
    }

    #[test]
    fn test_entropy_known_pattern() {
        // 4 bytes: 0x00, 0xFF, 0x00, 0xFF -> two symbols each 50%
        let data = [0x00u8, 0xFF, 0x00, 0xFF];
        let ent = compute_entropy(&data);
        // Expected entropy = -2 * 0.5 * log2(0.5) = 1.0
        assert!(approx_eq(ent, 1.0, 1e-9), "entropy should be 1.0 for two‑symbol 50/50 data");
    }
}
