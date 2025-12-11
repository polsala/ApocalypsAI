use radiation_exposure_estimator::parse_and_sum;

#[test]
fn test_parse_and_sum_basic() {
    let csv = "\
Scavenging,120,0.5\
Radioactive-Repair,30,2.0\
";
    let total = parse_and_sum(csv);
    // 120 min = 2h * 0.5 = 1.0 ; 30 min = 0.5h * 2.0 = 1.0 ; total = 2.0
    assert!((total - 2.0).abs() < 1e-6);
}

#[test]
fn test_empty_and_invalid_lines() {
    let csv = "\
InvalidLine\
,,\
Scavenging,60,1.0\
";
    let total = parse_and_sum(csv);
    // Only the valid line contributes: 60 min = 1h * 1.0 = 1.0
    assert!((total - 1.0).abs() < 1e-6);
}
