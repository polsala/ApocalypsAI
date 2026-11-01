#!/bin/bash

# Configuration
# Define the list of remote hosts in the format 'user@hostname'
REMOTE_HOSTS=("user1@host1.example.com" "user2@host2.example.com" "admin@localhost")

# Define the local directory containing the configuration files to sync
SOURCE_DIR="~/my_configs/"

# Define the destination directory on the remote hosts
DEST_DIR="~/.config/synced_configs/"

# --- Script Logic ---

echo "🚀 Starting configuration synchronization..."

# Ensure source directory exists locally (optional, but good practice)
if [ ! -d "$SOURCE_DIR" ]; then
  echo "❌ Error: Source directory '$SOURCE_DIR' does not exist locally."
  exit 1
fi

for host in "${REMOTE_HOSTS[@]}"; do
  echo "
➡️ Syncing to $host..."
  
  # Use rsync to synchronize files. 
  # -a: archive mode (preserves permissions, ownership, timestamps, etc.)
  # -v: verbose output
  # -z: compress file data during the transfer
  # --delete: delete extraneous files from dest dirs (use with caution!)
  rsync -avz --delete "$SOURCE_DIR" "$host:$DEST_DIR"
  
  if [ $? -eq 0 ]; then
    echo "✅ Successfully synced to $host."
  else
    echo "❌ Error syncing to $host. Please check SSH connection and permissions."
  fi
done

echo "
🎉 Configuration synchronization complete!"
