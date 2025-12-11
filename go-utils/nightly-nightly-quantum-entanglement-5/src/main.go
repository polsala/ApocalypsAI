package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// QuantumState represents the quantum state of a file
type QuantumState struct {
	Path        string
	Hash        string
	Exists      bool
	Size        int64
	LastModified time.Time
}

// QuantumEntanglementResult represents the result of entanglement check
type QuantumEntanglementResult struct {
	File1              QuantumState
	File2              QuantumState
	AreEntangled       bool
	EntanglementLevel  float64
	IsParallelUniverse bool
	Probability        float64
}

// calculateHash calculates SHA-256 hash of a file
func calculateHash(filePath string) (string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return "", err
	}
	defer file.Close()

	hash := sha256.New()
	if _, err := io.Copy(hash, file); err != nil {
		return "", err
	}

	return hex.EncodeToString(hash.Sum(nil)), nil
}

// getFileInfo gets file information for quantum state
func getFileInfo(filePath string) (QuantumState, error) {
	state := QuantumState{Path: filePath}

	info, err := os.Stat(filePath)
	if err != nil {
		if os.IsNotExist(err) {
			state.Exists = false
			return state, nil
		}
		return state, err
	}

	state.Exists = true
	state.Size = info.Size()
	state.LastModified = info.ModTime()

	hash, err := calculateHash(filePath)
	if err != nil {
		return state, err
	}
	state.Hash = hash

	return state, nil
}

// checkQuantumEntanglement checks if two files are quantum-entangled
func checkQuantumEntanglement(file1, file2 string) (QuantumEntanglementResult, error) {
	result := QuantumEntanglementResult{}

	// Get quantum states
	state1, err := getFileInfo(file1)
	if err != nil {
		return result, fmt.Errorf("failed to get info for file1: %w", err)
	}
	result.File1 = state1

	state2, err := getFileInfo(file2)
	if err != nil {
		return result, fmt.Errorf("failed to get info for file2: %w", err)
	}
	result.File2 = state2

	// Check if both files exist
	if !state1.Exists || !state2.Exists {
		result.AreEntangled = false
		result.Probability = 0.0
		return result, nil
	}

	// Check if hashes are identical (quantum entanglement)
	result.AreEntangled = state1.Hash == state2.Hash
	
	// Calculate entanglement probability (99.9% for identical, 0% for different)
	if result.AreEntangled {
		result.Probability = 99.9
		result.EntanglementLevel = 1.0
	} else {
		result.Probability = 0.0
		result.EntanglementLevel = 0.0
	}

	// Check if files are in parallel universes (different paths)
	normalizedPath1 := filepath.ToSlash(state1.Path)
	normalizedPath2 := filepath.ToSlash(state2.Path)
	result.IsParallelUniverse = normalizedPath1 != normalizedPath2

	return result, nil
}

// getQuantumQuote returns a whimsical quantum physics quote based on result
func getQuantumQuote(result QuantumEntanglementResult) string {
	quotes := map[bool][]string{
		true: {
			"\"Spooky action at a distance confirmed.\" - Einstein",
			"\"If you think you understand quantum mechanics, you don't understand quantum mechanics.\" - Feynman",
			"\"The universe is full of magical things, patiently waiting for our wits to grow sharper.\" - Eden Phillpotts",
			"\"Quantum mechanics is magic.\" - Daniel Greenberger",
		},
		false: {
			"\"Not everything that is faced can be changed, but nothing can be changed until it is faced.\" - James Baldwin",
			"\"The best way to predict the future is to create it.\" - Peter Drucker",
			"\"Reality is merely an illusion, albeit a very persistent one.\" - Einstein",
			"\"The universe is not only stranger than we imagine, it is stranger than we can imagine.\" - Haldane",
		},
	}

	selectedQuotes := quotes[result.AreEntangled]
	index := int(time.Now().UnixNano()) % len(selectedQuotes)
	return selectedQuotes[index]
}

// formatFileSize formats file size in human-readable format
func formatFileSize(size int64) string {
	if size < 1024 {
		return fmt.Sprintf("%d B", size)
	} else if size < 1024*1024 {
		return fmt.Sprintf("%.2f KB", float64(size)/1024)
	} else if size < 1024*1024*1024 {
		return fmt.Sprintf("%.2f MB", float64(size)/(1024*1024))
	}
	return fmt.Sprintf("%.2f GB", float64(size)/(1024*1024*1024))
}

// printResult prints the quantum entanglement result
func printResult(result QuantumEntanglementResult) {
	fmt.Println("🌌 Quantum Entanglement Checker 🌌")
	fmt.Println()
	fmt.Printf("File 1: %s\n", result.File1.Path)
	fmt.Printf("File 2: %s\n", result.File2.Path)
	fmt.Println()
	fmt.Println("Quantum State Analysis:")
	
	// File 1 info
	if result.File1.Exists {
		fmt.Printf("  Hash 1: %s\n", result.File1.Hash)
		fmt.Printf("  Size 1: %s\n", formatFileSize(result.File1.Size))
		fmt.Printf("  Last Modified 1: %s\n", result.File1.LastModified.Format("2006-01-02 15:04:05"))
	} else {
		fmt.Println("  File 1: Does not exist")
	}
	
	// File 2 info
	if result.File2.Exists {
		fmt.Printf("  Hash 2: %s\n", result.File2.Hash)
		fmt.Printf("  Size 2: %s\n", formatFileSize(result.File2.Size))
		fmt.Printf("  Last Modified 2: %s\n", result.File2.LastModified.Format("2006-01-02 15:04:05"))
	} else {
		fmt.Println("  File 2: Does not exist")
	}
	
	fmt.Println()
	fmt.Printf("🎯 Entanglement Probability: %.1f%%\n", result.Probability)
	
	if result.AreEntangled {
		if result.IsParallelUniverse {
			fmt.Println("✨ These files are quantum-entangled across parallel universes!")
		} else {
			fmt.Println("✨ These files are quantum-entangled!")
		}
	} else {
		fmt.Println("❌ These files are not quantum-entangled.")
		if result.IsParallelUniverse {
			fmt.Println("   They exist in different quantum coordinates (parallel universes).")
		}
	}
	
	fmt.Println()
	fmt.Println(getQuantumQuote(result))
}

func main() {
	// Check command line arguments
	if len(os.Args) != 3 {
		fmt.Println("Usage: qec <file1> <file2>")
		fmt.Println("Example: qec src/main.go src/backup.go")
		os.Exit(1)
	}

	file1 := os.Args[1]
	file2 := os.Args[2]

	// Check if files exist
	if _, err := os.Stat(file1); os.IsNotExist(err) {
		fmt.Printf("Error: File '%s' does not exist\n", file1)
		os.Exit(1)
	}

	if _, err := os.Stat(file2); os.IsNotExist(err) {
		fmt.Printf("Error: File '%s' does not exist\n", file2)
		os.Exit(1)
	}

	// Check quantum entanglement
	result, err := checkQuantumEntanglement(file1, file2)
	if err != nil {
		fmt.Printf("Error checking quantum entanglement: %v\n", err)
		os.Exit(1)
	}

	// Print result
	printResult(result)
}
