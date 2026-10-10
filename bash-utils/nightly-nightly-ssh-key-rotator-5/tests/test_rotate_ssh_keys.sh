#!/usr/bin/env bash
set -euo pipefail

# Locate the script under the repository layout
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../src" && pwd)"
SCRIPT="${SCRIPT_DIR}/rotate_ssh_keys.sh"

# Create an isolated temporary directory for testing
TMPDIR=$(mktemp -d)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

# ---------- Dry‑run test ----------
DRY_OUTPUT=$("$SCRIPT" -d "$TMPDIR" -n)
if [[ "$DRY_OUTPUT" != *"Would generate rsa key"* ]]; then
  echo "[FAIL] Dry‑run did not report expected actions"
  exit 1
fi

# Ensure no key files were created during dry‑run
if compgen -G "$TMPDIR/ssh_host_*_key" > /dev/null; then
  echo "[FAIL] Keys were created during dry‑run"
  exit 1
fi

echo "[PASS] Dry‑run behavior verified"

# ---------- Real run test ----------
"$SCRIPT" -d "$TMPDIR"
for type in rsa ecdsa ed25519; do
  KEY_PATH="$TMPDIR/ssh_host_${type}_key"
  if [[ ! -f "$KEY_PATH" ]]; then
    echo "[FAIL] Expected key $KEY_PATH not found"
    exit 1
  fi
  # Verify that a backup exists if the script was run a second time
  if [[ -f "${KEY_PATH}.bak.${timestamp}" ]]; then
    echo "[INFO] Backup detected for $type (optional)"
  fi
done

echo "[PASS] Real run generated all expected SSH host keys"

# All tests passed
exit 0
