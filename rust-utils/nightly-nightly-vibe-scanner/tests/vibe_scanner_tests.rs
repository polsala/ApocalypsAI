#![cfg(test)]

use crate::{scan_vibe, Vibe};

// Mock rationale: The `scan_vibe` function is a pure function that takes a string and returns a Vibe and a list of keywords. It does not interact with the file system, network, or any other external state. Therefore, direct unit testing of the function with various string inputs is sufficient and inherently deterministic and offline.

#[test]
fn test_hopeful_vibe() {
    let text = "We must build a new future with hope and resilience.";
    let (vibe, keywords) = scan_vibe(text);
    assert_eq!(vibe, Vibe::Hopeful);
    assert!(keywords.contains(&"build".to_string()));
    assert!(keywords.contains(&"future".to_string()));
    assert!(keywords.contains(&"hope".to_string()));
    assert!(keywords.contains(&"resilience".to_string()));
}

#[test]
fn test_despairing_vibe() {
    let text = "All is lost, there is no escape from the darkness and despair.";
    let (vibe, keywords) = scan_vibe(text);
    assert_eq!(vibe, Vibe::Despairing);
    assert!(keywords.contains(&"lost".to_string()));
    assert!(keywords.contains(&"no escape".to_string()));
    assert!(keywords.contains(&"darkness".to_string()));
    assert!(keywords.contains(&"despair".to_string()));
}

#[test]
fn test_chaotic_vibe() {
    let text = "The city is in chaos, shattered by unrest and constant fighting.";
    let (vibe, keywords) = scan_vibe(text);
    assert_eq!(vibe, Vibe::Chaotic);
    assert!(keywords.contains(&"chaos".to_string()));
    assert!(keywords.contains(&"shattered".to_string()));
    assert!(keywords.contains(&"unrest".to_string()));
    assert!(keywords.contains(&"fighting".to_string()));
}

#[test]
fn test_resourceful_vibe() {
    let text = "We need to scavenge for parts and improvise a solution. Ingenuity is key.";
    let (vibe, keywords) = scan_vibe(text);
    assert_eq!(vibe, Vibe::Resourceful);
    assert!(keywords.contains(&"scavenge".to_string()));
    assert!(keywords.contains(&"improvise".to_string()));
    assert!(keywords.contains(&"solution".to_string()));
    assert!(keywords.contains(&"ingenuity".to_string()));
}

#[test]
fn test_neutral_vibe() {
    let text = "The quick brown fox jumps over the lazy dog.";
    let (vibe, keywords) = scan_vibe(text);
    assert_eq!(vibe, Vibe::Neutral);
    assert!(keywords.is_empty());
}

#[test]
fn test_mixed_dominant_hopeful() {
    let text = "Despite the chaos, we still have hope to rebuild.";
    let (vibe, keywords) = scan_vibe(text);
    assert_eq!(vibe, Vibe::Hopeful);
    assert!(keywords.contains(&"chaos".to_string()));
    assert!(keywords.contains(&"hope".to_string()));
    assert!(keywords.contains(&"rebuild".to_string()));
}

#[test]
fn test_mixed_dominant_despairing() {
    let text = "There is no escape from the darkness, even if we try to build.";
    let (vibe, keywords) = scan_vibe(text);
    assert_eq!(vibe, Vibe::Despairing);
    assert!(keywords.contains(&"no escape".to_string()));
    assert!(keywords.contains(&"darkness".to_string()));
    assert!(keywords.contains(&"build".to_string()));
}

#[test]
fn test_empty_string() {
    let text = "";
    let (vibe, keywords) = scan_vibe(text);
    assert_eq!(vibe, Vibe::Neutral);
    assert!(keywords.is_empty());
}

#[test]
fn test_case_insensitivity() {
    let text = "HoPe for the fUtUrE";
    let (vibe, keywords) = scan_vibe(text);
    assert_eq!(vibe, Vibe::Hopeful);
    assert!(keywords.contains(&"hope".to_string()));
    assert!(keywords.contains(&"future".to_string()));
}

#[test]
fn test_tie_breaking_hopeful_resourceful() {
    let text = "We need to scavenge and find hope for the future.";
    let (vibe, keywords) = scan_vibe(text);
    // Hopeful should win over Resourceful in a tie based on arbitrary priority
    assert_eq!(vibe, Vibe::Hopeful);
    assert!(keywords.contains(&"scavenge".to_string()));
    assert!(keywords.contains(&"find".to_string()));
    assert!(keywords.contains(&"hope".to_string()));
    assert!(keywords.contains(&"future".to_string()));
}

#[test]
fn test_tie_breaking_resourceful_chaotic() {
    let text = "Chaos reigns, but we will scavenge for a solution.";
    let (vibe, keywords) = scan_vibe(text);
    // Resourceful should win over Chaotic in a tie
    assert_eq!(vibe, Vibe::Resourceful);
    assert!(keywords.contains(&"chaos".to_string()));
    assert!(keywords.contains(&"scavenge".to_string()));
    assert!(keywords.contains(&"solution".to_string()));
}

#[test]
fn test_multiple_keywords_same_vibe() {
    let text = "Hope, future, build, survive, rebuild.";
    let (vibe, keywords) = scan_vibe(text);
    assert_eq!(vibe, Vibe::Hopeful);
    assert_eq!(keywords.len(), 5); // Ensure all unique keywords are counted
}
