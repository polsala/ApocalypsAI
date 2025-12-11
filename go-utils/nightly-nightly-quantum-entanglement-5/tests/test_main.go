package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

// createTestFile creates a temporary test file with given content
func createTestFile(t *testing.T, content string) string {
	file, err := os.CreateTemp("", "qec-test-*.txt")
	if err != nil {
		t.Fatalf("Failed to create temp file: %v", err)
	}
	defer file.Close()

	_, err = file.WriteString(content)
	if err != nil {
		t.Fatalf("Failed to write to temp file: %v", err)
	}

	return file.Name()
}

// cleanupTestFile removes a test file
func cleanupTestFile(t *testing.T, filename string) {
	err := os.Remove(filename)
	if err != nil {
		t.Logf("Warning: Failed to remove temp file %s: %v", filename, err)
	}
}

func TestCalculateHash(t *testing.T) {
	// Test with known content
	content := "Hello, Quantum World!"
	expectedHash := sha256.Sum256([]byte(content))
	expectedHashStr := hex.EncodeToString(expectedHash[:])

	// Create test file
	testFile := createTestFile(t, content)
	defer cleanupTestFile(t, testFile)

	// Calculate hash
	hash, err := calculateHash(testFile)
	if err != nil {
		t.Errorf("calculateHash failed: %v", err)
	}

	// Verify hash
	if hash != expectedHashStr {
		t.Errorf("Hash mismatch. Expected: %s, Got: %s", expectedHashStr, hash)
	}
}

func TestGetFileInfo(t *testing.T) {
	// Test with existing file
	content := "Test content for quantum state"
	testFile := createTestFile(t, content)
	defer cleanupTestFile(t, testFile)

	state, err := getFileInfo(testFile)
	if err != nil {
		t.Errorf("getFileInfo failed: %v", err)
	}

	// Verify state
	if !state.Exists {
		t.Error("Expected file to exist")
	}

	if state.Size != int64(len(content)) {
		t.Errorf("Size mismatch. Expected: %d, Got: %d", len(content), state.Size)
	}

	if state.Hash == "" {
		t.Error("Expected hash to be calculated")
	}

	// Test with non-existing file
	nonExistentFile := "this-file-does-not-exist-quantumly.txt"
	state2, err := getFileInfo(nonExistentFile)
	if err != nil {
		t.Errorf("getFileInfo should not return error for non-existent file: %v", err)
	}

	if state2.Exists {
		t.Error("Expected file to not exist")
	}

	if state2.Hash != "" {
		t.Error("Expected empty hash for non-existent file")
	}
}

func TestCheckQuantumEntanglement_SameFiles(t *testing.T) {
	// Create two identical files
	content := "Quantum entanglement test content"
	file1 := createTestFile(t, content)
	file2 := createTestFile(t, content)
	defer cleanupTestFile(t, file1)
	defer cleanupTestFile(t, file2)

	result, err := checkQuantumEntanglement(file1, file2)
	if err != nil {
		t.Errorf("checkQuantumEntanglement failed: %v", err)
	}

	// Verify entanglement
	if !result.AreEntangled {
		t.Error("Expected files to be entangled")
	}

	if result.Probability != 99.9 {
		t.Errorf("Expected probability 99.9, got %f", result.Probability)
	}

	if !result.IsParallelUniverse {
		t.Error("Expected parallel universe detection (different paths)")
	}

	// Verify hashes are identical
	if result.File1.Hash != result.File2.Hash {
		t.Error("Expected identical hashes")
	}
}

func TestCheckQuantumEntanglement_DifferentFiles(t *testing.T) {
	// Create two different files
	file1 := createTestFile(t, "Content A")
	file2 := createTestFile(t, "Content B")
	defer cleanupTestFile(t, file1)
	defer cleanupTestFile(t, file2)

	result, err := checkQuantumEntanglement(file1, file2)
	if err != nil {
		t.Errorf("checkQuantumEntanglement failed: %v", err)
	}

	// Verify no entanglement
	if result.AreEntangled {
		t.Error("Expected files to NOT be entangled")
	}

	if result.Probability != 0.0 {
		t.Errorf("Expected probability 0.0, got %f", result.Probability)
	}

	if !result.IsParallelUniverse {
		t.Error("Expected parallel universe detection (different paths)")
	}

	// Verify hashes are different
	if result.File1.Hash == result.File2.Hash {
		t.Error("Expected different hashes")
	}
}

func TestCheckQuantumEntanglement_OneNonExistent(t *testing.T) {
	// Create one existing file and one non-existent
	content := "Existing file content"
	file1 := createTestFile(t, content)
	file2 := "non-existent-file.txt"
	defer cleanupTestFile(t, file1)

	result, err := checkQuantumEntanglement(file1, file2)
	if err != nil {
		t.Errorf("checkQuantumEntanglement failed: %v", err)
	}

	// Verify no entanglement
	if result.AreEntangled {
		t.Error("Expected no entanglement with non-existent file")
	}

	if result.Probability != 0.0 {
		t.Errorf("Expected probability 0.0, got %f", result.Probability)
	}

	// Verify file states
	if !result.File1.Exists {
		t.Error("Expected file1 to exist")
	}

	if result.File2.Exists {
		t.Error("Expected file2 to not exist")
	}
}

func TestCheckQuantumEntanglement_BothNonExistent(t *testing.T) {
	// Test with two non-existent files
	file1 := "non-existent-file-1.txt"
	file2 := "non-existent-file-2.txt"

	result, err := checkQuantumEntanglement(file1, file2)
	if err != nil {
		t.Errorf("checkQuantumEntanglement failed: %v", err)
	}

	// Verify no entanglement
	if result.AreEntangled {
		t.Error("Expected no entanglement with non-existent files")
	}

	if result.Probability != 0.0 {
		t.Errorf("Expected probability 0.0, got %f", result.Probability)
	}

	// Verify file states
	if result.File1.Exists {
		t.Error("Expected file1 to not exist")
	}

	if result.File2.Exists {
		t.Error("Expected file2 to not exist")
	}
}

func TestCheckQuantumEntanglement_SamePath(t *testing.T) {
	// Test with same file path (same quantum coordinate)
	content := "Same file, same universe"
	testFile := createTestFile(t, content)
	defer cleanupTestFile(t, testFile)

	result, err := checkQuantumEntanglement(testFile, testFile)
	if err != nil {
		t.Errorf("checkQuantumEntanglement failed: %v", err)
	}

	// Verify entanglement
	if !result.AreEntangled {
		t.Error("Expected file to be entangled with itself")
	}

	if result.Probability != 99.9 {
		t.Errorf("Expected probability 99.9, got %f", result.Probability)
	}

	// Should NOT be parallel universe (same path)
	if result.IsParallelUniverse {
		t.Error("Expected same universe for same file path")
	}
}

func TestGetQuantumQuote(t *testing.T) {
	// Test with entangled result
	entangledResult := QuantumEntanglementResult{
		AreEntangled: true,
	}

	quote := getQuantumQuote(entangledResult)
	if quote == "" {
		t.Error("Expected non-empty quote for entangled result")
	}

	// Verify quote contains expected content
	entangledQuotes := []string{
		"Spooky action at a distance confirmed.",
		"If you think you understand quantum mechanics, you don't understand quantum mechanics.",
		"The universe is full of magical things, patiently waiting for our wits to grow sharper.",
		"Quantum mechanics is magic.",
	}

	quoteFound := false
	for _, expectedQuote := range entangledQuotes {
		if strings.Contains(quote, expectedQuote) {
			quoteFound = true
			break
		}
	}
	if !quoteFound {
		t.Errorf("Unexpected quote for entangled result: %s", quote)
	}

	// Test with non-entangled result
	nonEntangledResult := QuantumEntanglementResult{
		AreEntangled: false,
	}

	quote2 := getQuantumQuote(nonEntangledResult)
	if quote2 == "" {
		t.Error("Expected non-empty quote for non-entangled result")
	}

	nonEntangledQuotes := []string{
		"Not everything that is faced can be changed",
		"The best way to predict the future is to create it.",
		"Reality is merely an illusion",
		"The universe is not only stranger than we imagine",
	}

	quoteFound2 := false
	for _, expectedQuote := range nonEntangledQuotes {
		if strings.Contains(quote2, expectedQuote) {
			quoteFound2 = true
			break
		}
	}
	if !quoteFound2 {
		t.Errorf("Unexpected quote for non-entangled result: %s", quote2)
	}
}

func TestFormatFileSize(t *testing.T) {
	tests := []struct {
		size     int64
		expected string
	}{
		{0, "0 B"},
		{100, "100 B"},
		{1024, "1.00 KB"},
		{1536, "1.50 KB"},
		{1024 * 1024, "1.00 MB"},
		{1536 * 1024, "1.50 MB"},
		{1024 * 1024 * 1024, "1.00 GB"},
	}

	for _, test := range tests {
		result := formatFileSize(test.size)
		if result != test.expected {
			t.Errorf("formatFileSize(%d) = %s, expected %s", test.size, result, test.expected)
		}
	}
}

func TestMainIntegration(t *testing.T) {
	// This test simulates the main function behavior
	// by capturing stdout and checking the output format

	// Create test files
	content := "Integration test content"
	file1 := createTestFile(t, content)
	file2 := createTestFile(t, content)
	defer cleanupTestFile(t, file1)
	defer cleanupTestFile(t, file2)

	// Capture stdout
	originalStdout := os.Stdout
r, w, _ := os.Pipe()
	os.Stdout = w

	// Redirect stderr to stdout for capture
	originalStderr := os.Stderr
	os.Stderr = w

	// Run the entanglement check (simulate main logic)
	result, err := checkQuantumEntanglement(file1, file2)
	if err != nil {
		t.Errorf("Integration test failed: %v", err)
	}

	// Restore stdout/stderr
	w.Close()
	os.Stdout = originalStdout
	os.Stderr = originalStderr

	// Read captured output
	output, _ := io.ReadAll(rr)
	rr.Close()

	outputStr := string(output)

	// Verify output contains expected elements
	expectedElements := []string{
		"🌌 Quantum Entanglement Checker 🌌",
		"File 1:",
		"File 2:",
		"Quantum State Analysis:",
		"Hash 1:",
		"Hash 2:",
		"🎯 Entanglement Probability: 99.9%",
		"✨ These files are quantum-entangled!",
	}

	for _, element := range expectedElements {
		if !strings.Contains(outputStr, element) {
			t.Errorf("Output missing expected element: %s\nFull output: %s", element, outputStr)
		}
	}

	// Verify result is correct
	if !result.AreEntangled {
		t.Error("Integration test: Expected entanglement")
	}
	if result.Probability != 99.9 {
		t.Errorf("Integration test: Expected probability 99.9, got %f", result.Probability)
	}
}

func BenchmarkCalculateHash(b *testing.B) {
	// Create a large test file
	content := make([]byte, 1024*1024) // 1MB
	for i := range content {
		content[i] = byte(i % 256)
	}
	testFile := createTestFile(&testing.T{}, string(content))
	defer cleanupTestFile(&testing.T{}, testFile)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, err := calculateHash(testFile)
		if err != nil {
			b.Fatal(err)
		}
	}
}

func BenchmarkCheckQuantumEntanglement(b *testing.B) {
	// Create test files
	content := "Benchmark test content for quantum entanglement"
	file1 := createTestFile(&testing.T{}, content)
	file2 := createTestFile(&testing.T{}, content)
	defer cleanupTestFile(&testing.T{}, file1)
	defer cleanupTestFile(&testing.T{}, file2)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, err := checkQuantumEntanglement(file1, file2)
		if err != nil {
			b.Fatal(err)
		}
	}
}
