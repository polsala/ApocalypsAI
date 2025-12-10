#[cfg(test)]
mod tests {
    use crate::add_emoji_to_commit;

    #[test]
    fn test_feat() {
        let input = "feat: add new feature\n\nDetailed description.";
        let expected = "🚀 feat: add new feature\n\nDetailed description.";
        assert_eq!(add_emoji_to_commit(input), expected);
    }

    #[test]
    fn test_fix() {
        let input = "fix: correct bug\n\nFix details.";
        let expected = "🐛 fix: correct bug\n\nFix details.";
        assert_eq!(add_emoji_to_commit(input), expected);
    }

    #[test]
    fn test_unknown() {
        let input = "unknown: do something\n\nDetails.";
        let expected = "✨ unknown: do something\n\nDetails.";
        assert_eq!(add_emoji_to_commit(input), expected);
    }

    #[test]
    fn test_empty() {
        let input = "";
        let expected = "";
        assert_eq!(add_emoji_to_commit(input), expected);
    }
}
