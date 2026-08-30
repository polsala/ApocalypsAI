use wasteland_nickname::generate_nickname;

#[test]
fn test_generate_nickname_alice() {
    // Checksum for "Alice" = 65 + 108 + 105 + 99 + 101 = 478
    // 478 % 10 = 8 -> "Ashen"
    // (478 / 10) = 47; 47 % 7 = 5 -> "the Keeper"
    let result = generate_nickname("Alice");
    assert_eq!(result, "Ashen Alice the Keeper");
}
