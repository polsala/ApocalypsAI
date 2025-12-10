#!/bin/bash

# Mock system commands for testing
export PATH="$(dirname "$0")/mocks:$PATH"

# Test 1: High CPU scenario
echo "Mocking CPU 95%..."
output=$(CPU_MOCK=95 ./src/main.sh)
[[ $output == *"🧠🔥"* ]] && echo "Test 1 passed" || echo "Test 1 failed"

# Test 2: Normal memory usage
echo "Mocking Memory 42%..."
output=$(MEM_MOCK=42 ./src/main.sh)
[[ $output == *"MemoryWarning=42%"* ]] && echo "Test 2 passed" || echo "Test 2 failed"

# Test 3: Disk warning
echo "Mocking Disk 85%..."
output=$(DISK_MOCK=85 ./src/main.sh)
[[ $output == *"💾🤔"* ]] && echo "Test 3 passed" || echo "Test 3 failed"

# Test 4: CPU temp extremes
echo "Mocking Temp 75°C..."
output=$(TEMP_MOCK=75 ./src/main.sh)
[[ $output == *"☀️75°C"* ]] && echo "Test 4 passed" || echo "Test 4 failed"

echo "All tests completed."

# mocks/top.sh
cat << 'EOF' > mocks/top.sh
#!/bin/bash
echo "Cpu(s):  $CPU_MOCK% user"
EOF
chmod +x mocks/top.sh

# mocks/free
free() {
echo "Mem:  4096 1700 2396"}

# mocks/df
df() {
echo "Filesystem      Size  Used Avail Use% Mounted at"}

# mocks/sensors
sensors() {
echo "Package id 0:  $TEMP_MOCK°C"}
