package main

import (
	"encoding/json"
	"os"
	"testing"
	"time"
)

func TestGenerateEntangledState(t *testing.T) {
	// Test normal entanglement
	state := generateEntangledState(0.1)
	if state.SpinX < -1 || state.SpinX > 1 {
		t.Errorf("SpinX out of range: %f", state.SpinX)
	}
	if state.SpinY < -1 || state.SpinY > 1 {
		t.Errorf("SpinY out of range: %f", state.SpinY)
	}
	if state.SpinZ < -1 || state.SpinZ > 1 {
		t.Errorf("SpinZ out of range: %f", state.SpinZ)
	}
	if state.Timestamp == 0 {
		t.Error("Timestamp should not be zero")
	}
}

func TestGenerateEntangledStateWithHighDecoherence(t *testing.T) {
	// Test with high decoherence rate
	state := generateEntangledState(0.9)
	// Should still generate valid quantum state
	if state.SpinX < -1 || state.SpinX > 1 {
		t.Errorf("SpinX out of range with high decoherence: %f", state.SpinX)
	}
}

func TestSimulateBellMeasurement(t *testing.T) {
	state := QuantumState{
		SpinX: 0.5,
		SpinY: 0.5,
		SpinZ: 0.7,
		IsEntangled: true,
		Timestamp: time.Now().UnixNano(),
	}

	measurement := simulateBellMeasurement(state, 0.0)
	if measurement < 0 || measurement > 1 {
		t.Errorf("Bell measurement out of range: %f", measurement)
	}
}

func TestSimulateBellMeasurementWithDecoherence(t *testing.T) {
	state := QuantumState{
		SpinX: 1.0,
		SpinY: 1.0,
		SpinZ: 1.0,
		IsEntangled: true,
		Timestamp: time.Now().UnixNano(),
	}

	// Test with high decoherence
	measurement := simulateBellMeasurement(state, 1.0)
	if measurement < 0 || measurement > 1 {
		t.Errorf("Bell measurement out of range with decoherence: %f", measurement)
	}
}

func TestCalculateCorrelation(t *testing.T) {
	// Test with perfect correlation
	measurements := []float64{1.0, 1.0, 1.0, 1.0}
	correlation := calculateCorrelation(measurements)
	if correlation != 0 {
		t.Errorf("Expected 0 correlation for constant values, got %f", correlation)
	}

	// Test with empty slice
	correlation = calculateCorrelation([]float64{})
	if correlation != 0 {
		t.Error("Expected 0 correlation for empty slice")
	}
}

func TestCalculateOverallFidelity(t *testing.T) {
	results := []EntanglementResult{
		{Fidelity: 0.8},
		{Fidelity: 0.9},
		{Fidelity: 0.7},
	}

	fidelity := calculateOverallFidelity(results)
	expected := (0.8 + 0.9 + 0.7) / 3
	if fidelity != expected {
		t.Errorf("Expected fidelity %f, got %f", expected, fidelity)
	}
}

func TestCalculateOverallCorrelation(t *testing.T) {
	results := []EntanglementResult{
		{Correlation: 0.8},
		{Correlation: 0.9},
		{Correlation: 0.7},
	}

	correlation := calculateOverallCorrelation(results)
	expected := (0.8 + 0.9 + 0.7) / 3
	if correlation != expected {
		t.Errorf("Expected correlation %f, got %f", expected, correlation)
	}
}

func TestDetermineEntanglementStatus(t *testing.T) {
	tests := []struct {
		fidelity   float64
		correlation float64
		expected   string
	}{
		{0.9, 0.8, "VERIFIED"},
		{0.7, 0.6, "PARTIAL"},
		{0.5, 0.4, "BROKEN"},
		{0.85, 0.6, "PARTIAL"},
		{0.65, 0.8, "PARTIAL"},
	}

	for _, test := range tests {
		status := determineEntanglementStatus(test.fidelity, test.correlation)
		if status != test.expected {
			t.Errorf("For fidelity %f and correlation %f, expected %s, got %s",
				test.fidelity, test.correlation, test.expected, status)
		}
	}
}

func TestCalculateEntanglementScore(t *testing.T) {
	tests := []struct {
		fidelity   float64
		correlation float64
		expected   float64
	}{
		{1.0, 1.0, 10.0},
		{0.5, 0.5, 5.0},
		{0.8, 0.9, 8.5},
		{0.0, 0.0, 0.0},
	}

	for _, test := range tests {
		score := calculateEntanglementScore(test.fidelity, test.correlation)
		if score != test.expected {
			t.Errorf("For fidelity %f and correlation %f, expected score %f, got %f",
				test.fidelity, test.correlation, test.expected, score)
		}
	}
}

func TestCalculateQuantumCoherence(t *testing.T) {
	tests := []struct {
		entangledCount int64
		totalCount     int64
		expected       float64
	}{
		{5, 10, 50.0},
		{10, 10, 100.0},
		{0, 10, 0.0},
		{0, 0, 0.0},
	}

	for _, test := range tests {
		coherence := calculateQuantumCoherence(test.entangledCount, test.totalCount)
		if coherence != test.expected {
			t.Errorf("For %d entangled out of %d total, expected coherence %f, got %f",
				test.entangledCount, test.totalCount, test.expected, coherence)
		}
	}
}

func TestJSONReportGeneration(t *testing.T) {
	report := &EntanglementReport{
		Timestamp:          time.Now(),
		Nodes:              3,
		Iterations:         100,
		DecoherenceRate:    0.1,
		OverallFidelity:    0.85,
		OverallCorrelation: 0.75,
		EntanglementStatus: "VERIFIED",
		EntanglementScore:  8.0,
		QuantumCoherence:   90.0,
		Results: []EntanglementResult{
			{NodeID: 0, IsEntangled: true, Fidelity: 0.8, Correlation: 0.7, MeasurementTime: 10.5},
			{NodeID: 1, IsEntangled: true, Fidelity: 0.9, Correlation: 0.8, MeasurementTime: 11.2},
			{NodeID: 2, IsEntangled: false, Fidelity: 0.7, Correlation: 0.6, MeasurementTime: 9.8},
		},
	}

	filename := "test_report.json"
	defer os.Remove(filename)

	err := generateJSONReport(report, filename)
	if err != nil {
		t.Fatalf("Failed to generate JSON report: %v", err)
	}

	// Verify file was created
	if _, err := os.Stat(filename); os.IsNotExist(err) {
		t.Error("JSON report file was not created")
	}

	// Verify JSON content
	file, err := os.Open(filename)
	if err != nil {
		t.Fatalf("Failed to open JSON report: %v", err)
	}
	defer file.Close()

	var parsedReport EntanglementReport
	decoder := json.NewDecoder(file)
	err = decoder.Decode(&parsedReport)
	if err != nil {
		t.Fatalf("Failed to parse JSON report: %v", err)
	}

	if parsedReport.Nodes != report.Nodes {
		t.Errorf("Expected %d nodes, got %d", report.Nodes, parsedReport.Nodes)
	}
	if parsedReport.EntanglementStatus != report.EntanglementStatus {
		t.Errorf("Expected status %s, got %s", report.EntanglementStatus, parsedReport.EntanglementStatus)
	}
}

func TestRunEntanglementVerification(t *testing.T) {
	// Test with minimal parameters
	report := runEntanglementVerification(2, 10, 0.1)

	if report.Nodes != 2 {
		t.Errorf("Expected 2 nodes, got %d", report.Nodes)
	}
	if report.Iterations != 10 {
		t.Errorf("Expected 10 iterations, got %d", report.Iterations)
	}
	if len(report.Results) != 2 {
		t.Errorf("Expected 2 results, got %d", len(report.Results))
	}

	// Verify all results have valid data
	for _, result := range report.Results {
		if result.Fidelity < 0 || result.Fidelity > 1 {
			t.Errorf("Invalid fidelity: %f", result.Fidelity)
		}
		if result.Correlation < -1 || result.Correlation > 1 {
			t.Errorf("Invalid correlation: %f", result.Correlation)
		}
		if result.MeasurementTime <= 0 {
			t.Errorf("Invalid measurement time: %f", result.MeasurementTime)
		}
	}
}

// Benchmark tests
func BenchmarkGenerateEntangledState(b *testing.B) {
	for i := 0; i < b.N; i++ {
		generateEntangledState(0.1)
	}
}

func BenchmarkSimulateBellMeasurement(b *testing.B) {
	state := QuantumState{
		SpinX: 0.5,
		SpinY: 0.5,
		SpinZ: 0.7,
		IsEntangled: true,
		Timestamp: time.Now().UnixNano(),
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		simulateBellMeasurement(state, 0.1)
	}
}

func BenchmarkCalculateCorrelation(b *testing.B) {
	measurements := make([]float64, 1000)
	for i := range measurements {
		measurements[i] = float64(i%2) * 0.5
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		calculateCorrelation(measurements)
	}
}

func BenchmarkRunEntanglementVerification(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		runEntanglementVerification(5, 100, 0.05)
	}
}
