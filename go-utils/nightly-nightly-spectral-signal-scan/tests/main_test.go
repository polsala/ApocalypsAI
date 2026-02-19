package main

import (
	"reflect"
	"sort"
	"testing"
)

// Mock rationale: The scanner operates on an in-memory 'spectralMap'.
// For testing, we provide a controlled, smaller mock map to ensure deterministic results
// without relying on the global 'spectralMap' or any external I/O.
var mockSpectralMap = []SpectralEcho{
	{
		ID:        "TEST-001",
		Frequency: 90.0,
		Strength:  0.7,
		Location:  "Test Location A",
		EchoType:  "Data Stream",
		PotentialResources: []string{"Data"},
	},
	{
		ID:        "TEST-002",
		Frequency: 100.0,
		Strength:  0.4,
		Location:  "Test Location B",
		EchoType:  "Power Grid Hum",
		PotentialResources: []string{"Power"},
	},
	{
		ID:        "TEST-003",
		Frequency: 95.0,
		Strength:  0.8,
		Location:  "Test Location C",
		EchoType:  "Broadcast Relic",
		PotentialResources: []string{"Comms"},
	},
	{
		ID:        "TEST-004",
		Frequency: 110.0,
		Strength:  0.9,
		Location:  "Test Location D",
		EchoType:  "Data Stream",
		PotentialResources: []string{"More Data"},
	},
	{
		ID:        "TEST-005",
		Frequency: 92.5,
		Strength:  0.2,
		Location:  "Test Location E",
		EchoType:  "Weak Signal",
		PotentialResources: []string{"Nothing"},
	},
}

func TestNewScanner(t *testing.T) {
	sc := NewScanner(mockSpectralMap, 0.5)

	if !reflect.DeepEqual(tsc.spectralData, mockSpectralMap) {
		t.Errorf("NewScanner spectralData mismatch: got %v, want %v", tsc.spectralData, mockSpectralMap)
	}
	if tsc.minStrength != 0.5 {
		t.Errorf("NewScanner minStrength mismatch: got %f, want %f", tsc.minStrength, 0.5)
	}
}

func TestScanner_Scan_AllMatching(t *testing.T) {
	sc := NewScanner(mockSpectralMap, 0.5) // Min strength 0.5
	// All echoes except TEST-002 (strength 0.4) and TEST-005 (strength 0.2) should match
	// within the 80.0-120.0 MHz range.

	expected := []SpectralEcho{
		mockSpectralMap[0], // TEST-001 (90.0, 0.7)
		mockSpectralMap[2], // TEST-003 (95.0, 0.8)
		mockSpectralMap[3], // TEST-004 (110.0, 0.9)
	}

	detected := sc.Scan(80.0, 120.0, 2)

	// Sort both slices for deterministic comparison
	sort.Slice(detected, func(i, j int) bool { return detected[i].ID < detected[j].ID })
	sort.Slice(expected, func(i, j int) bool { return expected[i].ID < expected[j].ID })

	if !reflect.DeepEqual(detected, expected) {
		t.Errorf("Scan result mismatch.\nGot:  %v\nWant: %v", detected, expected)
	}
}

func TestScanner_Scan_NoMatchingFrequency(t *testing.T) {
	sc := NewScanner(mockSpectralMap, 0.5)
	detected := sc.Scan(1.0, 5.0, 1) // Very low frequency range, no matches

	if len(detected) != 0 {
		t.Errorf("Expected no echoes, got %d", len(detected))
	}
}

func TestScanner_Scan_NoMatchingStrength(t *testing.T) {
	sc := NewScanner(mockSpectralMap, 0.95) // High min strength
	detected := sc.Scan(80.0, 120.0, 1)

	// Only TEST-004 (strength 0.9) should match if minStrength is 0.9, but 0.95 means no match.
	if len(detected) != 0 {
		t.Errorf("Expected no echoes, got %d", len(detected))
	}
}

func TestScanner_Scan_PartialMatch(t *testing.T) {
	sc := NewScanner(mockSpectralMap, 0.6) // Min strength 0.6
	// Freq range 90.0-100.0
	// TEST-001 (90.0, 0.7) -> Match
	// TEST-002 (100.0, 0.4) -> No match (strength)
	// TEST-003 (95.0, 0.8) -> Match

	expected := []SpectralEcho{
		mockSpectralMap[0], // TEST-001 (90.0, 0.7)
		mockSpectralMap[2], // TEST-003 (95.0, 0.8)
	}

	detected := sc.Scan(90.0, 100.0, 3)

	sort.Slice(detected, func(i, j int) bool { return detected[i].ID < detected[j].ID })
	sort.Slice(expected, func(i, j int) bool { return expected[i].ID < expected[j].ID })

	if !reflect.DeepEqual(detected, expected) {
		t.Errorf("Scan result mismatch.\nGot:  %v\nWant: %v", detected, expected)
	}
}

func TestScanner_Scan_Concurrency(t *testing.T) {
	sc := NewScanner(mockSpectralMap, 0.1) // Low min strength to ensure all are considered
	detected := sc.Scan(80.0, 120.0, 5) // More workers than items, should still work

	// With minStrength 0.1, all 5 items from mockSpectralMap should be detected.
	expected := []SpectralEcho{
		mockSpectralMap[0],
		mockSpectralMap[1],
		mockSpectralMap[2],
		mockSpectralMap[3],
		mockSpectralMap[4],
	}

	sort.Slice(detected, func(i, j int) bool { return detected[i].ID < detected[j].ID })
	sort.Slice(expected, func(i, j int) bool { return expected[i].ID < expected[j].ID })

	if !reflect.DeepEqual(detected, expected) {
		t.Errorf("Concurrent scan result mismatch.\nGot:  %v\nWant: %v", detected, expected)
	}

	if len(detected) != len(mockSpectralMap) {
		t.Errorf("Expected %d echoes, got %d", len(mockSpectralMap), len(detected))
	}
}

func TestScanner_Scan_ZeroWorkers(t *testing.T) {
	sc := NewScanner(mockSpectralMap, 0.5)
	detected := sc.Scan(80.0, 120.0, 0) // Zero workers

	if len(detected) != 0 {
		t.Errorf("Expected no echoes with zero workers, got %d", len(detected))
	}
}
