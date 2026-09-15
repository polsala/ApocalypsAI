use super::*;

// Mock rationale: These tests are unit tests for the Quibble struct and its methods.
// They do not interact with the file system or command line arguments directly.
// Instead, they use hardcoded strings and values to simulate input and test logic.

#[test]
fn test_quibble_from_str_valid() {
    let s = "Fix typo in README | 2 | 1 | 3";
    let quibble = Quibble::from_str(s).unwrap();
    assert_eq!(quibble.description, "Fix typo in README");
    assert_eq!(quibble.urgency, 2);
    assert_eq!(quibble.complexity, 1);
    assert_eq!(quibble.impact, 3);
    // Score is calculated with default weights during FromStr, but re-calculated in main
    // For this test, we just check the parsed values.
}

#[test]
fn test_quibble_from_str_invalid_format() {
    let s = "Fix typo in README | 2 | 1"; // Missing impact
    let err = Quibble::from_str(s).unwrap_err();
    assert!(err.contains("Invalid quibble format"));

    let s = "Fix typo in README"; // Too few parts
    let err = Quibble::from_str(s).unwrap_err();
    assert!(err.contains("Invalid quibble format"));

    let s = "Fix typo in README | 2 | 1 | 3 | extra"; // Too many parts
    let err = Quibble::from_str(s).unwrap_err();
    assert!(err.contains("Invalid quibble format"));
}

#[test]
fn test_quibble_from_str_invalid_numbers() {
    let s = "Fix typo in README | A | 1 | 3"; // Invalid urgency
    let err = Quibble::from_str(s).unwrap_err();
    assert!(err.contains("Invalid urgency value"));

    let s = "Fix typo in README | 2 | B | 3"; // Invalid complexity
    let err = Quibble::from_str(s).unwrap_err();
    assert!(err.contains("Invalid complexity value"));

    let s = "Fix typo in README | 2 | 1 | C"; // Invalid impact
    let err = Quibble::from_str(s).unwrap_err();
    assert!(err.contains("Invalid impact value"));

    let s = "Fix typo in README | 256 | 1 | 3"; // Out of range u8
    let err = Quibble::from_str(s).unwrap_err();
    assert!(err.contains("Invalid urgency value"));
}

#[test]
fn test_quibble_score_calculation() {
    let weights = Weights { urgency: 2, complexity: 1, impact: 3 };
    let quibble = Quibble::new(
        "Test Quibble".to_string(),
        5, // urgency
        3, // complexity
        7, // impact
        &weights,
    );
    // Expected score: (5 * 2) + (3 * 1) + (7 * 3) = 10 + 3 + 21 = 34
    assert_eq!(quibble.score, 34);

    let weights_default = Weights { urgency: 1, complexity: 1, impact: 1 };
    let quibble_default = Quibble::new(
        "Another Quibble".to_string(),
        10, // urgency
        1,  // complexity
        1,  // impact
        &weights_default,
    );
    // Expected score: (10 * 1) + (1 * 1) + (1 * 1) = 10 + 1 + 1 = 12
    assert_eq!(quibble_default.score, 12);
}

#[test]
fn test_quibble_sorting() {
    let weights = Weights { urgency: 1, complexity: 1, impact: 1 };
    let q1 = Quibble::new("Low priority".to_string(), 1, 1, 1, &weights); // Score 3
    let q2 = Quibble::new("Medium priority".to_string(), 5, 5, 5, &weights); // Score 15
    let q3 = Quibble::new("High priority".to_string(), 10, 8, 9, &weights); // Score 27

    let mut quibbles = vec![q1.clone(), q3.clone(), q2.clone()];
    quibbles.sort_by(|a, b| b.score.cmp(&a.score)); // Sort descending

    assert_eq!(quibbles[0].description, "High priority");
    assert_eq!(quibbles[1].description, "Medium priority");
    assert_eq!(quibbles[2].description, "Low priority");

    // Test with same score, should maintain original relative order (stable sort not strictly guaranteed by cmp, but often is)
    let q4 = Quibble::new("Same score A".to_string(), 2, 1, 0, &weights); // Score 3
    let q5 = Quibble::new("Same score B".to_string(), 1, 1, 1, &weights); // Score 3
    let mut quibbles_same_score = vec![q4.clone(), q5.clone()];
    quibbles_same_score.sort_by(|a, b| b.score.cmp(&a.score));
    // The order of q4 and q5 might vary depending on Rust's sort implementation for equal elements.
    // We can only assert that both are present and have the correct score.
    assert_eq!(quibbles_same_score[0].score, 3);
    assert_eq!(quibbles_same_score[1].score, 3);
}
