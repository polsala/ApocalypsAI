#[cfg(test)]
mod tests {
    use super::*;
    use nightly_apocalypse_cipher::cipher;

    #[test]
    fn test_basic_mapping() {
        assert_eq!(cipher("abc"), "@#$");
        assert_eq!(cipher("Hello"), "h3||0");
        assert_eq!(cipher("Apocalypse"), "@p0c@lyp53");
    }

    #[test]
    fn test_non_alpha_preserved() {
        assert_eq!(cipher("123!"), "123!");
        assert_eq!(cipher("Rust-2023"), "Ru5t-2023");
    }
}
