#!/usr/bin/env bash
# nightly-survival-todo – simple todo manager

set -euo pipefail

# Determine todo file
TODO_FILE="${TODO_FILE:-${PWD}/.nightly_todo.txt}"

usage() {
  cat <<'EOF'
Usage:
  nightly-survival-todo add "task description"
  nightly-survival-todo list
  nightly-survival-todo done <id>
EOF
  exit 1
}

add_task() {
  local task="$1"
  echo "$task" >> "$TODO_FILE"
  echo "Added task: $task"
}

list_tasks() {
  if [[ ! -f "$TODO_FILE" ]] || [[ ! -s "$TODO_FILE" ]]; then
    echo "No tasks."
    return
  fi
  local i=1
  while IFS= read -r line; do
    printf "%d) %s\n" "$i" "$line"
    ((i++))
  done < "$TODO_FILE"
}

done_task() {
  local id="$1"
  if [[ ! -f "$TODO_FILE" ]]; then
    echo "No tasks."
    exit 1
  fi
  local tmp
  tmp=$(mktemp) || exit 1
  local i=1
  local removed=0
  while IFS= read -r line; do
    if [[ $i -eq $id ]]; then
      echo "Completed: $line"
      removed=1
    else
      echo "$line" >> "$tmp"
    fi
    ((i++))
  done < "$TODO_FILE"
  if [[ $removed -eq 0 ]]; then
    echo "Task ID $id not found."
    rm -f "$tmp"
    exit 1
  fi
  mv "$tmp" "$TODO_FILE"
}

if [[ $# -lt 1 ]]; then
  usage
fi

cmd="$1"
shift

case "$cmd" in
  add)
    if [[ $# -lt 1 ]]; then usage; fi
    add_task "$*"
    ;;
  list)
    list_tasks
    ;;
  done)
    if [[ $# -lt 1 ]]; then usage; fi
    done_task "$1"
    ;;
  *)
    usage
    ;;
esac
