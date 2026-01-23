#!/bin/bash

set -e

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <language> <project-name>"
  exit 1
fi

LANG=$1
PROJECT_NAME=$2

TEMPLATE_DIR="templates"
TARGET_DIR="$PROJECT_NAME"

if [ ! -d "$TEMPLATE_DIR/$LANG" ]; then
  echo "Error: Unsupported language '$LANG'. Supported: python, node, go, rust."
  exit 1
fi

mkdir -p "$TARGET_DIR"
cp -r "$TEMPLATE_DIR/$LANG/"* "$TARGET_DIR/"

echo "✅ Devbox for $LANG initialized in $TARGET_DIR"
