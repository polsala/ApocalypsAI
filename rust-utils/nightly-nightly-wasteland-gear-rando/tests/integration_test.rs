use rand::rngs::StdRng;
use rand::SeedableRng;
use wgrandom::lib::generate_item;

#[test]
fn test_generate_item_deterministic() {
    // Fixed seed for deterministic output
    let seed = [0u8; 32];
    let mut rng = StdRng::from_seed(seed);
    let item = generate_item(&mut rng);
    assert_eq!(item.name, "Rusty Pipe Wrench");
    assert_eq!(item.rarity, "Common");
    assert_eq!(item.description, "A battered item, still functional enough for survival.");
}

