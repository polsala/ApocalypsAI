use emoji_mood_mapper::get_emoji;

#[test]
fn test_known_moods() {
    assert_eq!(get_emoji("happy"), ("😊", "Happy"));
    assert_eq!(get_emoji("sad"), ("😢", "Sad"));
    assert_eq!(get_emoji("angry"), ("😠", "Angry"));
}

#[test]
fn test_unknown_mood() {
    // Mock rationale: ensure deterministic fallback for any unlisted mood
    assert_eq!(get_emoji("elated"), ("🤔", "Unknown mood"));
}
