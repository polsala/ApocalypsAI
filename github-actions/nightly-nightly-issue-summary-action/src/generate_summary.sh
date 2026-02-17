#!/usr/bin/env bash
set -euo pipefail

# Mock rationale: In tests, curl is overridden to return fixture data.

if [[ -z "${GITHUB_TOKEN:-}" || -z "${GITHUB_REPOSITORY:-}" ]]; then
  echo "Missing required env vars GITHUB_TOKEN or GITHUB_REPOSITORY" >&2
  exit 1
fi

issues_json=$(curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$GITHUB_REPOSITORY/issues?state=open&per_page=100")

# Use jq to group issues by label name
# For issues without labels, group under "No Label"
summary=$(echo "$issues_json" | jq -r '
  .[] |
  {title: .title, number: .number, labels: (.labels | map(.name))} |
  . as $issue |
  ($issue.labels | length) as $len |
  if $len == 0 then
    "No Label"
  else
    $issue.labels[]
  end as $label |
  "\($label)\t\($issue.number)\t\($issue.title)"
' | sort | awk -F'\t' '
  {
    label=$1; num=$2; title=$3;
    count[label]++;
    issues[label]=issues[label] (count[label]==1 ? "" : "\n") "- #"num" "title;
  }
  END {
    for (l in issues) {
      printf "## %s\n%s\n\n", (l=="No Label"?"No Label":l), issues[l];
    }
  }
')

echo -e "# Open Issues Summary\n\n$summary"
