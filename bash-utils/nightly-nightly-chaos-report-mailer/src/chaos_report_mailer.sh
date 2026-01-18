#!/bin/bash

set -euo pipefail

# Default values
FROM="chaosbot@apocalyp.se"
TO=""
SUBJECT="Chaos Report: The Wasteland Awakens"
RESULTS_FILE=""
SMTP_SERVER="localhost"
SMTP_PORT="25"

# Help message
usage() {
  echo "Usage: $0 --to EMAIL --results FILE [--from EMAIL] [--subject SUBJECT] [--smtp-server HOST] [--smtp-port PORT]"
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --from)
      FROM="$2"
      shift 2
      ;;
    --to)
      TO="$2"
      shift 2
      ;;
    --subject)
      SUBJECT="$2"
      shift 2
      ;;
    --results)
      RESULTS_FILE="$2"
      shift 2
      ;;
    --smtp-server)
      SMTP_SERVER="$2"
      shift 2
      ;;
    --smtp-port)
      SMTP_PORT="$2"
      shift 2
      ;;
    *)
      usage
      ;;
  esac
done

# Validate required args
if [[ -z "$TO" || -z "$RESULTS_FILE" ]]; then
  echo "Error: --to and --results are required."
  usage
fi

if [[ ! -f "$RESULTS_FILE" ]]; then
  echo "Error: Results file '$RESULTS_FILE' not found."
  exit 1
fi

# Generate email body
read -r -d '' TEMPLATE <<EOF
Subject: $SUBJECT
To: $TO
From: $FROM

Greetings Survivor,

The chaos winds have settled. Here's the latest report from the wasteland:

$(jq -r '.scenarios[] | "- \(.name): \(.status)"' < "$RESULTS_FILE")

Stay vigilant. The machines are watching.

— ChaosBot v2.1
EOF

# Send email
if command -v sendmail > /dev/null; then
  echo "$TEMPLATE" | sendmail -t
elif command -v mail > /dev/null; then
  echo "$TEMPLATE" | mail -s "$SUBJECT" "$TO"
else
  echo "Error: No mail command found. Please configure sendmail or mail."
  exit 1
fi

echo "Chaos report sent to $TO."
