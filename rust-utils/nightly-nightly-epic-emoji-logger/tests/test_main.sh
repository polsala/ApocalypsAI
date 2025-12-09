#!/usr/bin/env bash
set -euo pipefail

# Compile
rustc src/main.rs -o logger

# Test 1: error line
printf \"error: something failed\\n\" | ./logger > output.txt
grep -q \"❌ error: something failed\" output.txt

# Test 2: warning line
printf \"warning: low battery\\n\" | ./logger > output.txt
grep -q \"⚠️ warning: low battery\" output.txt

# Test 3: info line
printf \"info: all good\\n\" | ./logger > output.txt
grep -q \"ℹ️ info: all good\" output.txt

# Test 4: debug line
printf \"debug: variable x=5\\n\" | ./logger > output.txt
grep -q \"🐛 debug: variable x=5\" output.txt

# Test 5: default
printf \"just a normal line\\n\" | ./logger > output.txt
grep -q \"📜 just a normal line\" output.txt

echo \"All tests passed\"
