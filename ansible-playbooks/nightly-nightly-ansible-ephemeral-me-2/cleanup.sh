#!/bin/bash
# Manual cleanup script for ephemeral messages

MESSAGE_FILE="/tmp/apocalypsai_ephemeral_message"
CLEANUP_SCRIPT="/tmp/apocalypsai_cleanup.sh"
REPORT_DIR="/tmp"

echo "=== ApocalypsAI Ephemeral Message Cleanup ==="
echo "Cleaning up ephemeral messages..."

# Remove message file
if [ -f "$MESSAGE_FILE" ]; then
    rm -f "$MESSAGE_FILE"
    echo "✓ Removed message file: $MESSAGE_FILE"
else
    echo "- Message file not found: $MESSAGE_FILE"
fi

# Remove cleanup script
if [ -f "$CLEANUP_SCRIPT" ]; then
    rm -f "$CLEANUP_SCRIPT"
    echo "✓ Removed cleanup script: $CLEANUP_SCRIPT"
else
    echo "- Cleanup script not found: $CLEANUP_SCRIPT"
fi

# Remove report files
REPORT_FILES=$(find "$REPORT_DIR" -name "apocalypsai_report_*.txt" 2>/dev/null)
if [ -n "$REPORT_FILES" ]; then
    echo "$REPORT_FILES" | while read -r file; do
        rm -f "$file"
        echo "✓ Removed report file: $file"
    done
else
    echo "- No report files found"
fi

# Remove PID file
PID_FILE="/tmp/apocalypsai_cleanup.pid"
if [ -f "$PID_FILE" ]; then
    rm -f "$PID_FILE"
    echo "✓ Removed PID file: $PID_FILE"
else
    echo "- PID file not found: $PID_FILE"
fi

echo "\nCleanup complete! All ephemeral messages have been removed."
echo "=== End Cleanup ==="
