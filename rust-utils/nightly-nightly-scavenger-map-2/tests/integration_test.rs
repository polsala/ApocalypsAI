use crate::generate_map;

#[test]
fn integration_deterministic() {
    let map_a = generate_map(4, 2, &['X'], 7);
    let map_b = generate_map(4, 2, &['X'], 7);
    assert_eq!(map_a, map_b);
}

