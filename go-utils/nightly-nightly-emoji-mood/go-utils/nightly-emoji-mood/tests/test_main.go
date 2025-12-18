package main

import (
	"bytes"
	"os/exec"
	"strings"
	"testing"
	"time"
)

func TestEmojiOutput(t *testing.T) {
	// Mock getCurrentTime to return a fixed time
	original := getCurrentTime
	getCurrentTime = func() time.Time {
		return time.Date(2023, 10, 2, 12, 0, 0, 0, time.UTC) // Monday
	}
	defer func() { getCurrentTime = original }()

	cmd := exec.Command("go", "run", "src/main.go")
	var out bytes.Buffer
	cmd.Stdout = &out
	if err := cmd.Run(); err != nil {
		t.Fatalf("command failed: %v", err)
	}
	result := strings.TrimSpace(out.String())
	expected := "💪"
	if result != expected {
		t.Fatalf("expected %q, got %q", expected, result)
	}
}

func TestEmojiWithPhrase(t *testing.T) {
	original := getCurrentTime
	getCurrentTime = func() time.Time {
		return time.Date(2023, 10, 3, 12, 0, 0, 0, time.UTC) // Tuesday
	}
	defer func() { getCurrentTime = original }()

	cmd := exec.Command("go", "run", "src/main.go", "--phrase")
	var out bytes.Buffer
	cmd.Stdout = &out
	if err := cmd.Run(); err != nil {
		t.Fatalf("command failed: %v", err)
	}
	result := strings.TrimSpace(out.String())
	if !strings.HasPrefix(result, "🚀") {
		t.Fatalf("expected output to start with 🚀, got %q", result)
	}
	// Check that a phrase is present
	if len(strings.Fields(result)) < 2 {
		t.Fatalf("expected a phrase after emoji, got %q", result)
	}
}
