use cryptic_plant_namer::generate_name;

#[test]
fn test_generate_name_seed_42() {
    assert_eq!(generate_name(42), "Whispering Daphneia");
}
