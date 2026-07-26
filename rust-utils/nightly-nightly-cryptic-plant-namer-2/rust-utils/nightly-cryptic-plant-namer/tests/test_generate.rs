#[cfg(test)]
mod tests {
    use cryptic_plant_namer::generate_name;

    #[test]
    fn test_generate_name_known_indices() {
        let name = generate_name(0, 0);
        assert_eq!(name, "Gleaming folia");
        let name2 = generate_name(3, 4);
        assert_eq!(name2, "Radiant stemma");
    }

    #[test]
    fn test_generate_name_wraparound() {
        // 10 % 5 = 0, 7 % 5 = 2
        let name = generate_name(10, 7);
        assert_eq!(name, "Gleaming petalus");
    }
}
