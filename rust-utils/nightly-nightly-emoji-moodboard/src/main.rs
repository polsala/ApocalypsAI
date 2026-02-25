use rand::seq::SliceRandom;
use rand::thread_rng;
use std::env;

/// Returns a slice of emojis that correspond to the given mood.
fn emojis_for_mood(mood: &str) -> &'static [&'static str] {
    match mood.to_lowercase().as_str() {
        "happy" | "joy" | "glad" => &["😄", "😊", "😁", "🥳"],
        "sad" | "down" | "blue" => &["😢", "☹️", "😞", "💧"],
        "angry" | "mad" => &["😡", "🤬", "👿"],
        "love" | "heart" => &["❤️", "💖", "😍", "🥰"],
        "relaxed" | "calm" => &["🧘‍♂️", "🌿", "☕", "😌"],
        "energetic" | "excited" => &["⚡", "🚀", "🤩", "💥"],
        "productive" | "focused" => &["💼", "📈", "🗂️", "🧠"],
        "party" | "celebrate" => &["🎉", "🥳", "🍾", "🪅"],
        "food" | "hungry" => &["🍕", "🍔", "🍣", "🍰"],
        "nature" | "outdoors" => &["🌲", "🏞️", "🌊", "🌻"],
        _ => &["❓", "🤔", "🧐"],
    }
}

/// Picks a random emoji from the slice for a given mood.
fn pick_emoji(mood: &str) -> &'static str {
    let options = emojis_for_mood(mood);
    let mut rng = thread_rng();
    options.choose(&mut rng).unwrap_or(&"❓")
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    let mut rng = thread_rng();

    let emojis: Vec<&str> = if args.is_empty() {
        // No moods supplied – generate three random emojis from a mixed pool.
        let all_emojis: Vec<&str> = [
            "😄", "😊", "😁", "🥳", "😢", "☹️", "😞", "💧",
            "😡", "🤬", "👿", "❤️", "💖", "😍", "🥰",
            "🧘‍♂️", "🌿", "☕", "😌", "⚡", "🚀", "🤩", "💥",
            "💼", "📈", "🗂️", "🧠", "🎉", "🥳", "🍾", "🪅",
            "🍕", "🍔", "🍣", "🍰", "🌲", "🏞️", "🌊", "🌻",
        ]
        .to_vec();
        (0..3)
            .map(|_| *all_emojis.choose(&mut rng).unwrap())
            .collect()
    } else {
        // Generate an emoji per supplied mood.
        args.iter().map(|m| pick_emoji(m)).collect()
    };

    println!("{}", emojis.join(" "));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_emojis_for_known_mood() {
        let happy = emojis_for_mood("happy");
        assert!(happy.contains(&"😄"));
        assert!(happy.contains(&"😊"));
    }

    #[test]
    fn test_emojis_for_unknown_mood() {
        let unknown = emojis_for_mood("quantum");
        assert_eq!(unknown, &["❓", "🤔", "🧐"]);
    }

    #[test]
    fn test_pick_emoji_returns_valid_option() {
        let emoji = pick_emoji("sad");
        let options = emojis_for_mood("sad");
        assert!(options.contains(&emoji));
    }
}
