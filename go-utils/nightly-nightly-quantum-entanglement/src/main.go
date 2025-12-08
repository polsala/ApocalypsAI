package main

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

// QuantumFile represents a file with quantum properties
type QuantumFile struct {
	Path       string
	Size       int64
	Hash       string
	Exists     bool
	State      string
	WaveFunc   string
}

// QuantumEntanglementResult represents the entanglement analysis
type QuantumEntanglementResult struct {
	File1              QuantumFile
	File2              QuantumFile
	EntanglementScore  float64
	IsEntangled        bool
	CoherenceLevel     string
}

// hashFile concurrently computes the SHA-256 hash of a file
func hashFile(filePath string, wg *sync.WaitGroup, resultChan chan<- QuantumFile) {
	defer wg.Done()

	qf := QuantumFile{
		Path:   filePath,
		Exists: false,
	}

	file, err := os.Open(filePath)
	if err != nil {
		resultChan <- qf
		return
	}
	defer file.Close()

	// Get file info
	info, err := file.Stat()
	if err != nil {
		resultChan <- qf
		return
	}

	qf.Exists = true
	qf.Size = info.Size()

	// Compute hash
	hasher := sha256.New()
	if _, err := io.Copy(hasher, file); err != nil {
		resultChan <- qf
		return
	}

	qf.Hash = hex.EncodeToString(hasher.Sum(nil))
	qf.State = "Collapsed (Classical)"
	qf.WaveFunc = "Stable"

	resultChan <- qf
}

// calculateEntanglementScore calculates the entanglement probability
func calculateEntanglementScore(qf1, qf2 QuantumFile) (float64, bool, string) {
	if !qf1.Exists || !qf2.Exists {
		return 0.0, false, "Undefined"
	}

	if qf1.Hash == qf2.Hash {
		return 100.0, true, "Perfect"
	}

	// Calculate similarity based on size difference
	var larger, smaller int64
	if qf1.Size > qf2.Size {
		larger, smaller = qf1.Size, qf2.Size
	} else {
		larger, smaller = qf2.Size, qf1.Size
	}

	if larger == 0 {
		return 0.0, false, "No Coherence"
	}

	diffRatio := float64(larger-smaller) / float64(larger)
	similarity := (1.0 - diffRatio) * 50.0 // Max 50% for size similarity

	// Add some "quantum noise" for hash difference
	similarity += 10.0 // Base quantum uncertainty

	coherence := "Low"
	if similarity > 75.0 {
		coherence = "High"
	} else if similarity > 50.0 {
		coherence = "Medium"
	}

	return similarity, false, coherence
}

// formatFileSize formats file size in human-readable format
func formatFileSize(size int64) string {
	const (
		KB = 1 << 10
		MB = 1 << 20
		GB = 1 << 30
	)

	if size < KB {
		return fmt.Sprintf("%d B", size)
	} else if size < MB {
		return fmt.Sprintf("%.2f KB", float64(size)/KB)
	} else if size < GB {
		return fmt.Sprintf("%.2f MB", float64(size)/MB)
	}
	return fmt.Sprintf("%.2f GB", float64(size)/GB)
}

// printHeader prints the quantum analysis header
func printHeader() {
	fmt.Println("🔬 Quantum Entanglement Analysis Report 🔬")
	fmt.Println("=" + strings.Repeat("=", 48))
	fmt.Println()
}

// printFileAnalysis prints the analysis for a single file
func printFileAnalysis(qf QuantumFile) {
	filename := filepath.Base(qf.Path)
	fmt.Printf("File: %s\n", filename)
	
	if !qf.Exists {
		fmt.Printf("  📄 Schrödinger State: Non-existent (Quantum Void)\n")
		fmt.Printf("  🔗 Quantum Signature: Unavailable\n")
		fmt.Printf("  ⚖️  Wave Function: Collapsed\n")
	} else {
		fmt.Printf("  📄 Schrödinger State: %s\n", qf.State)
		fmt.Printf("  🔗 Quantum Signature: %s\n", shortenHash(qf.Hash))
		fmt.Printf("  ⚖️  Wave Function: %s\n", qf.WaveFunc)
		fmt.Printf("  📏 File Size: %s\n", formatFileSize(qf.Size))
	}
	fmt.Println()
}

// printEntanglementAnalysis prints the entanglement analysis
func printEntanglementAnalysis(result QuantumEntanglementResult) {
	fmt.Println("🔬 Entanglement Analysis:")
	fmt.Printf("  🌀 Quantum Correlation: %.2f%%\n", result.EntanglementScore)
	
	if result.IsEntangled {
		fmt.Printf("  🌀 Entanglement Status: ✨ QUANTUM ENTANGLEMENT DETECTED ✨\n")
	} else {
		fmt.Printf("  🌀 Entanglement Status: No Entanglement Detected\n")
	}
	
	fmt.Printf("  🌀 Coherence Level: %s\n", result.CoherenceLevel)
	fmt.Println()
}

// printInterpretation prints the quantum interpretation
func printInterpretation(result QuantumEntanglementResult) {
	fmt.Println("💡 Interpretation:")
	
	if result.IsEntangled {
		fmt.Println("  These files exist in a perfectly entangled quantum state.")
		fmt.Println("  Any measurement on one will instantaneously affect the other!")
		fmt.Println("  Spooky action at a distance confirmed! 👻")
	} else {
		if result.EntanglementScore > 50 {
			fmt.Println("  These files show partial quantum correlation.")
			fmt.Println("  They may share some quantum properties but are not fully entangled.")
		} else {
			fmt.Println("  These files appear to be in separate quantum states.")
			fmt.Println("  No significant quantum correlation detected.")
		}
	}
	fmt.Println()
}

// shortenHash shortens a hash for display purposes
func shortenHash(hash string) string {
	if len(hash) > 12 {
		return hash[:6] + "..." + hash[len(hash)-6:]
	}
	return hash
}

// validateFiles validates that files exist and are readable
func validateFiles(path1, path2 string) error {
	for i, path := range []string{path1, path2} {
		if _, err := os.Stat(path); os.IsNotExist(err) {
			return fmt.Errorf("file %d (%s) does not exist", i+1, path)
		} else if err != nil {
			return fmt.Errorf("cannot access file %d (%s): %v", i+1, path, err)
		}
	}
	return nil
}

func main() {
	// Check command line arguments
	if len(os.Args) != 3 {
		fmt.Println("Usage: quantum-entanglement-checker <file1> <file2>")
		fmt.Println()
		fmt.Println("Example:")
		fmt.Println("  quantum-entanglement-checker file1.txt file2.txt")
		os.Exit(1)
	}

	file1 := os.Args[1]
	file2 := os.Args[2]

	// Validate files
	if err := validateFiles(file1, file2); err != nil {
		fmt.Printf("❌ Validation Error: %v\n", err)
		os.Exit(1)
	}

	// Print header
	printHeader()

	// Perform concurrent hashing
	var wg sync.WaitGroup
	resultChan := make(chan QuantumFile, 2)

	wg.Add(2)
	go hashFile(file1, &wg, resultChan)
	go hashFile(file2, &wg, resultChan)

	// Wait for completion
	wg.Wait()
	close(resultChan)

	// Collect results
	var qf1, qf2 QuantumFile
	for result := range resultChan {
		if result.Path == file1 {
			qf1 = result
		} else {
			qf2 = result
		}
	}

	// Print file analyses
	printFileAnalysis(qf1)
	printFileAnalysis(qf2)

	// Calculate entanglement
	entanglementScore, isEntangled, coherenceLevel := calculateEntanglementScore(qf1, qf2)
	result := QuantumEntanglementResult{
		File1:             qf1,
		File2:             qf2,
		EntanglementScore: entanglementScore,
		IsEntangled:       isEntangled,
		CoherenceLevel:    coherenceLevel,
	}

	// Print entanglement analysis
	printEntanglementAnalysis(result)

	// Print interpretation
	printInterpretation(result)

	// Print footer with timestamp
	fmt.Printf("⏱️  Analysis completed at %s\n", time.Now().Format("2006-01-02 15:04:05"))
	fmt.Println()
	fmt.Println("🌌 Remember: All measurements are relative to the observer's frame of reference.")
}
