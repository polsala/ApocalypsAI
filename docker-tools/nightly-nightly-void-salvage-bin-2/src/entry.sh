#!/bin/bash

SALVAGE_DIR="/salvage"
SECRET_KEY="voidwhisper2025"

function archive_command() {
  local cmd="$1"
  local id=$(echo "$cmd" | md5sum | cut -d ' ' -f 1)
  local enc_file="$SALVAGE_DIR/$id.enc"

  echo "$cmd" | openssl enc -aes-256-cbc -salt -k "$SECRET_KEY" -out "$enc_file" 2>/dev/null
  echo "[+] Command archived with ID: $id"
}

function retrieve_command() {
  local id="$1"
  local enc_file="$SALVAGE_DIR/$id.enc"

  if [ ! -f "$enc_file" ]; then
    echo "[-] Artifact not found: $id"
    exit 1
  fi

  local cmd=$(openssl enc -d -aes-256-cbc -k "$SECRET_KEY" -in "$enc_file" 2>/dev/null)
  echo "[+] Retrieved command: $cmd"
}

function print_art() {
  echo "
    .--.    .--.
   /    \  /    \
  |      \/      |
  |              |
   \            /
    '--.    .--'
        |  |
        |  |
       /  \
      '--'"
}

if [ "$1" == "archive" ]; then
  if [ -z "$2" ]; then
    echo "[-] Usage: archive <command>"
    exit 1
  fi
  print_art
  archive_command "$2"
elif [ "$1" == "retrieve" ]; then
  if [ -z "$2" ]; then
    echo "[-] Usage: retrieve <artifact_id>"
    exit 1
  fi
  print_art
  retrieve_command "$2"
else
  echo "[-] Unknown command: $1"
  exit 1
fi
