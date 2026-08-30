use survival_tip::{tip_with_seed, TIPS};\n\n#[test]\nfn tip_is_from_list() {\n    let tip = tip_with_seed(12345);\n    assert!(TIPS.contains(&tip), "Tip should be one of the predefined tips");\n}
