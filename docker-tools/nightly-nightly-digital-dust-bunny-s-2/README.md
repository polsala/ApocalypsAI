# Nightly Digital Dust Bunny Sweeper

A whimsical containerized utility that scans for and reports on digital 'dust bunnies' - orphaned files, empty directories, and stale cache artifacts.

## Features

- Scans directories for digital dust bunnies
- Generates a detailed report of findings
- Containerized for easy deployment
- Configurable scan patterns and thresholds

## Usage

```bash
# Build the container
docker build -t dust-bunny-sweeper .

# Run the sweeper
docker run --rm -v /path/to/scan:/scan dust-bunny-sweeper

# With custom configuration
docker run --rm -v /path/to/scan:/scan -v /path/to/config:/config dust-bunny-sweeper --config /config/config.json
```

## Configuration

Create a `config.json` file to customize the scan:

```json
{
  "scan_paths": ["/scan"],
  "ignore_patterns": ["*.tmp", "*.log"],
  "min_age_days": 30,
  "report_format": "json"
}
```

## Output

The sweeper generates a report in the specified format (JSON or text) detailing:
- Orphaned files
- Empty directories
- Stale cache artifacts
- Recommendations for cleanup

## License

MIT
