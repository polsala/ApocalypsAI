use mutant_name_generator::generate_name;

#[test]
fn deterministic_name_with_seed_42() {
    // Seed 42 should always produce "Feral Reaper"
    let name = generate_name(42);
    assert_eq!(name, "Feral Reaper");
}

#[test]
fn deterministic_name_with_seed_7() {
    // Seed 7 should always produce "Vicious Scavenger"
    let name = generate_name(7);
    assert_eq!(name, "Vicious Scavenger");
}
