use nightly_safehouse_name_generator::generate_name;

#[test]
fn same_seed_produces_same_name() {
    let seed = 12345u64;
    let first = generate_name(seed);
    let second = generate_name(seed);
    assert_eq!(first, second);
}
