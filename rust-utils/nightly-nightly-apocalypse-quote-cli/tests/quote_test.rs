use nightly_apocalypse_quote_cli::get_quote;

#[test]
fn deterministic_first_quote() {
    assert_eq!(get_quote(Some(0)), "The sky fell, but we still code.");
}

#[test]
fn deterministic_wraparound() {
    // Seed larger than the number of quotes to test modulo behavior
    assert_eq!(get_quote(Some(7)), "When the servers burn, the logs remain.");
}
