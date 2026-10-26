package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

// timeProvider is a function that returns the current time. Useful for mocking in tests.
var timeProvider = func() time.Time { return time.Now().UTC() }

// fetchServiceTime fetches the current time from a given URL and calculates drift.
func fetchServiceTime(url string, beaconStartTime time.Time, results chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()

	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		res_msg := fmt.Sprintf("[%s] Error fetching time: %v", url, err)
		results <- res_msg
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		res_msg := fmt.Sprintf("[%s] Received non-OK status: %d", url, resp.StatusCode)
		results <- res_msg
		return
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		res_msg := fmt.Sprintf("[%s] Error reading response body: %v", url, err)
		results <- res_msg
		return
	}

	serviceTimeStr := strings.TrimSpace(string(body))
	serviceTime, err := time.Parse(time.RFC3339, serviceTimeStr)
	if err != nil {
		res_msg := fmt.Sprintf("[%s] Error parsing service time '%s': %v", url, serviceTimeStr, err)
		results <- res_msg
		return
	}

	// Calculate round-trip time (RTT) for a more accurate drift calculation.
	// This is a simplification; a more robust solution would use NTP or similar.
	beaconEndTime := timeProvider()
	// Assume half of the RTT is one-way latency. This is a heuristic.
	latency := beaconEndTime.Sub(beaconStartTime) / 2

	drift := serviceTime.Sub(beaconStartTime.Add(latency))

	status := "Aligned"
	if abs(drift) > 1*time.Second {
		status = "Significant Drift"
	} else if abs(drift) > 100*time.Millisecond {
		status = "Slight Drift"
	}

	res_msg := fmt.Sprintf("[%s] Service Time: %s, Drift: %s, Status: %s", url, serviceTime.Format(time.RFC3339), drift, status)
	results <- res_msg
}

func abs(d time.Duration) time.Duration {
	if d < 0 {
		return -d
	}
	return d
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: chrono-sync-beacon <endpoint1_url> [endpoint2_url ...]")
		os.Exit(1)
	}

	endpoints := os.Args[1:]

	var wg sync.WaitGroup
	results := make(chan string, len(endpoints))

	fmt.Printf("Nightly Chrono-Sync Beacon initiated at %s (UTC). Probing %d endpoints...\n", timeProvider().Format(time.RFC3339), len(endpoints))

	for _, url := range endpoints {
		wg.Add(1)
		go fetchServiceTime(url, timeProvider(), results, &wg)
	}

	wg.Wait()
	close(results)

	fmt.Println("\n--- Temporal Alignment Report ---")
	for res := range results {
		fmt.Println(res)
	}
	fmt.Println("---------------------------------")
}
