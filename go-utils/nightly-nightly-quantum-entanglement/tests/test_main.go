package main

import (
	"crypto/sha256"
	"encoding/hex"
	"io"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
)

// TestHashFile tests the concurrent file hashing functionality
func TestHashFile(t *testing.T) {
	// Create temporary test files
	tempDir, err := os.MkdirTemp("", "quantum_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tempDir)

	// Test file 1
	testFile1 := filepath.Join(tempDir, "test1.txt")
	content1 := "Hello, Quantum World!"
	if err := os.WriteFile(testFile1, []byte(content1), 0644); err != nil {
		t.Fatal(err)
	}

	// Test file 2 (identical content)
	testFile2 := filepath.Join(tempDir, "test2.txt")
	if err := os.WriteFile(testFile2, []byte(content1), 0644); err != nil {
		t.Fatal(err)
	}

	// Test file 3 (different content)
	testFile3 := filepath.Join(tempDir, "test3.txt")
	content3 := "Hello, Classical World!"
	if err := os.WriteFile(testFile3, []byte(content3), 0644); err != nil {
		t.Fatal(err)
	}

	// Test hashing identical files
	var wg sync.WaitGroup
	resultChan := make(chan QuantumFile, 2)

	wg.Add(2)
	go hashFile(testFile1, &wg, resultChan)
	go hashFile(testFile2, &wg, resultChan)

	wg.Wait()
	close(resultChan)

	var results []QuantumFile
	for result := range resultChan {
		results = append(results, result)
	}

	if len(results) != 2 {
		t.Errorf("Expected 2 results, got %d", len(results))
	}

	// Both files should exist and have the same hash
	for _, result := range results {
		if !result.Exists {
			t.Error("Expected file to exist")
		}
		if result.Hash == "" {
			t.Error("Expected non-empty hash")
		}
		if result.Size != int64(len(content1)) {
			t.Errorf("Expected size %d, got %d", len(content1), result.Size)
		}
	}

	// Check that hashes are identical
	if results[0].Hash != results[1].Hash {
		t.Error("Expected identical hashes for identical files")
	}
}

// TestCalculateEntanglementScore tests the entanglement calculation logic
func TestCalculateEntanglementScore(t *testing.T) {
	tests := []struct {
		name        string
		qf1, qf2    QuantumFile
		expScore    float64
		expEntangled bool
		expCoherence string
	}{
		{
			name: "Identical files",
			qf1: QuantumFile{
				Exists: true,
				Hash:   "abc123",
				Size:   100,
			},
			qf2: QuantumFile{
				Exists: true,
				Hash:   "abc123",
				Size:   100,
			},
			expScore:    100.0,
			expEntangled: true,
			expCoherence: "Perfect",
		},
		{
			name: "Different files, same size",
			qf1: QuantumFile{
				Exists: true,
				Hash:   "abc123",
				Size:   100,
			},
			qf2: QuantumFile{
				Exists: true,
				Hash:   "def456",
				Size:   100,
			},
			expScore:    60.0, // 50% size similarity + 10% quantum noise
			expEntangled: false,
			expCoherence: "High",
		},
		{
			name: "Different files, different sizes",
			qf1: QuantumFile{
				Exists: true,
				Hash:   "abc123",
				Size:   100,
			},
			qf2: QuantumFile{
				Exists: true,
				Hash:   "def456",
				Size:   200,
			},
			expScore:    35.0, // 25% size similarity + 10% quantum noise
			expEntangled: false,
			expCoherence: "Low",
		},
		{
			name: "One file doesn't exist",
			qf1: QuantumFile{
				Exists: false,
				Hash:   "",
				Size:   0,
			},
			qf2: QuantumFile{
				Exists: true,
				Hash:   "abc123",
				Size:   100,
			},
			expScore:    0.0,
			expEntangled: false,
			expCoherence: "Undefined",
		},
		{
			name: "Both files don't exist",
			qf1: QuantumFile{
				Exists: false,
				Hash:   "",
				Size:   0,
			},
			qf2: QuantumFile{
				Exists: false,
				Hash:   "",
				Size:   0,
			},
			expScore:    0.0,
			expEntangled: false,
			expCoherence: "Undefined",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			score, entangled, coherence := calculateEntanglementScore(tt.qf1, tt.qf2)
			
			if score != tt.expScore {
				t.Errorf("Expected score %.2f, got %.2f", tt.expScore, score)
			}
			if entangled != tt.expEntangled {
				t.Errorf("Expected entangled %v, got %v", tt.expEntangled, entangled)
			}
			if coherence != tt.expCoherence {
				t.Errorf("Expected coherence %s, got %s", tt.expCoherence, coherence)
			}
		})
	}
}

// TestFormatFileSize tests the file size formatting function
func TestFormatFileSize(t *testing.T) {
	tests := []struct {
		size     int64
		expected string
	}{
		{0, "0 B"},
		{512, "512 B"},
		{1024, "1.00 KB"},
		{1536, "1.50 KB"},
		{1048576, "1.00 MB"},
		{1572864, "1.50 MB"},
		{1073741824, "1.00 GB"},
	}

	for _, tt := range tests {
		result := formatFileSize(tt.size)
		if result != tt.expected {
			t.Errorf("Expected %s, got %s for size %d", tt.expected, result, tt.size)
		}
	}
}

// TestShortenHash tests the hash shortening function
func TestShortenHash(t *testing.T) {
	tests := []struct {
		hash     string
		expected string
	}{
		{"", ""},
		{"abc", "abc"},
		{"abcdef", "abcdef"},
		{"a1b2c3d4e5f6g7h8i9j0", "a1b2c3...g7h8i9j0"},
		{"0123456789abcdef0123456789abcdef0123456789abcdef", "012345...89abcdef"},
	}

	for _, tt := range tests {
		result := shortenHash(tt.hash)
		if result != tt.expected {
			t.Errorf("Expected %s, got %s for hash %s", tt.expected, result, tt.hash)
		}
	}
}

// TestValidateFiles tests file validation
func TestValidateFiles(t *testing.T) {
	// Create temporary directory and files
	tempDir, err := os.MkdirTemp("", "validate_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tempDir)

	// Create test files
	testFile1 := filepath.Join(tempDir, "test1.txt")
	testFile2 := filepath.Join(tempDir, "test2.txt")
	if err := os.WriteFile(testFile1, []byte("test"), 0644); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(testFile2, []byte("test"), 0644); err != nil {
		t.Fatal(err)
	}

	// Test valid files
	err = validateFiles(testFile1, testFile2)
	if err != nil {
		t.Errorf("Expected no error for valid files, got %v", err)
	}

	// Test non-existent file
	nonExistent := filepath.Join(tempDir, "nonexistent.txt")
	err = validateFiles(testFile1, nonExistent)
	if err == nil {
		t.Error("Expected error for non-existent file")
	} else if !strings.Contains(err.Error(), "does not exist") {
		t.Errorf("Expected 'does not exist' error, got %v", err)
	}
}

// BenchmarkHashFile benchmarks the concurrent file hashing
func BenchmarkHashFile(b *testing.B) {
	// Create a temporary file with test data
	tempDir, err := os.MkdirTemp("", "benchmark_test")
	if err != nil {
		b.Fatal(err)
	}
	defer os.RemoveAll(tempDir)

	// Create a 1MB test file
	testFile := filepath.Join(tempDir, "benchmark.txt")
	testData := make([]byte, 1024*1024) // 1MB
	for i := range testData {
		testData[i] = byte(i % 256)
	}
	if err := os.WriteFile(testFile, testData, 0644); err != nil {
		b.Fatal(err)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		var wg sync.WaitGroup
		resultChan := make(chan QuantumFile, 1)
		
		wg.Add(1)
		go hashFile(testFile, &wg, resultChan)
		
		wg.Wait()
		close(resultChan)
		
		<-resultChan // Consume the result
	}
}

// BenchmarkCalculateEntanglementScore benchmarks the entanglement calculation
func BenchmarkCalculateEntanglementScore(b *testing.B) {
	qf1 := QuantumFile{
		Exists: true,
		Hash:   "abc123def456",
		Size:   1024,
	}
	qf2 := QuantumFile{
		Exists: true,
		Hash:   "def456abc123",
		Size:   2048,
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		calculateEntanglementScore(qf1, qf2)
	}
}

// TestHashAccuracy tests that the hash function produces correct SHA-256 hashes
func TestHashAccuracy(t *testing.T) {
	// Create temporary test file
	tempDir, err := os.MkdirTemp("", "hash_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tempDir)

	testFile := filepath.Join(tempDir, "test.txt")
	testContent := "Quantum entanglement test content"
	if err := os.WriteFile(testFile, []byte(testContent), 0644); err != nil {
		t.Fatal(err)
	}

	// Compute expected hash manually
	expectedHasher := sha256.New()
	io.WriteString(expectedHasher, testContent)
	expectedHash := hex.EncodeToString(expectedHasher.Sum(nil))

	// Get hash from our function
	var wg sync.WaitGroup
	resultChan := make(chan QuantumFile, 1)
	
	wg.Add(1)
	go hashFile(testFile, &wg, resultChan)
	
	wg.Wait()
	close(resultChan)
	
	result := <-resultChan
	
	if result.Hash != expectedHash {
		t.Errorf("Expected hash %s, got %s", expectedHash, result.Hash)
	}
	
	if result.Size != int64(len(testContent)) {
		t.Errorf("Expected size %d, got %d", len(testContent), result.Size)
	}
}

// TestConcurrentHashingOrder tests that concurrent hashing works regardless of order
func TestConcurrentHashingOrder(t *testing.T) {
	// Create temporary directory
	tempDir, err := os.MkdirTemp("", "concurrent_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tempDir)

	// Create two identical files
	testFile1 := filepath.Join(tempDir, "test1.txt")
	testFile2 := filepath.Join(tempDir, "test2.txt")
	content := "Concurrent test content"
	if err := os.WriteFile(testFile1, []byte(content), 0644); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(testFile2, []byte(content), 0644); err != nil {
		t.Fatal(err)
	}

	// Run multiple times to test for race conditions
	for i := 0; i < 10; i++ {
		var wg sync.WaitGroup
		resultChan := make(chan QuantumFile, 2)
		
		wg.Add(2)
		go hashFile(testFile1, &wg, resultChan)
		go hashFile(testFile2, &wg, resultChan)
		
		wg.Wait()
		close(resultChan)
		
		var results []QuantumFile
		for result := range resultChan {
			results = append(results, result)
		}
		
		if len(results) != 2 {
			t.Errorf("Iteration %d: Expected 2 results, got %d", i+1, len(results))
			continue
		}
		
		// Both should have identical hashes
		if results[0].Hash != results[1].Hash {
			t.Errorf("Iteration %d: Expected identical hashes, got %s and %s", 
				i+1, results[0].Hash, results[1].Hash)
		}
	}
}
