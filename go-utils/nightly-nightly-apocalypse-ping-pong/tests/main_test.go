package main

import (
    "bytes"
    "fmt"
    "testing"
    "time"
)

func TestGenerateReport_WithMockedLatencies(t *testing.T) {
    // Save original pingFunc and restore after test
    orig := pingFunc
    defer func() { pingFunc = orig }()

    mockLatencies := map[string]time.Duration{
        "fast.com": 30 * time.Millisecond,
        "mid.com":  120 * time.Millisecond,
        "slow.com": 350 * time.Millisecond,
    }

    pingFunc = func(host string) (time.Duration, error) {
        if d, ok := mockLatencies[host]; ok {
            return d, nil
        }
        return 0, fmt.Errorf("unknown host")
    }

    hosts := []string{"slow.com", "fast.com", "mid.com"}
    report := generateReport(hosts)

    if !bytes.Contains([]byte(report), []byte("⚡ fast.com (30ms)")) {
        t.Errorf("fast host emoji missing or incorrect: %s", report)
    }
    if !bytes.Contains([]byte(report), []byte("~ mid.com (120ms)")) {
        t.Errorf("mid host emoji missing or incorrect: %s", report)
    }
    if !bytes.Contains([]byte(report), []byte("🐢 slow.com (350ms)")) {
        t.Errorf("slow host emoji missing or incorrect: %s", report)
    }
}
