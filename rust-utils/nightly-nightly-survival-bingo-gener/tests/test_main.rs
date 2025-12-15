use nightly_survival_bingo_generator::generate_card;

#[test]
fn test_card_uniqueness() {
    let card = generate_card(Some(42));
    let mut all_tasks = Vec::new();
    for row in &card {
        for task in row {
            all_tasks.push(task.clone());
        }
    }
    let unique: std::collections::HashSet<_> = all_tasks.iter().cloned().collect();
    assert_eq!(unique.len(), 25, "All tasks should be unique");
}

#[test]
fn test_card_size() {
    let card = generate_card(Some(42));
    assert_eq!(card.len(), 5, "Card should have 5 rows");
    for row in &card {
        assert_eq!(row.len(), 5, "Each row should have 5 tasks");
    }
}

#[test]
fn test_deterministic_output() {
    let card1 = generate_card(Some(12345));
    let card2 = generate_card(Some(12345));
    assert_eq!(card1, card2, "Same seed should produce same card");
}
