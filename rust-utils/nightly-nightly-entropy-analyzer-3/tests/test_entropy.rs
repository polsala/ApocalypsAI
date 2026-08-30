use nightly_entropy_analyzer::compute_entropy;

#[test]
fn test_entropy_known() {
    // "aaab" -> a:3/4, b:1/4 => entropy ≈ 0.8112781244591328 bits per character
    let s = "aaab";
    let entropy = compute_entropy(s);
    let expected = 0.8112781244591328_f64;
    assert!((entropy - expected).abs() < 1e-12);
}

#[test]
fn test_entropy_empty() {
    assert_eq!(compute_entropy(""), 0.0);
}

#[test]
fn test_entropy_single_char() {
    assert_eq!(compute_entropy("aaaaa"), 0.0);
}
