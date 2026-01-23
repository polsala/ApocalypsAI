package main

import (
	"bytes"
	"strings"
	"testing"
)

// Mock rationale: We avoid network dependencies by testing pure functions like reverse.

func TestReverse(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"hello", "olleh"},
		{"world", "dlrow"},
		{"racecar", "racecar"},
		{"", ""},
		{"a", "a"},
	}

	for _, test := range tests {
		result := reverse(test.input)
		if result != test.expected {
			t.Errorf("reverse(%q) = %q; expected %q", test.input, result, test.expected)
		}
	}
}

func TestStatsTracking(t *testing.T) {
	stats = Stats{} // Reset stats

	stats.mutex.Lock()
	stats.totalMessages = 5
	stats.activeConnections = 2
	stats.mutex.Unlock()

	stats.mutex.Lock()
	if stats.totalMessages != 5 {
		t.Errorf("Expected totalMessages to be 5, got %d", stats.totalMessages)
	}
	if stats.activeConnections != 2 {
		t.Errorf("Expected activeConnections to be 2, got %d", stats.activeConnections)
	}
	stats.mutex.Unlock()
}

func TestReverseWithSpecialChars(t *testing.T) {
	input := "!@#$%^&*()"
	expected := ")(*&^%$#@!"
	result := reverse(input)
	if result != expected {
		t.Errorf("reverse(%q) = %q; expected %q", input, result, expected)
	}
}

func TestReverseUnicode(t *testing.T) {
	input := "こんにちは"
	expected := "はちにんこ"
	result := reverse(input)
	if result != expected {
		t.Errorf("reverse(%q) = %q; expected %q", input, result, expected)
	}
}

func FuzzReverse(f *testing.F) {
	f.Add("hello")
	f.Add("")
	f.Add("a")
	f.Fuzz(func(t *testing.T, s string) {
		reversed := reverse(s)
		doubleReversed := reverse(reversed)
		if doubleReversed != s {
			t.Errorf("Double reverse of %q is %q; expected original", s, doubleReversed)
		}
	})
}
