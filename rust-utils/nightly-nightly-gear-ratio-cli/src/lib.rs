pub fn compute_gear_inches(chainring: u32, cog: u32, wheel_diameter_mm: u32) -> f64 {
    if cog == 0 {
        return 0.0;
    }
    let ratio = chainring as f64 / cog as f64;
    let wheel_inch = wheel_diameter_mm as f64 * std::f64::consts::PI / 25.4;
    ratio * wheel_inch
}
