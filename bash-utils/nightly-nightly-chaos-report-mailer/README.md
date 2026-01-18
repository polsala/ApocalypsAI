# nightly-chaos-report-mailer

A Bash utility that sends a fun, themed email summarizing the outcome of chaos engineering experiments. Designed for post-apocalyptic DevOps teams who still want to keep everyone in the loop—with style.

## Features

- Reads chaos experiment results from JSON
- Generates a themed email body using templates
- Sends email via SMTP (configurable)
- Lightweight and portable

## Usage

```bash
./chaos_report_mailer.sh --to admin@example.com --from chaosbot@apocalyp.se --subject "Chaos Report: The Wasteland Awakens" --results results.json
```

## Requirements

- Bash 4+
- `mail` or `sendmail` configured
- `jq` for JSON parsing

## Testing

Run the test suite with:

```bash
bats tests/test_chaos_report_mailer.bats
```
