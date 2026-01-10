#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_suggest_labels_basic() {
        let body = "This is a bug that crashes the app";
        let labels = suggest_labels(body);
        assert_eq!(labels, vec!["bug"]);
    }

    #[test]
    fn test_suggest_labels_multiple() {
        let body = "Feature request: improve performance and fix security issue";
        let labels = suggest_labels(body);
        assert_eq!(labels, vec!["enhancement", "performance", "security"]);
    }

    #[test]
    fn test_no_labels() {
        let body = "Just a random text with no keywords";
        let labels = suggest_labels(body);
        assert!(labels.is_empty());
    }
}
