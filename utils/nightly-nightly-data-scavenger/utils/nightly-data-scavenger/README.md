# Nightly Data Scavenger

## Description

The Nightly Data Scavenger is a crucial utility for sifting through the digital detritus of the old world. It helps survivors extract meaningful, structured data from unstructured log files using regular expressions. Whether you're looking for error messages, resource usage, or communication patterns, this tool will help you reclaim valuable insights from the digital wasteland.

It takes a log file path and a regular expression with named capture groups, then outputs the extracted data as JSON Lines (JSONL) for easy parsing and analysis.

## Usage

```bash
python src/scavenger.py --log-file <path_to_log_file> --pattern "<regex_pattern_with_named_groups>" [--output-file <path_to_output_jsonl_file>]
```

### Arguments:

*   `--log-file`: **Required**. Path to the input log file.
*   `--pattern`: **Required**. A regular expression string. Use `(?P<name>...)` for named capture groups to extract specific fields.
*   `--output-file`: **Optional**. Path to the output JSONL file. If not provided, output will be printed to stdout.

### Example:

Let's say you have a log file `server.log` with lines like:
`[2023-10-27 10:30:05] ERROR: Failed to connect to database 'mydb' with user 'admin'. (Attempt 3)`
`[2023-10-27 10:30:06] INFO: User 'guest' logged in from 192.168.1.10.`

To extract timestamp, log level, and message:

```bash
python src/scavenger.py \
    --log-file server.log \
    --pattern "\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (?P<level>\w+): (?P<message>.*)" \
    --output-file extracted_data.jsonl
```

This would produce `extracted_data.jsonl` with content like:

```json
{"timestamp": "2023-10-27 10:30:05", "level": "ERROR", "message": "Failed to connect to database 'mydb' with user 'admin'. (Attempt 3)"}
{"timestamp": "2023-10-27 10:30:06", "level": "INFO", "message": "User 'guest' logged in from 192.168.1.10."}
```
