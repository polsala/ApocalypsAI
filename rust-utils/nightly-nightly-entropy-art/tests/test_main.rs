use nightly_entropy_art::generate_pattern;\n\n#[test]\nfn test_known_pattern() {\n    let input = "test";\n    let expected = "\
█  ████\n\
█    ██ \n\
██ █    \n\
█      █\n\
█   █   \n\
 █  ██  \n\
 █████ █\n\
 ██  █ █";\n    assert_eq!(generate_pattern(input), expected);\n}\n
