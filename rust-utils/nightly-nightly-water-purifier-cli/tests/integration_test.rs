use nightly_water_purifier_cli::recommended_steps;

#[test]
fn test_rain_low() {
    let steps = recommended_steps("rain", 30);
    assert_eq!(steps, vec![
        "Collect in clean container",
        "Boil for 1 minute"
    ]);
}

#[test]
fn test_river_medium() {
    let steps = recommended_steps("river", 120);
    assert_eq!(steps, vec![
        "Preâfilter through coarse material",
        "Boil for 5 minutes",
        "Add chlorine tablets (1 per liter)"
    ]);
}

#[test]
fn test_unknown_high() {
    let steps = recommended_steps("swamp", 300);
    assert_eq!(steps, vec![
        "Assume unknown source; treat cautiously",
        "Boil for 10 minutes",
        "Add chlorine tablets (2 per liter)",
        "Use activated carbon filter"
    ]);
}

