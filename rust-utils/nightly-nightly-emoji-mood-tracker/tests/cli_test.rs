use std::env;
use std::path::PathBuf;

#[test]
fn test_data_path_resolves_to_home() {
    // Mock rationale: Ensure the utility respects the HOME environment variable.
    let temp_home = tempfile::tempdir().unwrap();
    env::set_var("HOME", temp_home.path());
    let path = nightly_emoji_mood_tracker::get_data_path();
    let mut expected = PathBuf::from(temp_home.path());
    expected.push(".emoji_mood_tracker.json");
    assert_eq!(path, expected);
}
