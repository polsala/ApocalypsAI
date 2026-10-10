use nightly_survival_kit_builder::get_kit;

#[test]
fn test_zombie_kit() {
    let kit = get_kit("zombie");
    let expected = vec!["Baseball bat", "Spare ammo", "First aid kit", "Water filter"];
    assert_eq!(kit, expected);
}

#[test]
fn test_unknown_kit() {
    let kit = get_kit("unknown");
    let expected = vec!["Multi‑tool", "Flashlight", "Batteries", "Emergency food"];
    assert_eq!(kit, expected);
}
