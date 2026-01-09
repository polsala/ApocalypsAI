use void_whisper_decoder::decode_message;

#[test]
fn test_noise_removal() {
    // Mock rationale: Testing the core logic of noise removal, no external dependencies.
    let input = "[STATIC] Message /// from _VOID_ the past --- ... ~";
    let expected = "Message from the past";
    assert_eq!(decode_message(input, false, false, false), expected);
}

#[test]
fn test_interpretation() {
    // Mock rationale: Testing the character substitution logic, no external dependencies.
    let input = "XQZJ KWWV"; // Should become "EAS I CCVV" -> "EAS I CCUU" (V->U)
    let expected = "EAS I CCUU";
    assert_eq!(decode_message(input, true, false, false), expected);
}

#[test]
fn test_keyword_highlighting() {
    // Mock rationale: Testing the keyword highlighting logic, no external dependencies.
    let input = "Find water and food. DANGER ahead.";
    let expected = "Find [!water] and [!food]. [!DANGER] ahead.";
    assert_eq!(decode_message(input, false, true, false), expected);

    let input_case_insensitive = "find WATER and food. danger ahead.";
    let expected_case_insensitive = "find [!WATER] and [!food]. [!danger] ahead.";
    assert_eq!(decode_message(input_case_insensitive, false, true, false), expected_case_insensitive);
}

#[test]
fn test_all_features_combined() {
    // Mock rationale: Testing the combined effect of all features, no external dependencies.
    let input = "[STATIC] XQZJ KWWV. Find WATER and food. DANGER ahead. ///";
    let expected = "EAS I CCUU. Find [!WATER] and [!food]. [!DANGER] ahead.";
    assert_eq!(decode_message(input, true, true, false), expected);
}

#[test]
fn test_empty_input() {
    // Mock rationale: Testing behavior with empty input, no external dependencies.
    let input = "";
    let expected = "";
    assert_eq!(decode_message(input, false, false, false), expected);
}

#[test]
fn test_no_changes_needed() {
    // Mock rationale: Testing input that should remain unchanged, no external dependencies.
    let input = "Hello world.";
    let expected = "Hello world.";
    assert_eq!(decode_message(input, false, false, false), expected);
}

#[test]
fn test_frequency_analysis() {
    // Mock rationale: Testing frequency analysis calculation, no external dependencies.
    let input = "Banana Apple Orange";
    let result = decode_message(input, false, false, true);
    assert!(result.starts_with("Banana Apple Orange"));
    assert!(result.contains("--- Frequency Analysis ---"));
    assert!(result.contains("A: 4"));
    assert!(result.contains("N: 2"));
    assert!(result.contains("B: 1"));
    assert!(result.contains("P: 1"));
    assert!(result.contains("L: 1"));
    assert!(result.contains("O: 1"));
    assert!(result.contains("R: 1"));
    assert!(result.contains("G: 1"));
    assert!(result.contains("E: 1"));
}

#[test]
fn test_frequency_analysis_with_interpretation() {
    // Mock rationale: Testing frequency analysis after interpretation, no external dependencies.
    let input = "XQZJ KWWV"; // Interpreted: EAS I CCUU
    let result = decode_message(input, true, false, true);
    assert!(result.starts_with("EAS I CCUU"));
    assert!(result.contains("--- Frequency Analysis ---"));
    assert!(result.contains("U: 2"));
    assert!(result.contains("C: 2"));
    assert!(result.contains("A: 1"));
    assert!(result.contains("S: 1"));
    assert!(result.contains("I: 1"));
    assert!(result.contains("E: 1"));
}
