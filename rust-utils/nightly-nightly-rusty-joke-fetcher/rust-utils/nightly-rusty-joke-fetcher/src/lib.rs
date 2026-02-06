use reqwest::blocking::Client;
use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct Joke {
    pub setup: String,
    pub punchline: String,
}

pub fn fetch_joke(url: &str) -> Result<Joke, Box<dyn std::error::Error>> {
    let client = Client::new();
    let resp = client.get(url).send()?;
    let joke: Joke = resp.json()?;
    Ok(joke)
}
