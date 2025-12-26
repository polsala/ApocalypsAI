use nightly_dice_roller::{parse_notation, roll_dice};
use rand::rngs::mock::StepRng;

#[test]
fn test_parse_notation() {
    assert_eq!(parse_notation("2d6+3"), Some((2, 6, 3)));
    assert_eq!(parse_notation("4d10-2"), Some((4, 10, -2)));
    assert_eq!(parse_notation("1d20"), Some((1, 20, 0)));
    assert_eq!(parse_notation("bad"), None);
}

#[test]
fn test_roll_dice_deterministic() {
    // StepRng::new(start, step) returns a deterministic sequence.
    // Using start=1 and step=0 makes every call return 1.
    let mut rng = StepRng::new(1, 0);
    let total = roll_dice(3, 6, &mut rng);
    assert_eq!(total, 3); // three rolls of 1 each
}
