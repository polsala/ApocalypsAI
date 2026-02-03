#!/bin/bash

REPO_PATH="$1"
THRESHOLD="${2:-10}"

if [ -z "$REPO_PATH" ]; then
  echo "Usage: $0 <repo-path> [threshold]"
  exit 1
fi

if [ ! -d "$REPO_PATH/.git" ]; then
  echo "Error: $REPO_PATH is not a Git repository."
  exit 1
fi

pushd "$REPO_PATH" > /dev/null

# Get commit counts per author in the last 7 days
AUTHOR_COMMITS=$(git log --since="7 days ago" --pretty=format:"%an" | sort | uniq -c | sort -nr)

# Filter authors exceeding threshold
echo "$AUTHOR_COMMITS" | while read -r count author; do
  if [ "$count" -gt "$THRESHOLD" ]; then
    echo "Gremlin Alert: $author has $count commits in the last 7 days (threshold: $THRESHOLD)."
  fi
done

popd > /dev/null
