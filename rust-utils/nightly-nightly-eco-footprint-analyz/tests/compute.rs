use eco_footprint_analyzer::compute_total;

#[test]
fn test_compute_total() {
    let csv = "activity,co2_kg\ndriving,2.5\neating_beef,3.0\n";
    let total = compute_total(csv).expect("should compute");
    assert!((total - 5.5).abs() < 1e-6);
}
