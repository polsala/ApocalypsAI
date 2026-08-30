use nightly_ramble_tips::get_tip;

#[test]
fn deterministic_tip() {
    let tip = get_tip(Some(42));
    assert_eq!(tip, "A well‑maintained flashlight is worth more than gold.");
}
