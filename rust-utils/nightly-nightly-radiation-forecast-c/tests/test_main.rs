#[cfg(test)]
mod tests {
    use nightly_radiation_forecast_cli::compute_radiation;

    #[test]
    fn test_known_values() {
        // (lat, lon) -> expected level using the same formula as the implementation
        let cases = vec![
            ((0.0_f64, 0.0_f64), 1_u32),
            ((10.0_f64, 20.0_f64), ((10 * 31 + 20 * 17) % 100 + 1) as u32),
            ((-34.05_f64, 118.25_f64), ((34 * 31 + 118 * 17) % 100 + 1) as u32),
            ((-90.0_f64, -180.0_f64), ((90 * 31 + 180 * 17) % 100 + 1) as u32),
        ];
        for ((lat, lon), expected) in cases {
            assert_eq!(compute_radiation(lat, lon), expected);
        }
    }
}
