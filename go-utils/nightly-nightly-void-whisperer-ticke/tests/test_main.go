package main

import (
	"testing"
	"time"
)

// Mock rationale: We simulate ticker behavior by running for a short duration
// and checking for panics or unexpected exits.
func TestTickerRuns(t *testing.T) {
	go main()
	time.Sleep(1 * time.Second)
}
