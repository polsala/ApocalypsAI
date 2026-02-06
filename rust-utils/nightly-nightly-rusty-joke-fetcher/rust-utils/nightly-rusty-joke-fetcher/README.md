# nightly-rusty-joke-fetcher

A tiny Rust CLI that fetches a random joke from an online API and prints it.

## Usage

```bash
cargo run -- --url https://official-joke-api.appspot.com/random_joke
```

If no URL is provided, it defaults to the official joke API.

## Features

- Simple command line interface
- Uses `reqwest` for HTTP requests
- Parses JSON into a `Joke` struct
- Handles errors gracefully

## Testing

Run `cargo test` to execute the unit tests. The tests use `mockito` to mock the HTTP endpoint, ensuring deterministic offline behavior.
