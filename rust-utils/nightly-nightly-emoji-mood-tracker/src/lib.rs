use serde::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;
use std::io::{self, Write};

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
pub struct MoodEntry {
    pub date: String,
    pub emoji: String,
    pub note: Option<String>,
}

pub fn get_data_path() -> PathBuf {
    let mut path = dirs::home_dir().expect("Could not find home directory");
    path.push(".emoji_mood_tracker.json");
    path
}

pub fn load_entries() -> io::Result<Vec<MoodEntry>> {
    let path = get_data_path();
    if !path.exists() {
        return Ok(vec![]);
    }
    let data = fs::read_to_string(path)?;
    let entries: Vec<MoodEntry> = serde_json::from_str(&data)?;
    Ok(entries)
}

pub fn save_entries(entries: &[MoodEntry]) -> io::Result<()> {
    let path = get_data_path();
    let data = serde_json::to_string_pretty(entries)?;
    let mut file = fs::File::create(path)?;
    file.write_all(data.as_bytes())?;
    Ok(())
}

pub fn add_entry(emoji: &str, note: Option<&str>) -> io::Result<()> {
    let mut entries = load_entries()?;
    let date = chrono::Local::now().format("%Y-%m-%d").to_string();
    let entry = MoodEntry {
        date,
        emoji: emoji.to_string(),
        note: note.map(|s| s.to_string()),
    };
    entries.push(entry);
    save_entries(&entries)
}

pub fn stats() -> io::Result<std::collections::HashMap<String, usize>> {
    let entries = load_entries()?;
    let mut map = std::collections::HashMap::new();
    for e in entries {
        *map.entry(e.emoji).or_insert(0) += 1;
    }
    Ok(map)
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::NamedTempFile;
    use std::fs;
    use std::path::PathBuf;

    // Mock rationale: Use a temporary directory and override HOME to keep tests deterministic.
    fn with_temp_home<F: FnOnce()>(test: F) {
        let temp_dir = tempfile::tempdir().unwrap();
        std::env::set_var("HOME", temp_dir.path());
        test();
        // TempDir cleans up automatically.
    }

    #[test]
    fn test_add_and_stats() {
        with_temp_home(|| {
            // Ensure a clean state
            let _ = fs::remove_file(get_data_path());

            add_entry("😊", Some("Good day")).unwrap();
            add_entry("😢", None).unwrap();
            add_entry("😊", None).unwrap();

            let stats_map = stats().unwrap();
            assert_eq!(stats_map.get("😊"), Some(&2usize));
            assert_eq!(stats_map.get("😢"), Some(&1usize));
        });
    }
}
