package main

import (
	"os/exec"
	"strings"
	"testing"
)

func TestEncodeString(t *testing.T) {
	// Build the binary first
	buildCmd := exec.Command("go", "build", "-o", "nightly-emoji-encoder", "src/main.go")
	if err := buildCmd.Run(); err != nil {
		t.Fatalf("failed to build binary: %v", err)
	}

	// Define test cases
	cases := []struct {
		input string
		output string
	}{
		{"Hi!", "🇭🇮!"},
		{"Hello 123", "🇭🇪🇱🇱🇴 1️⃣2️⃣3️⃣"},
		{"GoLang", "🇬🇴🇱🇦🇳🇬"},
	}

	for _, tc := range cases {
		cmd := exec.Command("./nightly-emoji-encoder")
		cmd.Stdin = strings.NewReader(tc.input)
		out, err := cmd.Output()
		if err != nil {
			t.Fatalf("execution failed: %v", err)
		}
		got := strings.TrimSpace(string(out))
		if got != tc.output {
			t.Errorf("input %q: expected %q, got %q", tc.input, tc.output, got)
		}
	}
}
