# Nightly API Mood Ring

## Summary
`nightly-api-mood-ring` is a whimsical-yet-useful Go utility that concurrently checks the 'mood' of a list of web APIs. Instead of just reporting 'up' or 'down', it assigns an emotional state (e.g., "Serene", "Furious", "Confused") based on HTTP status codes, response times, and connectivity.

This tool is perfect for a quick, at-a-glance assessment of your distributed system's emotional well-being.

## Features
- **Concurrent API Checks**: Utilizes Go's goroutines to check multiple APIs simultaneously.
- **Whimsical Mood Reporting**: Translates technical metrics (status codes, latency) into relatable emotional states.
- **Configurable**: Easily provide a list of URLs via a file or standard input.
- **Timeout Handling**: Detects and reports unresponsive APIs.

## Installation
To install `nightly-api-mood-ring`, ensure you have Go (1.16 or higher) installed, then:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/go-utils/nightly-api-mood-ring/src
go build -o ../nightly-api-mood-ring .
# The executable will be in go-utils/nightly-api-mood-ring/nightly-api-mood-ring
```

## Usage

### 1. Create a list of URLs
Create a file, e.g., `urls.txt`, with one URL per line:

```
https://api.example.com/health
https://another.service.org/status
http://localhost:8080/metrics
```

### 2. Run the utility

**From a file:**
```bash
./nightly-api-mood-ring -urls ../urls.txt
```

**From standard input (pipe):**
```bash
echo -e "https://api.example.com/health\nhttps://another.service.org/status" | ./nightly-api-mood-ring
```

**Example Output:**
```
Checking API Moods...

URL: https://api.example.com/health
  Status: 200 OK
  Latency: 45ms
  Mood: Serene

URL: https://another.service.org/status
  Status: 500 Internal Server Error
  Latency: 120ms
  Mood: Furious

URL: http://localhost:8080/metrics
  Status: 404 Not Found
  Latency: 15ms
  Mood: Confused

URL: https://slow.api.com/data
  Status: 200 OK
  Latency: 780ms
  Mood: Sluggish

URL: https://unreachable.com
  Status: 0 (Error)
  Latency: 0ms
  Mood: Silent (Connection Error)
```

## Configuration

- `-urls <file_path>`: Specify a file containing URLs (one per line). If not provided, URLs are read from stdin.
- `-timeout <duration>`: Set the HTTP request timeout (e.g., `5s`, `500ms`). Default is `3s`.

## Development

### Running Tests
From the `go-utils/nightly-api-mood-ring` directory:

```bash
go test ./tests
```

## Contributing
Feel free to contribute to the emotional well-being of our APIs! Submit issues or pull requests to the ApocalypsAI repository.
