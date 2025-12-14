package main

import (
	"os"
	"path/filepath"
	"testing"
)

// TestGenerateSignature tests the generateSignature function
func TestGenerateSignature(t *testing.T) {
	// Create a temporary test file
	tmpDir := t.TempDir()
	testFile := filepath.Join(tmpDir, "test.go")
	testContent := []byte("package main\nfunc test() {}")

	if err := os.WriteFile(testFile, testContent, 0644); err != nil {
		t.Fatalf("Failed to create test file: %v", err)
	}

	// Generate signature
	sig, err := generateSignature(testFile)
	if err != nil {
		t.Fatalf("generateSignature failed: %v", err)
	}

	// Verify signature properties
	if sig.FilePath != testFile {
		t.Errorf("Expected FilePath %s, got %s", testFile, sig.FilePath)
	}

	if len(sig.Signature) != 66 { // 0x + 64 hex chars
		t.Errorf("Expected signature length 66, got %d", len(sig.Signature))
	}

	if sig.QuantumBits <= 0 {
		t.Errorf("Expected positive quantum bits, got %d", sig.QuantumBits)
	}
}

// TestCountBits tests the countBits function
func TestCountBits(t *testing.T) {
	// Test with all zeros
	var zeros [32]byte
	if count := countBits(zeros); count != 0 {
		t.Errorf("Expected 0 bits for zeros, got %d", count)
	}

	// Test with all ones (0xFF = 8 bits)
	var ones [32]byte
	for i := range ones {
		ones[i] = 0xFF
	}
	expected := 32 * 8 // 256 bits
	if count := countBits(ones); count != expected {
		t.Errorf("Expected %d bits for all ones, got %d", expected, count)
	}

	// Test with mixed pattern
	pattern := [32]byte{0b10101010, 0b01010101}
	expected = 16 // 8 + 8
	if count := countBits(pattern); count != expected {
		t.Errorf("Expected %d bits for pattern, got %d", expected, count)
	}
}

// TestAreEntangled tests the areEntangled function
func TestAreEntangled(t *testing.T) {
	sig1 := QuantumSignature{Signature: "0x1234567890abcdef"}
	sig2 := QuantumSignature{Signature: "0x1234567890abcdef"}
	sig3 := QuantumSignature{Signature: "0xfedcba0987654321"}

	if !areEntangled(sig1, sig2) {
		t.Error("Expected sig1 and sig2 to be entangled")
	}

	if areEntangled(sig1, sig3) {
		t.Error("Expected sig1 and sig3 to not be entangled")
	}
}

// TestCheckEntanglement tests the checkEntanglement function
func TestCheckEntanglement(t *testing.T) {
	tmpDir := t.TempDir()

	// Create two identical files
	file1 := filepath.Join(tmpDir, "file1.go")
	file2 := filepath.Join(tmpDir, "file2.go")
	content := []byte("package main\nfunc test() {}")

	if err := os.WriteFile(file1, content, 0644); err != nil {
		t.Fatalf("Failed to create file1: %v", err)
	}

	if err := os.WriteFile(file2, content, 0644); err != nil {
		t.Fatalf("Failed to create file2: %v", err)
	}

	// Check entanglement (should not error)
	if err := checkEntanglement(file1, file2); err != nil {
		t.Errorf("checkEntanglement failed: %v", err)
	}
}

// TestPrintSignature tests the printSignature function
func TestPrintSignature(t *testing.T) {
	tmpDir := t.TempDir()
	testFile := filepath.Join(tmpDir, "test.go")
	testContent := []byte("package main\nfunc test() {}")

	if err := os.WriteFile(testFile, testContent, 0644); err != nil {
		t.Fatalf("Failed to create test file: %v", err)
	}

	// Print signature (should not error)
	if err := printSignature(testFile); err != nil {
		t.Errorf("printSignature failed: %v", err)
	}
}

// TestCompareSignatures tests the compareSignatures function
func TestCompareSignatures(t *testing.T) {
	tmpDir := t.TempDir()

	// Create two identical signature files
	sig1 := filepath.Join(tmpDir, "sig1.txt")
	sig2 := filepath.Join(tmpDir, "sig2.txt")
	sigContent := "0x1234567890abcdef"

	if err := os.WriteFile(sig1, []byte(sigContent), 0644); err != nil {
		t.Fatalf("Failed to create sig1: %v", err)
	}

	if err := os.WriteFile(sig2, []byte(sigContent), 0644); err != nil {
		t.Fatalf("Failed to create sig2: %v", err)
	}

	// Compare signatures (should not error)
	if err := compareSignatures(sig1, sig2); err != nil {
		t.Errorf("compareSignatures failed: %v", err)
	}
}

// BenchmarkGenerateSignature benchmarks the generateSignature function
func BenchmarkGenerateSignature(b *testing.B) {
	tmpDir := b.TempDir()
	testFile := filepath.Join(tmpDir, "test.go")
	testContent := make([]byte, 1024*1024) // 1MB of data

	if err := os.WriteFile(testFile, testContent, 0644); err != nil {
		b.Fatalf("Failed to create test file: %v", err)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, err := generateSignature(testFile)
		if err != nil {
			b.Fatalf("generateSignature failed: %v", err)
		}
	}
}

// BenchmarkCountBits benchmarks the countBits function
func BenchmarkCountBits(b *testing.B) {
	data := [32]byte{0b10101010, 0b01010101, 0b11110000, 0b00001111}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		countBits(data)
	}
}
