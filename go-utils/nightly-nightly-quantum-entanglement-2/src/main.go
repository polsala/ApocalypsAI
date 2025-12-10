package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io"
	"os"
)

// calculateFileHash computes the SHA256 hash of a file
func calculateFileHash(filename string) (string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return "", fmt.Errorf("failed to open file %s: %w", filename, err)
	}
	defer file.Close()

	hash := sha256.New()
	if _, err := io.Copy(hash, file); err != nil {
		return "", fmt.Errorf("failed to read file %s: %w", filename, err)
	}

	return hex.EncodeToString(hash.Sum(nil)), nil
}

// checkQuantumEntanglement compares two file hashes
func checkQuantumEntanglement(file1, file2 string) (bool, string, string, error) {
	hash1, err := calculateFileHash(file1)
	if err != nil {
		return false, "", "", err
	}

	hash2, err := calculateFileHash(file2)
	if err != nil {
		return false, "", "", err
	}

	entangled := hash1 == hash2
	return entangled, hash1, hash2, nil
}

// formatHash displays hash with first 12 characters and ellipsis
func formatHash(hash string) string {
	if len(hash) > 12 {
		return hash[:12] + "..."
	}
	return hash
}

// printQuantumResult displays the whimsical quantum-themed results
func printQuantumResult(file1, file2 string, entangled bool, hash1, hash2 string) {
	fmt.Println("📄 File 1:", file1)
	fmt.Println("Hash:", formatHash(hash1))
	fmt.Println()
	fmt.Println("📄 File 2:", file2)
	fmt.Println("Hash:", formatHash(hash2))
	fmt.Println()
	fmt.Println("✨ Quantum Analysis Complete!")
	fmt.Println()
	
	if entangled {
		fmt.Println("🎯 Result: These files are QUANTUM ENTANGLED! 🪐")
		fmt.Println("💫 They share the same cosmic signature.")
	} else {
		fmt.Println("🌌 Result: These files are NOT quantum entangled.")
		fmt.Println("🌠 They have different cosmic signatures.")
	}
}

func main() {
	if len(os.Args) != 3 {
		fmt.Fprintf(os.Stderr, "Usage: %s <file1> <file2>\n", os.Args[0])
		os.Exit(1)
	}

	file1 := os.Args[1]
	file2 := os.Args[2]

	entangled, hash1, hash2, err := checkQuantumEntanglement(file1, file2)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

	printQuantumResult(file1, file2, entangled, hash1, hash2)
}
