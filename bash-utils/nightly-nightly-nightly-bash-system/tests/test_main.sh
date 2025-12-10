# Mock CPU/memory data for testing
MOCK_CPU="75.3"
MOCK_MEM="25.1"

# Test emoji mapping
test_emoji_mapping() {
  # Low usage
  [[ $(get_emoji 20) == "😊" ]] || { echo "Test failed: Low usage emoji"; exit 1; }
  # Medium usage
  [[ $(get_emoji 50) == "😐" ]] || { echo "Test failed: Medium usage emoji"; exit 1; }
  # High usage
  [[ $(get_emoji 80) == "😟" ]] || { echo "Test failed: High usage emoji"; exit 1; }
  echo "All emoji tests passed! ✅"
}

test_emoji_mapping
