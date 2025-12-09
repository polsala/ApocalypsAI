use nightly_rainbowify_cli::rainbow;

#[test]
fn test_rainbow_full_sentence() {
    let input = "Rust";
    // Expected colors: R(31), u(33), s(32), t(36)
    let expected = "\x1b[31mR\x1b[0m\x1b[33mu\x1b[0m\x1b[32ms\x1b[0m\x1b[36mt\x1b[0m";
    assert_eq!(rainbow(input), expected);
}

// Mock rationale: No external I/O, deterministic function.
