package main

import (
	"testing"
	"time"
)

// Mock rationale: We need to test the expiration logic. Instead of mocking time.Now(),
// which is complex and often leads to brittle tests, we use a very short cleanInterval
// for the cache cleaner goroutine and explicit time.Sleep calls in tests to simulate
// time passing. This approach makes the tests deterministic and offline, as it doesn't
// rely on external services or complex time manipulation libraries.

func TestEchoCache_SetAndGet(t *testing.T) {
	cache := NewEchoCache(10 * time.Millisecond) // Short interval for faster testing
	defer cache.StopCleaner()

	cache.Set("key1", "value1", 10) // TTL 10 seconds
	val, ok := cache.Get("key1")

	if !ok {
		t.Errorf("Expected key1 to be found, but it was not.")
	}
	if val != "value1" {
		t.Errorf("Expected value1, got %s", val)
	}

	_, ok = cache.Get("nonexistent")
	if ok {
		t.Errorf("Expected nonexistent key to not be found, but it was.")
	}
}

func TestEchoCache_Expiration(t *testing.T) {
	cache := NewEchoCache(10 * time.Millisecond) // Short interval for faster testing
	defer cache.StopCleaner()

	cache.Set("expiring_key", "expiring_value", 1) // Expires in 1 second

	// Immediately after setting, it should be present
	val, ok := cache.Get("expiring_key")
	if !ok {
		t.Errorf("Expected expiring_key to be found immediately after set.")
	}
	if val != "expiring_value" {
		t.Errorf("Expected expiring_value, got %s", val)
	}

	// Wait for more than the TTL + cleaner interval to ensure expiration is processed
	time.Sleep(1500 * time.Millisecond) // 1.5 seconds

	// After expiration, it should not be found
	_, ok = cache.Get("expiring_key")
	if ok {
		t.Errorf("Expected expiring_key to be expired, but it was found.")
	}

	// Check for echo
	echoes := cache.GetEchoes()
	if len(echoes) == 0 {
		t.Errorf("Expected at least one echo, got none.")
	}
	expectedEcho := "Temporal Echo: Key 'expiring_key' with value 'expiring_value' expired."
	foundEcho := false
	for _, echo := range echoes {
		if echo == expectedEcho {
			foundEcho = true
			break
		}
	}
	if !foundEcho {
		t.Errorf("Expected echo '%s' not found in echoes: %v", expectedEcho, echoes)
	}
}

func TestEchoCache_Delete(t *testing.T) {
	cache := NewEchoCache(10 * time.Millisecond)
	defer cache.StopCleaner()

	cache.Set("deletable_key", "deletable_value", 10) // TTL 10 seconds
	_, ok := cache.Get("deletable_key")
	if !ok {
		t.Errorf("Expected deletable_key to be found.")
	}

	cache.Delete("deletable_key")
	_, ok = cache.Get("deletable_key")
	if ok {
		t.Errorf("Expected deletable_key to be deleted, but it was found.")
	}
}

func TestEchoCache_MultipleExpirationsAndEchoes(t *testing.T) {
	cache := NewEchoCache(10 * time.Millisecond)
	defer cache.StopCleaner()

	cache.Set("keyA", "valueA", 1) // Expires in 1s
	cache.Set("keyB", "valueB", 2) // Expires in 2s

	time.Sleep(1500 * time.Millisecond) // Wait for keyA to expire

	_, okA := cache.Get("keyA")
	if okA {
		t.Errorf("Expected keyA to be expired.")
	}
	_, okB := cache.Get("keyB")
	if !okB {
		t.Errorf("Expected keyB to still be present.")
	}

	echoes := cache.GetEchoes()
	if len(echoes) != 1 {
		t.Errorf("Expected 1 echo after 1.5s, got %d. Echoes: %v", len(echoes), echoes)
	}
	expectedEchoA := "Temporal Echo: Key 'keyA' with value 'valueA' expired."
	if echoes[0] != expectedEchoA {
		t.Errorf("Expected echo '%s', got '%s'", expectedEchoA, echoes[0])
	}

	time.Sleep(1000 * time.Millisecond) // Wait for keyB to expire (total 2.5s)

	_, okA = cache.Get("keyA") // Should still be expired
	if okA {
		t.Errorf("Expected keyA to be expired.")
	}
	_, okB = cache.Get("keyB") // Should now be expired
	if okB {
		t.Errorf("Expected keyB to be expired.")
	}

	echoes = cache.GetEchoes() // Get new echoes
	if len(echoes) != 1 { // Should be 1 new echo for keyB
		t.Errorf("Expected 1 new echo after 2.5s, got %d. Echoes: %v", len(echoes), echoes)
	}
	expectedEchoB := "Temporal Echo: Key 'keyB' with value 'valueB' expired."
	if echoes[0] != expectedEchoB {
		t.Errorf("Expected echo '%s', got '%s'", expectedEchoB, echoes[0])
	}
}

func TestEchoCache_StopCleaner(t *testing.T) {
	cache := NewEchoCache(10 * time.Millisecond)
	cache.Set("test_key", "test_value", 1) // Set a key to expire

	cache.StopCleaner() // Stop the cleaner immediately

	time.Sleep(1500 * time.Millisecond) // Wait past TTL

	// The key should still be present because the cleaner was stopped
	_, ok := cache.Get("test_key")
	if !ok {
		t.Errorf("Expected test_key to still be present after cleaner stopped, but it was not.")
	}

	echoes := cache.GetEchoes()
	if len(echoes) != 0 {
		t.Errorf("Expected no echoes after cleaner stopped, got %v", echoes)
	}
}
