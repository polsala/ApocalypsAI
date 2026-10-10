use qr_ascii::generate_qr_ascii;

#[test]
fn integration_test_hello_world() {
    let ascii = generate_qr_ascii("Hello, world!");
    // Basic sanity checks – the output must be non‑empty and contain at least one block character
    assert!(!ascii.is_empty(), "Output should not be empty");
    assert!(ascii.contains('█'), "Output should contain block characters");
}
