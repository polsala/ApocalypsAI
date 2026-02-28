#!/usr/bin/env bash
set -euo pipefail

# Create a temporary CSV data file
DATA_FILE=$(mktemp)
cat > "$DATA_FILE" <<'EOF'
Fern,2023-09-01,7
Cactus,2023-09-10,30
EOF

# Export environment variables so the script uses the temporary file and a fixed current date
export PLANT_DATA_FILE="$DATA_FILE"
export DATE_OVERRIDE="2023-09-15"

# Helper to run the script
run() {
  ./src/reminder.sh "$@"
}

# Test --list output
list_output=$(run --list)
expected_list="Fern: next watering on 2023-09-08
Cactus: next watering on 2023-10-10"
if [[ "$list_output" != "$expected_list" ]]; then
  echo "FAIL: --list output mismatch"
  echo "Got:"; echo "$list_output"
  echo "Expected:"; echo "$expected_list"
  exit 1
fi

# Test plant needing water
fern_output=$(run Fern)
if [[ "$fern_output" != "💧 Plant 'Fern' needs watering!" ]]; then
  echo "FAIL: Fern watering check"
  echo "Got: $fern_output"
  exit 1
fi

# Test plant not needing water
cactus_output=$(run Cactus)
if [[ "$cactus_output" != "✅ Plant 'Cactus' is fine." ]]; then
  echo "FAIL: Cactus watering check"
  echo "Got: $cactus_output"
  exit 1
fi

# Test marking a plant as watered
run --water Fern
new_last=$(awk -F, '$1=="Fern"{print $2}' "$DATA_FILE")
if [[ "$new_last" != "2023-09-15" ]]; then
  echo "FAIL: Fern watering date not updated"
  echo "Got: $new_last"
  exit 1
fi

echo "All tests passed"
