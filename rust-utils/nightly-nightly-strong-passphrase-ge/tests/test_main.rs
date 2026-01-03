use nightly_strong_passphrase_generator::PassphraseOptions;
use nightly_strong_passphrase_generator::generate_passphrase;

#[test]
fn test_default_generation() {
    std::env::set_var("PASSGEN_SEED", "42");
    let opts = PassphraseOptions {
        words: 4,
        include_numbers: false,
        include_symbols: false,
    };
    let pass = generate_passphrase(&opts);
    assert_eq!(pass, "date-kiwi-honeydew-elderberry");
}

#[test]
fn test_numbers_and_symbols() {
    std::env::set_var("PASSGEN_SEED", "12345");
    let opts = PassphraseOptions {
        words: 3,
        include_numbers: true,
        include_symbols: true,
    };
    let pass = generate_passphrase(&opts);
    let has_digit = pass.chars().any(|c| c.is_ascii_digit());
    let has_symbol = pass.chars().any(|c| "!@#$%^&*".contains(c));
    assert!(has_digit);
    assert!(has_symbol);
}

#[test]
fn test_custom_word_count() {
    std::env::set_var("PASSGEN_SEED", "999");
    let opts = PassphraseOptions {
        words: 5,
        include_numbers: false,
        include_symbols: false,
    };
    let pass = generate_passphrase(&opts);
    assert_eq!(pass, "kiwi-honeydew-cherry-date-kiwi");
}
