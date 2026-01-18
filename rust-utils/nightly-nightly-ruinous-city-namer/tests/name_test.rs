use ruinous_city_namer::generate_name;\n\n#[test]\nfn test_name_deterministic() {\n    let name = generate_name(42);\n    assert_eq!(name, \"ra-ka\");\n}\n
