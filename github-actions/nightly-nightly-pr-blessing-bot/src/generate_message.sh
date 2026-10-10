#!/bin/bash
set -euo pipefail

PR_STATUS="$1"

if [ -z "$PR_STATUS" ]; then
  echo "Usage: $0 <pr-status>" >&2
  exit 1
fi

MESSAGE=""
if [ "$PR_STATUS" == "success" ]; then
  MESSAGE="The cosmic dust settles, and your PR shines! ✨ May your code forever compile and your merges be swift. Huzzah, survivor! 🚀"
elif [ "$PR_STATUS" == "failure" ]; then
  MESSAGE="A minor temporal anomaly detected in your PR. ⏳ Fear not, brave coder, for even the void has its re-tries. Adjust your flux capacitor and try again! 🛠️"
else
  MESSAGE="Your PR has achieved a mysterious state: $PR_STATUS. The cosmos observes. 🌌"
fi

echo "$MESSAGE"
