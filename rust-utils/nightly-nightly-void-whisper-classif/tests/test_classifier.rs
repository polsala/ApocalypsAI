// Mock rationale: The classification logic is entirely deterministic and operates on string inputs.
// It does not interact with any external systems, files, or network resources.
// Therefore, no external mocks are required; direct function calls are sufficient for testing.

use nightly_void_whisper_classif::{classify_whisper, Category, Urgency, ClassificationResult};

#[test]
fn test_resource_alert_high_urgency() {
    let whisper = "Danger! Food supplies are critical!";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::ResourceAlert);
    assert_eq!(result.urgency, Urgency::High);
}

#[test]
fn test_temporal_anomaly_medium_urgency() {
    let whisper = "A temporal rift detected, warning of echoes soon.";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::TemporalAnomaly);
    assert_eq!(result.urgency, Urgency::Medium);
}

#[test]
fn test_social_chatter_low_urgency() {
    let whisper = "Hello friend, just a casual message.";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::SocialChatter);
    assert_eq!(result.urgency, Urgency::Low);
}

#[test]
fn test_existential_dread_low_urgency() {
    let whisper = "The void calls, all is meaningless.";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::ExistentialDread);
    assert_eq!(result.urgency, Urgency::Low);
}

#[test]
fn test_unknown_category_low_urgency() {
    let whisper = "Just some random noise in the static.";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::Unknown);
    assert_eq!(result.urgency, Urgency::Low);
}

#[test]
fn test_mixed_keywords_prioritization() {
    // "danger" should make it high urgency, "food" makes it resource alert
    let whisper = "There's a danger in the temporal loop, but also food!";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::ResourceAlert); // Food is matched first in ordered_categories
    assert_eq!(result.urgency, Urgency::High);
}

#[test]
fn test_case_insensitivity() {
    let whisper = "uRgEnT wAtEr sUpPlY nEeDeD!";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::ResourceAlert);
    assert_eq!(result.urgency, Urgency::High);
}

#[test]
fn test_multiple_urgency_keywords_highest_wins() {
    let whisper = "Alert! Watch out, but no immediate danger.";
    let result = classify_whisper(whisper);
    assert_eq!(result.urgency, Urgency::Medium); // "Alert" and "watch" are medium, "immediate danger" is not present
}

#[test]
fn test_danger_implies_resource_alert_if_no_other_category() {
    let whisper = "Danger ahead!";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::ResourceAlert);
    assert_eq!(result.urgency, Urgency::High);
}

#[test]
fn test_temporal_and_high_urgency() {
    let whisper = "Critical temporal distortion detected NOW!";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::TemporalAnomaly);
    assert_eq!(result.urgency, Urgency::High);
}

#[test]
fn test_social_and_medium_urgency() {
    let whisper = "Warning: unknown signal detected, possible contact soon.";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::SocialChatter);
    assert_eq!(result.urgency, Urgency::Medium);
}

#[test]
fn test_only_urgency_keyword() {
    let whisper = "Urgent!";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::Unknown); // No category keyword
    assert_eq!(result.urgency, Urgency::High);
}

#[test]
fn test_only_category_keyword() {
    let whisper = "Found some water.";
    let result = classify_whisper(whisper);
    assert_eq!(result.category, Category::ResourceAlert);
    assert_eq!(result.urgency, Urgency::Low); // No urgency keyword
}
