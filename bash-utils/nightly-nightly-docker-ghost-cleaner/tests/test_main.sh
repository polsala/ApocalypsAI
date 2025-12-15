#!/usr/bin/env bash
set -euo pipefail

# Create temp dir
tmpdir=$(mktemp -d)
trap 'rm -rf \"$tmpdir\"' EXIT

# Create mock docker script
cat > \"$tmpdir/docker\" <<'EOF'
#!/usr/bin/env bash
echo \"MOCK_DOCKER_CALL: $@\" >> \"$MOCK_LOG\"
if [[ \"$1\" == \"images\" && \"$2\" == \"-f\" && \"$3\" == \"dangling=true\" && \"$4\" == \"-q\" ]]; then
  echo \"$MOCK_DOCKER_IMAGES\"
elif [[ \"$1\" == \"rmi\" ]]; then
  # simulate removal
  echo \"Removed $2\"
else
  echo \"Unknown command\"
fi
EOF
chmod +x \"$tmpdir/docker\"

# Test case 1: dangling images present
MOCK_LOG=\"$tmpdir/mock.log\"
MOCK_DOCKER_IMAGES=\"img1\\nimg2\\nimg3\"
export MOCK_LOG MOCK_DOCKER_IMAGES

# Run script with PATH pointing to mock
PATH=\"$tmpdir:$PATH\" ./src/main.sh > \"$tmpdir/output1\"

# Verify output
output=$(cat \"$tmpdir/output1\")
if [[ \"$output\" != \"👻 Docker ghosts cleaned! (3 images removed)\" ]]; then
  echo \"Test 1 failed: unexpected output: $output\"
  exit 1
fi

# Verify mock docker calls
calls=$(cat \"$tmpdir/mock.log\")
expected_calls=$'MOCK_DOCKER_CALL: images -f dangling=true -q\\nMOCK_DOCKER_CALL: rmi img1\\nMOCK_DOCKER_CALL: rmi img2\\nMOCK_DOCKER_CALL: rmi img3\\n'
if [[ \"$calls\" != \"$expected_calls\" ]]; then
  echo \"Test 1 failed: unexpected docker calls\"
  echo \"$calls\"
  exit 1
fi

# Test case 2: no dangling images
MOCK_LOG=\"$tmpdir/mock.log\"
MOCK_DOCKER_IMAGES=\\"\\"
export MOCK_LOG MOCK_DOCKER_IMAGES

PATH=\"$tmpdir:$PATH\" ./src/main.sh > \"$tmpdir/output2\"

output=$(cat \"$tmpdir/output2\")
if [[ \"$output\" != \"🕸️ No ghosts found.\" ]]; then
  echo \"Test 2 failed: unexpected output: $output\"
  exit 1
fi

# Verify only one call to images
calls=$(cat \"$tmpdir/mock.log\")
expected_calls=$'MOCK_DOCKER_CALL: images -f dangling=true -q\\n'
if [[ \"$calls\" != \"$expected_calls\" ]]; then
  echo \"Test 2 failed: unexpected docker calls\"
  echo \"$calls\"
  exit 1
fi

echo \"All tests passed.\"
