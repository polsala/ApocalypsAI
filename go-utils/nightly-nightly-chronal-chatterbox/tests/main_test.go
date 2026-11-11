package main

import (
	"bufio"
	"bytes"
	"io"
	"math/rand"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// --- Mocking Utilities ---

// mockRandSource implements rand.Source for deterministic random number generation.
type mockRandSource struct {
	floats []float64
	ints   []int
	floatIdx int
	intIdx   int
	mu       sync.Mutex // Protects access to indices
}

func (m *mockRandSource) Int63() int64 {
	m.mu.Lock()
	defer m.mu.Unlock()
	if m.intIdx >= len(m.ints) {
		return 0 // Default or panic if more ints are requested than provided
	}
	val := m.ints[m.intIdx]
	m.intIdx++
	return int64(val)
}

func (m *mockRandSource) Seed(seed int64) {} // No-op for mock

func (m *mockRandSource) Float64() float64 {
	m.mu.Lock()
	defer m.mu.Unlock()
	if m.floatIdx >= len(m.floats) {
		return 0.0 // Default or panic if more floats are requested than provided
	}
	val := m.floats[m.floatIdx]
	m.floatIdx++
	return val
}

// NewMockRand creates a new *rand.Rand with a deterministic source.
func NewMockRand(floats []float64, ints []int) *rand.Rand {
	return rand.New(&mockRandSource{floats: floats, ints: ints})
}

// --- Test Cases ---

func TestApplyLatency(t *testing.T) {
	// # Mock rationale: time.Sleep is a blocking call. For deterministic and fast tests, we need to ensure it's called with the correct duration without actually waiting.
	originalSleep := sleep
	defer func() { sleep = originalSleep }() // Restore original sleep after test

	var sleptFor time.Duration
	sleep = func(d time.Duration) {
		sleptFor = d // Capture the duration sleep was called with
	}

	expectedDuration := 100 * time.Millisecond
	te := &TemporalEffects{Latency: expectedDuration}

	if te.Latency > 0 {
		sleep(te.Latency)
	}

	if sleptFor != expectedDuration {
		t.Errorf("Expected sleep for %v, got %v", expectedDuration, sleptFor)
	}
}

func TestApplyPacketLoss(t *testing.T) {
	// # Mock rationale: rand.Float64 introduces non-determinism. For deterministic tests, we need to control its output to test both "loss" and "no loss" scenarios.

	// Test case 1: No loss (mocked Float64 < PacketLossProb)
	mockRandNoLoss := NewMockRand([]float64{0.1}, nil)
	teNoLoss := &TemporalEffects{PacketLossProb: 0.5, Rand: mockRandNoLoss}
	msgNoLoss, lostNoLoss := teNoLoss.applyPacketLoss("hello")
	if lostNoLoss || msgNoLoss != "hello" {
		t.Errorf("Expected no loss, got lost=%t, msg=%q", lostNoLoss, msgNoLoss)
	}

	// Test case 2: Loss (mocked Float64 >= PacketLossProb)
	mockRandLoss := NewMockRand([]float64{0.6}, nil)
	teLoss := &TemporalEffects{PacketLossProb: 0.5, Rand: mockRandLoss}
	msgLoss, lostLoss := teLoss.applyPacketLoss("world")
	if !lostLoss || msgLoss != "" {
		t.Errorf("Expected loss, got lost=%t, msg=%q", lostLoss, msgLoss)
	}

	// Test case 3: No loss when probability is 0
	mockRandZeroProb := NewMockRand([]float64{0.9}, nil)
	teZeroProb := &TemporalEffects{PacketLossProb: 0.0, Rand: mockRandZeroProb}
	msgZeroProb, lostZeroProb := teZeroProb.applyPacketLoss("test")
	if lostZeroProb || msgZeroProb != "test" {
		t.Errorf("Expected no loss with 0 probability, got lost=%t, msg=%q", lostZeroProb, msgZeroProb)
	}
}

func TestApplyTemporalDistortion(t *testing.T) {
	// # Mock rationale: rand.Intn and other random functions make distortion non-deterministic. For deterministic tests, we need to control the random choices.

	// Intensity 0: No distortion
	mockRand0 := NewMockRand(nil, []int{})
	te0 := &TemporalEffects{DistortionIntensity: 0, Rand: mockRand0}
	if res := te0.applyTemporalDistortion("abc"); res != "abc" {
		t.Errorf("Expected no distortion for intensity 0, got %q", res)
	}

	// Intensity 1: Single swap (mocked Intn(len) for positions)
	// Input: "Hello"
	// Mocked Intn(5) -> 1 (for 'e'), Intn(5) -> 3 (for 'l')
	// Expected: "Helleo" (swapping 'e' at index 1 with 'l' at index 3)
	// Oh, wait, the distortion logic is `switch te.Rand.Intn(3)` for type of distortion.
	// Let's make it deterministic for a specific distortion type.

	// Test case 1: Swap characters (Intn(3) -> 0)
	// Input: "ABCDE"
	// Mocked Intn(len) -> 1 (B), Intn(len) -> 3 (D)
	// Expected: "ADCBE"
	mockRandSwap := NewMockRand(nil, []int{0, 1, 3}) // 0 for swap, then 1, 3 for indices
	teSwap := &TemporalEffects{DistortionIntensity: 1, Rand: mockRandSwap}
	if res := teSwap.applyTemporalDistortion("ABCDE"); res != "ADCBE" {
		t.Errorf("Expected swap distortion 'ADCBE', got %q", res)
	}

	// Test case 2: Insert character (Intn(3) -> 1)
	// Input: "ABC"
	// Mocked Intn(len) -> 1 (B), Intn(len+1) -> 2 (insert at index 2)
	// Expected: "ABBC"
	mockRandInsert := NewMockRand(nil, []int{1, 1, 2}) // 1 for insert, then 1 for char index, 2 for insert position
	teInsert := &TemporalEffects{DistortionIntensity: 1, Rand: mockRandInsert}
	if res := teInsert.applyTemporalDistortion("ABC"); res != "ABBC" {
		t.Errorf("Expected insert distortion 'ABBC', got %q", res)
	}

	// Test case 3: Delete character (Intn(3) -> 2)
	// Input: "ABCDE"
	// Mocked Intn(len) -> 2 (C)
	// Expected: "ABDE"
	mockRandDelete := NewMockRand(nil, []int{2, 2}) // 2 for delete, then 2 for delete position
	teDelete := &TemporalEffects{DistortionIntensity: 1, Rand: mockRandDelete}
	if res := teDelete.applyTemporalDistortion("ABCDE"); res != "ABDE" {
		t.Errorf("Expected delete distortion 'ABDE', got %q", res)
	}

	// Test case 4: Multiple distortions (Intensity 2)
	// Input: "XYZ"
	// 1st distortion: Swap (Intn(3)->0), indices 0, 2 (X, Z) -> "ZYX"
	// 2nd distortion: Insert (Intn(3)->1), char index 1 (Y), insert pos 1 -> "ZYYX"
	mockRandMulti := NewMockRand(nil, []int{0, 0, 2, 1, 1, 1}) // Swap (0,0,2), Insert (1,1,1)
	teMulti := &TemporalEffects{DistortionIntensity: 2, Rand: mockRandMulti}
	if res := teMulti.applyTemporalDistortion("XYZ"); res != "ZYYX" {
		t.Errorf("Expected multi-distortion 'ZYYX', got %q", res)
	}
}

func TestHandleConnection(t *testing.T) {
	// # Mock rationale: net.Conn involves actual network I/O, which is slow and non-deterministic. net.Pipe allows simulating network communication in-memory.
	clientConn, serverConn := net.Pipe()
	defer clientConn.Close()
	defer serverConn.Close()

	// Mock sleep function
	originalSleep := sleep
	defer func() { sleep = originalSleep }()
	var sleptFor time.Duration
	sleep = func(d time.Duration) { sleptFor = d }

	// Mock random source for deterministic behavior
	// Floats: 0.1 (no packet loss)
	// Ints: 0 (for distortion type: swap), 1 (index 1), 3 (index 3)
	mockRand := NewMockRand([]float64{0.1}, []int{0, 1, 3})

	te := &TemporalEffects{
		Latency:             50 * time.Millisecond,
		PacketLossProb:      0.0, // No loss for this test
		DistortionIntensity: 1,
		Rand:                mockRand,
	}

	// Start handler in a goroutine
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		handleConnection(serverConn, te)
	}()

	// Client sends message
	clientWriter := bufio.NewWriter(clientConn)
	clientReader := bufio.NewReader(clientConn)
	inputMsg := "Hello Temporal Echo!"
	_, err := clientWriter.WriteString(inputMsg + "\n")
	if err != nil {
		t.Fatalf("Client write error: %v", err)
	}
	clientWriter.Flush()

	// Client reads response
	response, err := clientReader.ReadString('\n')
	if err != nil {
		t.Fatalf("Client read error: %v", err)
	}

	// Verify latency was applied
	if sleptFor != te.Latency {
		t.Errorf("Expected sleep for %v, got %v", te.Latency, sleptFor)
	}

	// Verify distortion (based on mockRand and distortion logic: swap indices 1 and 3)
	// Original: "Hello Temporal Echo!"
	// Indices:   01234567890123456789
	// Chars:     H e l l o   T e m p o r a l   E c h o !
	// Swap 'e' (idx 1) with 'l' (idx 3) -> "Hlleo Temporal Echo!"
	expectedDistortion := "Hlleo Temporal Echo!\n"
	if response != expectedDistortion {
		t.Errorf("Expected distorted response %q, got %q", expectedDistortion, response)
	}

	wg.Wait() // Wait for handleConnection to finish
}

func TestHandleConnection_PacketLoss(t *testing.T) {
	// # Mock rationale: net.Conn involves actual network I/O, which is slow and non-deterministic. net.Pipe allows simulating network communication in-memory.
	clientConn, serverConn := net.Pipe()
	defer clientConn.Close()
	defer serverConn.Close()

	// Mock random source to force packet loss
	mockRand := NewMockRand([]float64{0.9}, nil) // 0.9 > 0.5, so loss occurs

	te := &TemporalEffects{
		Latency:             0,
		PacketLossProb:      0.5, // High probability to ensure loss
		DistortionIntensity: 0,
		Rand:                mockRand,
	}

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		handleConnection(serverConn, te)
	}()

	clientWriter := bufio.NewWriter(clientConn)
	inputMsg := "This message should be lost."
	_, err := clientWriter.WriteString(inputMsg + "\n")
	if err != nil {
		t.Fatalf("Client write error: %v", err)
	}
	clientWriter.Flush()

	// Client attempts to read, expecting EOF or timeout due to no response
	clientConn.SetReadDeadline(time.Now().Add(100 * time.Millisecond)) // Set a short deadline
	reader := bufio.NewReader(clientConn)
	_, err = reader.ReadString('\n')

	if err == nil || !strings.Contains(err.Error(), "timeout") && err != io.EOF {
		t.Errorf("Expected read error (timeout or EOF) due to packet loss, got %v", err)
	}

	wg.Wait()
}
