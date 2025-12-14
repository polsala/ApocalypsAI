package main

import (
	"crypto/sha256"
	"encoding/hex"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// QuantumSignature represents a quantum signature for a code snippet
type QuantumSignature struct {
	FilePath    string
	Signature   string
	Timestamp   time.Time
	QuantumBits int
}

// String returns a formatted string representation
func (q QuantumSignature) String() string {
	return fmt.Sprintf("🌀 Quantum Signature for %s\n"+
		"Signature: %s\n"+
		"Timestamp: %s\n"+
		"Quantum Bits: %d\n",
		path.Base(q.FilePath), q.Signature, q.Timestamp.Format(time.RFC3339), q.QuantumBits)
}

// generateSignature generates a quantum signature for a file
func generateSignature(filePath string) (QuantumSignature, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return QuantumSignature{}, fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	// Read file content
	content, err := io.ReadAll(file)
	if err != nil {
		return QuantumSignature{}, fmt.Errorf("failed to read file: %w", err)
	}

	// Generate SHA256 hash
	hash := sha256.Sum256(content)
	hashStr := "0x" + hex.EncodeToString(hash[:])

	// Count quantum bits (number of 1s in the hash)
	quantumBits := countBits(hash)

	return QuantumSignature{
		FilePath:    filePath,
		Signature:   hashStr,
		Timestamp:   time.Now(),
		QuantumBits: quantumBits,
	}, nil
}

// countBits counts the number of 1s in a byte array
func countBits(data [32]byte) int {
	count := 0
	for _, b := range data {
		for b != 0 {
			count += int(b & 1)
			b >>= 1
		}
	}
	return count
}

// areEntangled checks if two signatures are entangled
func areEntangled(sig1, sig2 QuantumSignature) bool {
	return sig1.Signature == sig2.Signature
}

// checkEntanglement checks if two files are quantum entangled
func checkEntanglement(file1, file2 string) error {
	var wg sync.WaitGroup
	var sig1, sig2 QuantumSignature
	var err1, err2 error

	wg.Add(2)

	// Generate signatures concurrently
	go func() {
		defer wg.Done()
		sig1, err1 = generateSignature(file1)
	}()

	go func() {
		defer wg.Done()
		sig2, err2 = generateSignature(file2)
	}()

	wg.Wait()

	if err1 != nil {
		return fmt.Errorf("failed to generate signature for %s: %w", file1, err1)
	}
	if err2 != nil {
		return fmt.Errorf("failed to generate signature for %s: %w", file2, err2)
	}

	// Print signatures
	fmt.Println(sig1)
	fmt.Println(sig2)

	// Check entanglement
	if areEntangled(sig1, sig2) {
		fmt.Println("🎉 These files are quantum entangled!")
	} else {
		fmt.Println("🌌 These files are not quantum entangled.")
		fmt.Println("💡 Try running them through the quantum tunnel again!")
	}

	return nil
}

// printSignature prints the quantum signature for a file
func printSignature(filePath string) error {
	sig, err := generateSignature(filePath)
	if err != nil {
		return err
	}
	fmt.Println(sig)
	return nil
}

// compareSignatures compares two signature files
func compareSignatures(sig1Path, sig2Path string) error {
	// Read signature files
	sig1Content, err := os.ReadFile(sig1Path)
	if err != nil {
		return fmt.Errorf("failed to read signature file %s: %w", sig1Path, err)
	}

	sig2Content, err := os.ReadFile(sig2Path)
	if err != nil {
		return fmt.Errorf("failed to read signature file %s: %w", sig2Path, err)
	}

	// Compare signatures
	if string(sig1Content) == string(sig2Content) {
		fmt.Println("🎉 The signatures are quantum entangled!")
	} else {
		fmt.Println("🌌 The signatures are not quantum entangled.")
		fmt.Println("💡 Try running them through the quantum tunnel again!")
	}

	return nil
}

func main() {
	// Define command line flags
	checkCmd := flag.NewFlagSet("check", flag.ExitOnError)
	checkFile1 := checkCmd.String("file1", "", "First file to check")
	checkFile2 := checkCmd.String("file2", "", "Second file to check")

	sigCmd := flag.NewFlagSet("signature", flag.ExitOnError)
	sigFile := sigCmd.String("file", "", "File to generate signature for")

	cmpCmd := flag.NewFlagSet("compare", flag.ExitOnError)
	cmpSig1 := cmpCmd.String("sig1", "", "First signature file")
	cmpSig2 := cmpCmd.String("sig2", "", "Second signature file")

	// Check if no arguments provided
	if len(os.Args) < 2 {
		fmt.Println("Usage:")
		fmt.Println("  qec check --file1 <file1> --file2 <file2>")
		fmt.Println("  qec signature --file <file>")
		fmt.Println("  qec compare --sig1 <sig1> --sig2 <sig2>")
		fmt.Println("\nFor more information, run qec --help")
		return
	}

	// Parse subcommand
	switch os.Args[1] {
	case "check":
		checkCmd.Parse(os.Args[2:])
		if *checkFile1 == "" || *checkFile2 == "" {
			checkCmd.Usage()
			return
		}
		if err := checkEntanglement(*checkFile1, *checkFile2); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "signature":
		sigCmd.Parse(os.Args[2:])
		if *sigFile == "" {
			sigCmd.Usage()
			return
		}
		if err := printSignature(*sigFile); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "compare":
		cmpCmd.Parse(os.Args[2:])
		if *cmpSig1 == "" || *cmpSig2 == "" {
			cmpCmd.Usage()
			return
		}
		if err := compareSignatures(*cmpSig1, *cmpSig2); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	default:
		fmt.Fprintf(os.Stderr, "Unknown command: %s\n", os.Args[1])
		fmt.Println("Available commands: check, signature, compare")
		os.Exit(1)
	}
}
