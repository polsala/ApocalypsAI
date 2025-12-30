package main

import "testing"

func TestMixQuoteStructure(t *testing.T) {
    q := mixQuote()
    // Mock rationale: ensure the quote contains a comma and ends with a period.
    if len(q) == 0 {
        t.Fatalf("quote is empty")
    }
    if q[len(q)-1] != '.' {
        t.Fatalf("quote does not end with period: %s", q)
    }
    if !contains(q, ",") {
        t.Fatalf("quote does not contain a comma separator: %s", q)
    }
}

// contains is a helper to check substring presence.
// Mock rationale: simple implementation without external deps.
func contains(s, substr string) bool {
    return len(s) >= len(substr) && (func() bool {
        for i := 0; i <= len(s)-len(substr); i++ {
            if s[i:i+len(substr)] == substr {
                return true
            }
        }
        return false
    })()
}
