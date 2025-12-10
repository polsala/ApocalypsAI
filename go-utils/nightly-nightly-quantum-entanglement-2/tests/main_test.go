package main

import (
	"os"
	"testing"
)

// TestCalculateFileHash tests the hash calculation function
func TestCalculateFileHash(t *testing.T) {
	// Create a temporary test file
	testFile, err := os.CreateTemp("", "testfile")
	if err != nil {
		t.Fatalf("Failed to create temp file: %v", err)
	}
	defer os.Remove(testFile.Name())
	defer testFile.Close()

	// Write test content
	testContent := "Hello, Quantum World!"
	if _, err := testFile.WriteString(testContent); err != nil {
		t.Fatalf("Failed to write to temp file: %v", err)
	}
	testFile.Close()

	// Calculate hash
	hash, err := calculateFileHash(testFile.Name())
	if err != nil {
		t.Errorf("calculateFileHash failed: %v", err)
	}

	// Verify hash is not empty
	if hash == "" {
		t.Error("Expected non-empty hash")
	}

	// Verify hash length (SHA256 = 64 hex chars)
	if len(hash) != 64 {
		t.Errorf("Expected hash length 64, got %d", len(hash))
	}
}

// TestCheckQuantumEntanglement tests entanglement checking
func TestCheckQuantumEntanglement(t *testing.T) {
	// Create two identical test files
	testFile1, err := os.CreateTemp("", "testfile1")
	if err != nil {
		t.Fatalf("Failed to create temp file 1: %v", err)
	}
	defer os.Remove(testFile1.Name())
	defer testFile1.Close()

	testFile2, err := os.CreateTemp("", "testfile2")
	if err != nil {
		t.Fatalf("Failed to create temp file 2: %v", err)
	}
	defer os.Remove(testFile2.Name())
	defer testFile2.Close()

	// Write identical content
	testContent := "Quantum entanglement test"
	if _, err := testFile1.WriteString(testContent); err != nil {
		t.Fatalf("Failed to write to temp file 1: %v", err)
	}
	if _, err := testFile2.WriteString(testContent); err != nil {
		t.Fatalf("Failed to write to temp file 2: %v", err)
	}
	testFile1.Close()
	testFile2.Close()

	// Test entanglement (should be true)
	entangled, hash1, hash2, err := checkQuantumEntanglement(testFile1.Name(), testFile2.Name())
	if err != nil {
		t.Errorf("checkQuantumEntanglement failed: %v", err)
	}

	if !entangled {
		t.Error("Expected files to be quantum entangled")
	}

	if hash1 != hash2 {
		t.Error("Expected identical hashes for identical files")
	}

	// Create different content file
	testFile3, err := os.CreateTemp("", "testfile3")
	if err != nil {
		t.Fatalf("Failed to create temp file 3: %v", err)
	}
	defer os.Remove(testFile3.Name())
	defer testFile3.Close()

	if _, err := testFile3.WriteString("Different quantum content"); err != nil {
		t.Fatalf("Failed to write to temp file 3: %v", err)
	}
	testFile3.Close()

	// Test non-entanglement (should be false)
	entangled2, hash3, hash4, err := checkQuantumEntanglement(testFile1.Name(), testFile3.Name())
	if err != nil {
		t.Errorf("checkQuantumEntanglement failed: %v", err)
	}

	if entangled2 {
		t.Error("Expected files to NOT be quantum entangled")
	}

	if hash3 == hash4 {
		t.Error("Expected different hashes for different files")
	}
}

// TestCalculateFileHashNonExistent tests error handling for non-existent files
func TestCalculateFileHashNonExistent(t *testing.T) {
	_, err := calculateFileHash("nonexistent_file.txt")
	if err == nil {
		t.Error("Expected error for non-existent file, got nil")
	}
	// Verify error message contains filename
	if err != nil && !contains(err.Error(), "nonexistent_file.txt") {
		t.Errorf("Error message should contain filename, got: %v", err)
	}
}

// TestFormatHash tests hash formatting
func TestFormatHash(t *testing.T) {
	// Test long hash (should be truncated)
	longHash := "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
	formatted := formatHash(longHash)
	expected := "a1b2c3d4e5f6..."
	if formatted != expected {
		t.Errorf("Expected %s, got %s", expected, formatted)
	}

	// Test short hash (should not be truncated)
	shortHash := "short"
	formatted2 := formatHash(shortHash)
	if formatted2 != shortHash {
		t.Errorf("Expected %s, got %s", shortHash, formatted2)
	}
}

// Helper function to check if string contains substring
func contains(s, substr string) bool {
	return len(s) >= len(substr) && s[len(s)-len(substr):] == substr
}

// BenchmarkCalculateFileHash benchmarks hash calculation
func BenchmarkCalculateFileHash(b *testing.B) {
	// Create a temporary test file with some content
	testFile, err := os.CreateTemp("", "benchfile")
	if err != nil {
		b.Fatalf("Failed to create temp file: %v", err)
	}
	defer os.Remove(testFile.Name())
	defer testFile.Close()

	// Write test content
	testContent := make([]byte, 1024*1024) // 1MB of data
	if _, err := testFile.Write(testContent); err != nil {
		b.Fatalf("Failed to write to temp file: %v", err)
	}
	testFile.Close()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = calculateFileHash(testFile.Name())
	}
}
