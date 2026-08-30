use cryptid_finder::get_cryptid;

#[test]
fn test_urban() {
    assert_eq!(get_cryptid("urban"), "Skinwalker");
}

#[test]
fn test_swamp() {
    assert_eq!(get_cryptid("swamp"), "Mokele‑Mbembe");
}
