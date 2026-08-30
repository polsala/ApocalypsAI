package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// SpectralEcho represents a detected spectral signal from the past.
type SpectralEcho struct {
	ID                 string
	Frequency          float64 // Simulated frequency in MHz
	Strength           float64 // Simulated strength (0.0 - 1.0)
	Location           string  // Whimsical location description
	EchoType           string  // e.g., "Data Stream", "Power Grid Hum", "Broadcast Relic"
	PotentialResources []string // e.g., "Servers", "Fuel", "Food", "Water"
}

// spectralMap holds all known spectral echoes.
var spectralMap = []SpectralEcho{
	{
		ID:        "ECHO-001",
		Frequency: 101.5,
		Strength:  0.85,
		Location:  "Old Library Sector A-7",
		EchoType:  "Data Stream",
		PotentialResources: []string{"Servers", "Archives", "Knowledge"},
	},
	{
		ID:        "ECHO-002",
		Frequency: 88.3,
		Strength:  0.30,
		Location:  "Forgotten Bunker 13",
		EchoType:  "Broadcast Relic",
		PotentialResources: []string{"Old Radios", "Emergency Broadcasts"},
	},
	{
		ID:        "ECHO-003",
		Frequency: 98.1,
		Strength:  0.72,
		Location:  "Abandoned Substation Gamma",
		EchoType:  "Power Grid Hum",
		PotentialResources: []string{"Fuel", "Generators", "Electrical Components"},
	},
	{
		ID:        "ECHO-004",
		Frequency: 109.9,
		Strength:  0.45,
		Location:  "Collapsed Internet Cafe 'The Byte'",
		EchoType:  "Data Stream",
		PotentialResources: []string{"Scrap Electronics", "Coffee Beans (stale)"},
	},
	{
		ID:        "ECHO-005",
		Frequency: 105.9,
		Strength:  0.91,
		Location:  "Crumbling Radio Tower Peak",
		EchoType:  "Broadcast Relic",
		PotentialResources: []string{"Communication Gear", "Antennas", "Information"},
	},
	{
		ID:        "ECHO-006",
		Frequency: 92.7,
		Strength:  0.60,
		Location:  "Flooded Server Farm Delta",
		EchoType:  "Data Stream",
		PotentialResources: []string{"Waterlogged Servers", "Rare Earth Metals"},
	},
}

// Scanner simulates scanning for spectral echoes.
type Scanner struct {
	spectralData []SpectralEcho
	minStrength  float64
}

// NewScanner creates a new Scanner with a given spectral map and minimum strength threshold.
func NewScanner(data []SpectralEcho, minStrength float64) *Scanner {
	return &Scanner{
		spectralData: data,
		minStrength:  minStrength,
	}
}

// Scan performs a simulated concurrent scan for echoes within a frequency range.
// It uses numWorkers goroutines to process the spectral data.
func (s *Scanner) Scan(minFreq, maxFreq float64, numWorkers int) []SpectralEcho {
	var detectedEchoes []SpectralEcho
	var mu sync.Mutex // Mutex to protect detectedEchoes slice
	var wg sync.WaitGroup

	if numWorkers <= 0 {
		return detectedEchoes // No workers, no scan
	}

	// Divide the spectral data among workers
	chunkSize := (len(s.spectralData) + numWorkers - 1) / numWorkers

	fmt.Printf("Scanning for spectral echoes between %.1f MHz and %.1f MHz with %d workers...\n", minFreq, maxFreq, numWorkers)

	for i := 0; i < numWorkers; i++ {
		start := i * chunkSize
		end := (i + 1) * chunkSize
		if end > len(s.spectralData) {
			end = len(s.spectralData)
		}

		if start >= end {
			continue // No data for this worker
		}

		wg.Add(1)
		go func(workerID int, chunk []SpectralEcho) {
			defer wg.Done()
			// fmt.Printf("Worker %d processing %d echoes.\n", workerID, len(chunk))
			for _, echo := range chunk {
				if echo.Frequency >= minFreq && echo.Frequency <= maxFreq && echo.Strength >= s.minStrength {
					// Simulate some processing time
					time.Sleep(time.Duration(rand.Intn(50)+10) * time.Millisecond)
					mu.Lock()
					detectedEchoes = append(detectedEchoes, echo)
					mu.Unlock()
				}
			}
		}(i, s.spectralData[start:end])
	}

	wg.Wait()
	return detectedEchoes
}

func main() {
	rand.Seed(time.Now().UnixNano())

	scanner := NewScanner(spectralMap, 0.5) // Minimum strength threshold of 0.5

	// Perform a scan across a common FM radio frequency range
	detected := scanner.Scan(88.0, 108.0, 3) // Scan from 88.0 MHz to 108.0 MHz with 3 concurrent workers

	fmt.Println("\nDetected Spectral Echoes:")
	fmt.Println("-------------------------")
	if len(detected) == 0 {
		fmt.Println("No significant spectral echoes detected in this range.")
	} else {
		// Sorting for consistent output in main, though not strictly required for functionality.
		// For testing, this would be done in the test function itself.
		// sort.Slice(detected, func(i, j int) bool {
		// 	return detected[i].Strength > detected[j].Strength
		// })

		for _, echo := range detected {
			fmt.Printf("ID: %s\n", echo.ID)
			fmt.Printf("  Frequency: %.1f MHz, Strength: %.2f\n", echo.Frequency, echo.Strength)
			fmt.Printf("  Type: %s\n", echo.EchoType)
			fmt.Printf("  Location: %s\n", echo.Location)
			fmt.Printf("  Potential Resources: %v\n\n", echo.PotentialResources)
		}
	}
	fmt.Println("-------------------------")
	fmt.Println("Scan complete. May your journey be fruitful!")
}
