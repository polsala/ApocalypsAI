pub fn add_emoji_to_commit(message: &str) -> String {
    let mut lines: Vec<&str> = message.lines().collect();
    if lines.is_empty() {
        return message.to_string();
    }
    let first_line = lines[0];
    let emoji = match first_line.split(':').next() {
        Some(prefix) => {
            let type_part = prefix.split_whitespace().next().unwrap_or("");
            match type_part {
                "feat" => "🚀",
                "fix" => "🐛",
                "docs" => "📚",
                "style" => "🎨",
                "refactor" => "🔧",
                "test" => "🧪",
                "chore" => "🔄",
                _ => "✨",
            }
        }
        None => "✨",
    };
    lines[0] = &format!("{} {}", emoji, first_line);
    lines.join("\n")
}
