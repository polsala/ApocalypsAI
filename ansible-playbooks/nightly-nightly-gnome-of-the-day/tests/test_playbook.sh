#!/usr/bin/env bash
set -e

# Run the playbook with a deterministic day (1)
ansible-playbook -i inventory.ini src/playbook.yml -e "day_of_month=1"

# Verify the file was created
if [ ! -f /tmp/gnome_of_the_day.txt ]; then
  echo "File not created"
  exit 1
fi

content=$(cat /tmp/gnome_of_the_day.txt)
expected="A gnome a day keeps the void at bay."

if [ "$content" != "$expected" ]; then
  echo "Unexpected content: $content"
  exit 1
fi

echo "Test passed"
