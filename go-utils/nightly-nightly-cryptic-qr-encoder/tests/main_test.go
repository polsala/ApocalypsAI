package main

import (
    "os"
    "os/exec"
    "testing"
)

func TestPlaceholderQR(t *testing.T) {
    // Temporary output file; will be removed after the test.
    outFile := "test_output.png"
    defer os.Remove(outFile)

    // Execute the program with a sample string.
    cmd := exec.Command("go", "run", "./src/main.go", "sample-text", outFile)
    // # Mock rationale: running the actual program is safe – it has no external dependencies.
    if err := cmd.Run(); err != nil {
        t.Fatalf("Program exited with error: %v", err)
    }

    info, err := os.Stat(outFile)
    if err != nil {
        t.Fatalf("Output file not created: %v", err)
    }
    if info.Size() <= 8 {
        t.Fatalf("Output file size (%d) is too small; expected placeholder PNG with data", info.Size())
    }
}
