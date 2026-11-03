#!/bin/bash

# This script generates the Apocalypse Readiness Report Card.
# It expects REPORT_LEVEL to be set in the environment.
# It outputs the report content to stdout.

REPORT_CONTENT=""
SCORE=0
MAX_SCORE=0

# Function to check for file existence and add to report
check_file() {
  MAX_SCORE=$((MAX_SCORE + 1))
  if [ -f "$1" ]; then
    REPORT_CONTENT="${REPORT_CONTENT}- ✅ **$1**: Present\n"
    SCORE=$((SCORE + 1))
  else
    REPORT_CONTENT="${REPORT_CONTENT}- ❌ **$1**: Missing\n"
  fi
}

# Function to check for directory existence
check_dir() {
  MAX_SCORE=$((MAX_SCORE + 1))
  if [ -d "$1" ]; then
    REPORT_CONTENT="${REPORT_CONTENT}- ✅ **$1/**: Present\n"
    SCORE=$((SCORE + 1))
  else
    REPORT_CONTENT="${REPORT_CONTENT}- ❌ **$1/**: Missing\n"
  fi
}

REPORT_CONTENT="### 📜 Apocalypse Readiness Report Card 📜\n\n"
REPORT_CONTENT="${REPORT_CONTENT}This report assesses the repository's readiness based on common best practices.\n\n"
REPORT_CONTENT="${REPORT_CONTENT}--- \n\n"

# Basic checks
check_file "README.md"
check_file "LICENSE"

if [ "$REPORT_LEVEL" == "standard" ] || [ "$REPORT_LEVEL" == "full" ]; then
  check_file "CONTRIBUTING.md"
  check_file "SECURITY.md"
  check_file "CODE_OF_CONDUCT.md"
fi

if [ "$REPORT_LEVEL" == "full" ]; then
  check_dir ".github/workflows"
  check_dir ".github/ISSUE_TEMPLATE"
  check_dir ".github/PULL_REQUEST_TEMPLATE"
  check_file "CHANGELOG.md"
fi

REPORT_CONTENT="${REPORT_CONTENT}\n--- \n\n"
REPORT_CONTENT="${REPORT_CONTENT}**Overall Readiness Score**: ${SCORE}/${MAX_SCORE}\n"

if [ "$SCORE" -eq "$MAX_SCORE" ]; then
  REPORT_CONTENT="${REPORT_CONTENT}🎉 **Status**: Fully Prepared for the Inevitable! 🎉"
elif [ "$SCORE" -ge "$((MAX_SCORE * 3 / 4))" ]; then
  REPORT_CONTENT="${REPORT_CONTENT}👍 **Status**: Mostly Ready, but a few cosmic tweaks could help."
elif [ "$SCORE" -ge "$((MAX_SCORE / 2))" ]; then
  REPORT_CONTENT="${REPORT_CONTENT}⚠️ **Status**: Some Preparations Made, but Gaps Remain. Proceed with Caution."
else
  REPORT_CONTENT="${REPORT_CONTENT}🚨 **Status**: Significant Gaps Detected. The Apocalypse Awaits! 🚨"
fi

echo -e "$REPORT_CONTENT"
