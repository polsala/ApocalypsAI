#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wrap_word_hello() {
        let word = "hello";
        let wrapped = wrap_word(word);
        assert_eq!(wrapped, "🤣hello🤣");
    }

    #[test]
    fn test_wrap_word_world() {
        let word = "world";
        let wrapped = wrap_word(word);
        assert_eq!(wrapped, "😄world😄");
    }

    #[test]
    fn test_process_input() {
        let input = "hello world";
        let output = process_input(input);
        assert_eq!(output, "🤣hello🤣 😄world😄");
    }

    #[test]
    fn test_process_input_single_word() {
        let input = "rust";
        let output = process_input(input);
        assert_eq!(output, "🤣rust🤣");
    }
}
