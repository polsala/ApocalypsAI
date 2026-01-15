package main

import (
	"fmt"
	"math/rand"
	"os"
	"sync"
	"time"
)

// ListeningPost represents a simulated network endpoint.
type ListeningPost struct {
	URL          string
	MinLatencyMs int     // Minimum simulated latency in milliseconds
	MaxLatencyMs int     // Maximum simulated latency in milliseconds
	FailureRate  float64 // Probability of failure (0.0 to 1.0)
}

// RelayResult holds the outcome of sending a whisper to a ListeningPost.
type RelayResult struct {
	PostURL  string
	Status   string // "Success", "Failure"
	Latency  time.Duration
	Error    string
}

// sendWhisper simulates sending a message to a listening post and getting an echo.
// It uses a mockable function for actual "network" interaction.
var sendWhisperFunc = func(post ListeningPost, message string) RelayResult {
	// Simulate network latency
	latencyMs := rand.Intn(post.MaxLatencyMs-post.MinLatencyMs+1) + post.MinLatencyMs
	time.Sleep(time.Duration(latencyMs) * time.Millisecond)

	// Simulate potential failure
	if rand.Float64() < post.FailureRate {
		return RelayResult{
			PostURL: post.URL,
			Status:  "Failure",
			Latency: time.Duration(latencyMs) * time.Millisecond,
			Error:   fmt.Sprintf("Temporal distortion detected at %s", post.URL),
		}
	}

	return RelayResult{
		PostURL: post.URL,
		Status:  "Success",
		Latency: time.Duration(latencyMs) * time.Millisecond,
		Error:   "",
	}
}

// osExit is a variable that can be overridden in tests to prevent actual program exit.
var osExit = os.Exit

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-echo-chamber-relay <whisper_message>")
		osExit(1) // Use the mockable osExit
	}
	whisperMessage := os.Args[1]

	// Seed random for latency and failure simulation
	// # Mock rationale: rand.Seed is called once here. For tests, we mock sendWhisperFunc directly
	// to control outcomes, making the random seed irrelevant for test determinism.
	rand.Seed(time.Now().UnixNano())

	listeningPosts := []ListeningPost{
		{URL: "echo-chamber-alpha.void", MinLatencyMs: 50, MaxLatencyMs: 150, FailureRate: 0.1},
		{URL: "echo-chamber-beta.void", MinLatencyMs: 100, MaxLatencyMs: 300, FailureRate: 0.05},
		{URL: "echo-chamber-gamma.void", MinLatencyMs: 20, MaxLatencyMs: 80, FailureRate: 0.2},
		{URL: "echo-chamber-delta.void", MinLatencyMs: 150, MaxLatencyMs: 400, FailureRate: 0.0}, // Very reliable
	}

	var wg sync.WaitGroup
	resultsChan := make(chan RelayResult, len(listeningPosts))

	fmt.Printf("Relaying whisper \"%s\" to %d echo chambers...\n", whisperMessage, len(listeningPosts))

	for _, post := range listeningPosts {
		wg.Add(1)
		go func(p ListeningPost) {
			defer wg.Done()
			result := sendWhisperFunc(p, whisperMessage)
			resultsChan <- result
		}(post)
	}

	wg.Wait()
	close(resultsChan)

	fmt.Println("\n--- Echo Report ---")
	successCount := 0
	failureCount := 0
	for result := range resultsChan {
		if result.Status == "Success" {
			fmt.Printf("✅ %-25s | Status: %s | Latency: %-8s\n", result.PostURL, result.Status, result.Latency)
			successCount++
		} else {
			fmt.Printf("❌ %-25s | Status: %s | Latency: %-8s | Error: %s\n", result.PostURL, result.Status, result.Latency, result.Error)
			failureCount++
		}
	}

	fmt.Printf("\nSummary: %d successful echoes, %d failed echoes.\n", successCount, failureCount)
}
