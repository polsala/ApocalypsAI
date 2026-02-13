use std::collections::HashMap;

/// Returns a tuple of (emoji, description) for a given mood.
///
/// If the mood is not recognized, returns the default "🤔" with "Unknown mood".
pub fn get_emoji(mood: &str) -> (&'static str, &'static str) {
    let map: HashMap<&str, (&str, &str)> = [
        ("happy", ("😊", "Happy")),
        ("sad", ("😢", "Sad")),
        ("angry", ("😠", "Angry")),
        ("excited", ("🤩", "Excited")),
        ("tired", ("😴", "Tired")),
        ("confused", ("🤔", "Confused")),
    ]
    .iter()
    .cloned()
    .collect();

    map.get(mood).cloned().unwrap_or(("🤔", "Unknown mood"))
}
