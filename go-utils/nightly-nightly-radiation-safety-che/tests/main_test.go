package main

import "testing"

func TestEvaluate(t *testing.T) {
    cases := []struct {
        level    float64
        expected string
    }{
        {0.3, "🌿 Radiation level 0.30 µSv/h: Safe. The glow is gentle."},
        {0.7, "⚠️ Radiation level 0.70 µSv/h: Caution. Keep your hat on."},
        {3.5, "☢️ Radiation level 3.50 µSv/h: Dangerous! Seek shelter immediately."},
    }
    for _, c := range cases {
        got := evaluate(c.level)
        if got != c.expected {
            t.Errorf("evaluate(%v) = %q, want %q", c.level, got, c.expected)
        }
    }
}
// Mock rationale: tests use deterministic values, no external dependencies.
