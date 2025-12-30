package main

import (
	"bytes"
	"math/rand"
	"testing"
	"time"
)

// Mock rationale: We need deterministic tests for the anomaly application logic.
// By injecting a seeded `rand.Rand` source, we ensure that random decisions
// (like packet loss or byte corruption) are predictable and repeatable,
// allowing for reliable unit testing without actual network I/O.

func TestApplyAethericEffects_NoEffects(t *testing.T) {
	config := NewAethericConfig(0, 0.0, 0.0, 1024)
	input := []byte("Hello, Aether!")

	output, err := config.applyAethericEffects(input)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if output == nil {
		t.Fatalf("Expected output, got nil (loss)")
	}
	if !bytes.Equal(input, output) {
		t.Errorf("Expected output to be unchanged, got %q, want %q", output, input)
	}
}

func TestApplyAethericEffects_Loss(t *testing.T) {
	// Seed the random source to ensure loss occurs deterministically.
	// A seed of 1 will make rand.Float64() return 0.00000000000000000000 for the first call.
	// So, if lossRate is > 0, it should trigger.
	seededRand := rand.New(rand.NewSource(1)) // # Mock rationale: Deterministic random source for predictable loss.
	config := AethericConfig{
		DelayMs:        0,
		LossRate:       0.5, // High chance of loss
		CorruptionRate: 0.0,
		BufferSize:     1024,
		RandSource:     seededRand,
	}
	input := []byte("Lost in the Aether!")

	output, err := config.applyAethericEffects(input)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if output != nil {
		t.Errorf("Expected nil output (loss), got %q", output)
	}

	// Test with 0% loss rate to ensure no loss occurs
	config.LossRate = 0.0 // Ensure no loss for this specific test path
	output, err = config.applyAethericEffects(input)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if output == nil {
		t.Errorf("Expected output (no loss), got nil")
	}
	if !bytes.Equal(input, output) {
		t.Errorf("Expected output to be unchanged, got %q, want %q", output, input)
	}
}

func TestApplyAethericEffects_Corruption(t *testing.T) {
	// Seed the random source to ensure corruption occurs deterministically.
	// A seed of 1 will make rand.Float64() return 0.00000000000000000000 for the first call.
	// So, if corruptionRate is > 0, it should trigger for the first byte.
	seededRand := rand.New(rand.NewSource(1)) // # Mock rationale: Deterministic random source for predictable corruption.
	config := AethericConfig{
		DelayMs:        0,
		LossRate:       0.0,
		CorruptionRate: 1.0, // 100% chance to corrupt every byte
		BufferSize:     1024,
		RandSource:     seededRand,
	}
	input := []byte("Corrupt me!")

	output, err := config.applyAethericEffects(input)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if output == nil {
		t.Fatalf("Expected output, got nil (loss)")
	}
	if bytes.Equal(input, output) {
		t.Errorf("Expected output to be corrupted, but it was unchanged: %q", output)
	}

	// Verify that at least one byte was corrupted (with 100% corruption rate, all should be different)
	corruptedCount := 0
	for i := 0; i < len(input); i++ {
		if input[i] != output[i] {
			corruptedCount++
		}
	}
	if corruptedCount == 0 {
		t.Errorf("Expected at least one byte to be corrupted, but none were.")
	}

	// Test with 0% corruption rate
	config.CorruptionRate = 0.0
	output, err = config.applyAethericEffects(input)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if output == nil {
		t.Fatalf("Expected output, got nil (loss)")
	}
	if !bytes.Equal(input, output) {
		t.Errorf("Expected output to be unchanged with 0%% corruption, got %q, want %q", output, input)
	}
}

func TestApplyAethericEffects_Delay(t *testing.T) {
	config := NewAethericConfig(10, 0.0, 0.0, 1024)
	input := []byte("Delayed message")

	start := time.Now()
	output, err := config.applyAethericEffects(input)
	duration := time.Since(start)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if output == nil {
		t.Fatalf("Expected output, got nil (loss)")
	}
	if !bytes.Equal(input, output) {
		t.Errorf("Expected output to be unchanged, got %q, want %q", output, input)
	}

	// We can't guarantee exact sleep duration due to OS scheduling, but we can check if it was *at least* the delay.
	// # Mock rationale: While time.Sleep is hard to mock directly for duration, we can assert that *some* time passed.
	// For a true unit test, one might mock the time package, but for this level of utility, a duration check is acceptable.
	if duration < (time.Duration(config.DelayMs) * time.Millisecond) {
		t.Errorf("Expected delay of at least %dms, but only %s passed", config.DelayMs, duration)
	}
}
