#[cfg(test)]
mod tests {
    use nightly_shelter_capacity_planner::can_survive;

    #[test]
    fn test_survivable_true() {
        // 5 people, 2 L water/day, 500 L total, 2000 kcal food/day, 100 000 kcal total, 30 days
        assert!(can_survive(5, 2.0, 500.0, 2000.0, 100_000.0, 30));
    }

    #[test]
    fn test_survivable_false() {
        // Not enough water for 10 people over 10 days
        assert!(!can_survive(10, 3.0, 200.0, 2500.0, 500_000.0, 10));
    }
}
