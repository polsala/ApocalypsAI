#!/bin/sh

ARCHIVE_PATH="$1"

if [ -z "$ARCHIVE_PATH" ]; then
    echo "Usage: inspect_cache.sh <archive_path>"
    echo "\nMount your archive to /mnt/cache/<your_archive_name> inside the container."
    echo "Example: docker run --rm -v /host/path/archive.tar.gz:/mnt/cache/archive.tar.gz nightly-survival-cache-inspector /mnt/cache/archive.tar.gz"
    exit 1
fi

if [ ! -f "$ARCHIVE_PATH" ]; then
    echo "Error: Archive not found at '$ARCHIVE_PATH'. Please ensure it's correctly mounted."
    exit 1
fi

echo "--- Archive SHA256 Sum ---"
sha256sum "$ARCHIVE_PATH"

echo "\n--- Archive Contents ---"
case "$ARCHIVE_PATH" in
    *.tar|*.tar.gz|*.tgz|*.tar.bz2|*.tbz|*.tar.xz|*.txz)
        tar tvf "$ARCHIVE_PATH"
        ;;
    *.zip)
        unzip -l "$ARCHIVE_PATH"
        ;;
    *)
        echo "Warning: Unknown archive type for '$ARCHIVE_PATH'. Attempting to list with 'file' command and then 'tar' or 'unzip'."
        file "$ARCHIVE_PATH"
        # Try tar first, then unzip as a fallback for unknown types
        if tar tvf "$ARCHIVE_PATH" 2>/dev/null; then
            echo "(Listed with tar)"
        elif unzip -l "$ARCHIVE_PATH" 2>/dev/null; then
            echo "(Listed with unzip)"
        else
            echo "Error: Could not list contents with 'tar' or 'unzip'. Archive format might be unsupported."
            exit 1
        fi
        ;;
esac
