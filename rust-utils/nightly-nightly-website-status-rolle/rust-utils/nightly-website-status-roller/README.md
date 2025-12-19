# nightly-website-status-roller

A whimsical Rust CLI that rolls the status of your favorite URLs.  
It fetches each URL, prints the HTTP status code, and adds a matching emoji.

## Usage

```bash
# From a file
nightly-website-status-roller urls.txt

# From stdin
cat urls.txt | nightly-website-status-roller

# With a single URL
nightly-website-status-roller https://example.com
```

## Output

```
🌐 Status Roller 🎲
https://example.com 200 ✅
https://nonexistent.com 404 ❌
```

## Installation

```bash
cargo install nightly-website-status-roller
```

## Tests

Run `cargo test` to verify deterministic behavior using mocked endpoints.
