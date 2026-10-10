#[cfg(test)]
mod tests {
    use nightly_scavenger_map::generate_map;

    #[test]
    fn deterministic_dimensions_and_symbols() {
        // Mock rationale: fixed seed ensures reproducible output for testing
        let width = 7;
        let height = 4;
        let seed = 123456789;
        let map = generate_map(width, height, seed);
        let lines: Vec<&str> = map.split('\n').collect();
        assert_eq!(lines.len(), height, "Map should have {} rows", height);
        for line in lines {
            assert_eq!(line.chars().count(), width, "Each row should have {} columns", width);
            for ch in line.chars() {
                assert!(matches!(ch, '.' | 'W' | 'F' | 'M' | 'T'), "Invalid symbol '{}' found", ch);
            }
        }
    }
}
