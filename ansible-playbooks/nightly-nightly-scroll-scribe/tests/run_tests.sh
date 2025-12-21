#!/bin/bash
set -euo pipefail

TEST_DIR="/tmp/scroll_scribe_test"
INVENTORY_FILE="tests/test_inventory.ini"
PLAYBOOK_FILE="tests/test_scribe_playbook.yml" # This playbook imports scribe_playbook.yml

echo "--- Running Nightly Scroll Scribe Tests ---"

# Clean up previous test runs
echo "Cleaning up previous test directory: $TEST_DIR"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"

# Mock rationale: Create mock markdown files for testing various compliance scenarios.
# This ensures deterministic and offline testing by controlling the input data.
echo "Creating mock scrolls..."

# Good scroll: Has all required front matter keys and tags
cat <<EOF > "$TEST_DIR/good_scroll.md"
---
title: "A Well-Formed Scroll"
date: "2023-10-27"
tags:
  - knowledge
  - reference
  - ansible
---
This is a perfectly compliant scroll.
EOF

# Scroll with no front matter
cat <<EOF > "$TEST_DIR/no_front_matter.md"
This scroll has no front matter at all.
EOF

# Scroll with missing a required key (e.g., 'date')
cat <<EOF > "$TEST_DIR/missing_key.md"
---
title: "Missing Date Scroll"
tags:
  - knowledge
  - reference
---
This scroll is missing the 'date' key.
EOF

# Scroll with missing a required tag (e.g., 'reference')
cat <<EOF > "$TEST_DIR/missing_tag.md"
---
title: "Missing Reference Tag Scroll"
date: "2023-10-27"
tags:
  - knowledge
  - ansible
---
This scroll is missing the 'reference' tag.
EOF

# Scroll with malformed front matter (e.g., missing closing '---')
cat <<EOF > "$TEST_DIR/malformed_front_matter.md"
---
title: "Malformed Scroll"
date: "2023-10-27"
tags:
  - knowledge
This scroll has malformed front matter.
EOF

echo "Running Ansible playbook for testing..."
# Run the test playbook, capturing output as JSON.
# Pass scroll_directory as an extra var to override the default in vars/main.yml.
ANSIBLE_STDOUT_CALLBACK=json ansible-playbook -i "$INVENTORY_FILE" "$PLAYBOOK_FILE" -e "scroll_directory=$TEST_DIR" > "$TEST_DIR/ansible_output.json"

echo "Analyzing test results..."

# Mock rationale: Parse the JSON output from Ansible to deterministically check compliance.
# This is deterministic and offline as it only processes local files and Ansible output.

# Extract the debug messages for compliant and non-compliant scrolls
COMPLIANT_MSG=$(jq -r '.plays[0].tasks[] | select(.task.name == "Report compliant scrolls") | .hosts.localhost.msg' "$TEST_DIR/ansible_output.json")
NON_COMPLIANT_MSG=$(jq -r '.plays[0].tasks[] | select(.task.name == "Report non-compliant scrolls") | .hosts.localhost.msg' "$TEST_DIR/ansible_output.json")
DETAILED_ISSUES_MSGS=$(jq -r '.plays[0].tasks[] | select(.task.name == "Display detailed issues for non-compliant scrolls") | .hosts.localhost.msg' "$TEST_DIR/ansible_output.json")

# Check for compliant scrolls count and content
if echo "$COMPLIANT_MSG" | grep -q "good_scroll.md"; then
    echo "✅ Correctly identified 'good_scroll.md' as compliant."
else
    echo "❌ Failed to identify 'good_scroll.md' as compliant."
    exit 1
fi

# Check for non-compliant scrolls count and content
NON_COMPLIANT_SCROLLS=("no_front_matter.md" "missing_key.md" "missing_tag.md" "malformed_front_matter.md")
ALL_NON_COMPLIANT_FOUND=true
for scroll in "${NON_COMPLIANT_SCROLLS[@]}"; do
    if ! echo "$NON_COMPLIANT_MSG" | grep -q "$scroll"; then
        echo "❌ Failed to identify '$scroll' as non-compliant."
        ALL_NON_COMPLIANT_FOUND=false
    fi
done

if "$ALL_NON_COMPLIANT_FOUND"; then
    echo "✅ Correctly identified all 4 non-compliant scrolls."
else
    exit 1
fi

# Check specific issues for malformed_front_matter.md
if echo "$DETAILED_ISSUES_MSGS" | grep -q "malformed_front_matter.md" && echo "$DETAILED_ISSUES_MSGS" | grep -q "Missing or malformed YAML front matter"; then
    echo "✅ Correctly identified malformed front matter issue for 'malformed_front_matter.md'."
else
    echo "❌ Failed to identify malformed front matter issue for 'malformed_front_matter.md'."
    exit 1
fi

# Check specific issues for missing_key.md
if echo "$DETAILED_ISSUES_MSGS" | grep -q "missing_key.md" && echo "$DETAILED_ISSUES_MSGS" | grep -q "Missing required key: date"; then
    echo "✅ Correctly identified missing key issue for 'missing_key.md'."
else
    echo "❌ Failed to identify missing key issue for 'missing_key.md'."
    exit 1
fi

# Check specific issues for missing_tag.md
if echo "$DETAILED_ISSUES_MSGS" | grep -q "missing_tag.md" && echo "$DETAILED_ISSUES_MSGS" | grep -q "Missing required tag: reference"; then
    echo "✅ Correctly identified missing tag issue for 'missing_tag.md'."
else
    echo "❌ Failed to identify missing tag issue for 'missing_tag.md'."
    exit 1
fi


echo "All tests passed for Nightly Scroll Scribe!"

# Clean up test directory
rm -rf "$TEST_DIR"
