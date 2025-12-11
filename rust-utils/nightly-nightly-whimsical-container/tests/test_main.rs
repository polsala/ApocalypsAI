use super::*;

#[test]
fn test_fantasy_playful() {
    let names = generate_names("fantasy", "playful", 3);
    assert!(names.contains(&"enchanted-forest-inator".to_string()));
    assert!(names.contains(&"mystic-dragon-bot".to_string()));
    assert!(names.contains(&"ancient-artifact-pal".to_string()));
}

#[test]
fn test_cyberpunk_serious() {
    let names = generate_names("cyberpunk", "serious", 2);
    assert!(names.contains(&"neon-matrix-core".to_string()));
    assert!(names.contains(&"quantum-interface-engine".to_string()));
}

#[test]
fn test_pirate_absurd() {
    let names = generate_names("pirate", "absurd", 1);
    assert!(names.contains(&"cursed-ship-blorp".to_string()));
}

// Mock rationale: Using fixed test data to ensure deterministic outcomes
// while verifying the name generation logic works as expected
