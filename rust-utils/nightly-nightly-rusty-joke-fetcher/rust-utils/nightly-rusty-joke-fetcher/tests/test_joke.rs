#[cfg(test)]
mod tests {
    use nightly_rusty_joke_fetcher::fetch_joke;
    use mockito::{mock, server_address};

    #[test]
    fn test_fetch_joke_success() {
        let _m = mock("GET", "/random_joke")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(r#"{\"setup\":\"Why did the chicken cross the road?\",\"punchline\":\"To get to the other side.\"}"#)
            .create();

        let url = &format!("http://{}/random_joke", server_address());
        let joke = fetch_joke(url).expect("should fetch joke");
        assert_eq!(joke.setup, "Why did the chicken cross the road?");
        assert_eq!(joke.punchline, "To get to the other side.");
    }

    #[test]
    fn test_fetch_joke_failure() {
        let _m = mock("GET", "/random_joke")
            .with_status(500)
            .create();

        let url = &format!("http://{}/random_joke", server_address());
        let result = fetch_joke(url);
        assert!(result.is_err());
    }
}
