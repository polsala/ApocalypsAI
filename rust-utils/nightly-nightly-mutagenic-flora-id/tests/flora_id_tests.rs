use nightly_mutagenic_flora_id::{find_flora, FloraArgs, FLORA_DB};

// Mock rationale: The FLORA_DB is a static, internal data structure.
// All tests operate directly on this data and the matching logic,
// making them deterministic and offline without external mocks.

#[test]
fn test_identify_gloom_bloom_exact() {
    let args = FloraArgs {
        color: Some("dark-purple".to_string()),
        shape: Some("bell".to_string()),
        glow: Some(true),
        sound: Some("faint-hum".to_string()),
    };
    let identified = find_flora(&args);
    assert_eq!(identified.len(), 1);
    assert_eq!(identified[0].name, "Gloom Bloom");
}

#[test]
fn test_identify_shimmer_shroom_no_sound_query() {
    let args = FloraArgs {
        color: Some("iridescent".to_string()),
        shape: Some("umbrella".to_string()),
        glow: Some(true),
        sound: None,
    };
    let identified = find_flora(&args);
    assert_eq!(identified.len(), 1);
    assert_eq!(identified[0].name, "Shimmer Shroom");
}

#[test]
fn test_identify_shimmer_shroom_with_sound_query_no_match() {
    let args = FloraArgs {
        color: Some("iridescent".to_string()),
        shape: Some("umbrella".to_string()),
        glow: Some(true),
        sound: Some("some-sound".to_string()), // Shimmer Shroom has no sound
    };
    let identified = find_flora(&args);
    assert!(identified.is_empty());
}

#[test]
fn test_identify_multiple_glowing_flora() {
    let args = FloraArgs {
        color: None,
        shape: None,
        glow: Some(true),
        sound: None,
    };
    let identified = find_flora(&args);
    // Gloom Bloom, Shimmer Shroom, Crimson Spore, Void Blossom, Glimmer Grass
    assert_eq!(identified.len(), 5);
    let names: Vec<&str> = identified.iter().map(|f| f.name).collect();
    assert!(names.contains(&"Gloom Bloom"));
    assert!(names.contains(&"Shimmer Shroom"));
    assert!(names.contains(&"Crimson Spore"));
    assert!(names.contains(&"Void Blossom"));
    assert!(names.contains(&"Glimmer Grass"));
}

#[test]
fn test_no_match_unknown_characteristics() {
    let args = FloraArgs {
        color: Some("blue".to_string()),
        shape: Some("square".to_string()),
        glow: Some(false),
        sound: None,
    };
    let identified = find_flora(&args);
    assert!(identified.is_empty());
}

#[test]
fn test_identify_by_sound_only() {
    let args = FloraArgs {
        color: None,
        shape: None,
        glow: None,
        sound: Some("soft-rustle".to_string()),
    };
    let identified = find_flora(&args);
    assert_eq!(identified.len(), 1);
    assert_eq!(identified[0].name, "Whisper Weed");
}

#[test]
fn test_identify_by_color_and_glow() {
    let args = FloraArgs {
        color: Some("crimson".to_string()),
        shape: None,
        glow: Some(true),
        sound: None,
    };
    let identified = find_flora(&args);
    assert_eq!(identified.len(), 1);
    assert_eq!(identified[0].name, "Crimson Spore");
}

#[test]
fn test_empty_args_returns_all() {
    let args = FloraArgs {
        color: None,
        shape: None,
        glow: None,
        sound: None,
    };
    let identified = find_flora(&args);
    assert_eq!(identified.len(), FLORA_DB.len());
}

#[test]
fn test_identify_void_blossom_exact() {
    let args = FloraArgs {
        color: Some("black".to_string()),
        shape: Some("spiral".to_string()),
        glow: Some(true),
        sound: Some("deep-resonance".to_string()),
    };
    let identified = find_flora(&args);
    assert_eq!(identified.len(), 1);
    assert_eq!(identified[0].name, "Void Blossom");
}

#[test]
fn test_identify_glimmer_grass_no_sound_query() {
    let args = FloraArgs {
        color: Some("emerald-green".to_string()),
        shape: Some("blade".to_string()),
        glow: Some(true),
        sound: None,
    };
    let identified = find_flora(&args);
    assert_eq!(identified.len(), 1);
    assert_eq!(identified[0].name, "Glimmer Grass");
}
