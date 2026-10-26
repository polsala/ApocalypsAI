package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"sync"
	"time"
)

// BeaconStatus represents the status of a monitored endpoint.
type BeaconStatus struct {
	URL     string
	Status  string // "Steady", "Lagging", "Silent"
	Latency time.Duration
	Error   error
}

// checkBeacon pings a single URL and returns its status.
func checkBeacon(url string, timeout time.Duration) BeaconStatus {
	client := &http.Client{
		Timeout: timeout,
	}
	start := time.Now()
	resp, err := client.Get(url)
	latency := time.Since(start)

	if err != nil {
		return BeaconStatus{URL: url, Status: "Silent", Latency: latency, Error: err}
	}
	defer resp.Body.Close()

	// Read body to ensure full response is received and connection is closed properly
	_, _ = ioutil.ReadAll(resp.Body)

	if resp.StatusCode == http.StatusOK {
		if latency > 500*time.Millisecond { // Arbitrary threshold for "Lagging"
			return BeaconStatus{URL: url, Status: "Lagging", Latency: latency}
		}
		return BeaconStatus{URL: url, Status: "Steady", Latency: latency}
	}
	return BeaconStatus{URL: url, Status: "Silent", Latency: latency, Error: fmt.Errorf("HTTP status %d", resp.StatusCode)}
}

// monitorBeacons concurrently checks a list of URLs.
func monitorBeacons(endpoints []string, timeout time.Duration) []BeaconStatus {
	var wg sync.WaitGroup
	results := make(chan BeaconStatus, len(endpoints))

	for _, url := range endpoints {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()
			results <- checkBeacon(u, timeout)
		}(url)
	}

	wg.Wait()
	close(results)

	var finalStatuses []BeaconStatus
	for res := range results {
		finalStatuses = append(finalStatuses, res)
	}
	return finalStatuses
}

func main() {
	endpointsStr := flag.String("endpoints", "", "Comma-separated list of URLs to monitor (e.g., 'http://example.com,http://google.com')")
	timeoutSec := flag.Int("timeout", 5, "Timeout for each beacon check in seconds")
	flag.Parse()

	if *endpointsStr == "" {
		fmt.Println("Error: No endpoints provided. Use -endpoints flag.")
		flag.Usage()
		return
	}

	endpoints := strings.Split(*endpointsStr, ",")
	if len(endpoints) == 0 {
		fmt.Println("Error: No valid endpoints found after parsing.")
		return
	}

	timeout := time.Duration(*timeoutSec) * time.Second

	fmt.Printf("Monitoring %d temporal beacons with a %s timeout per beacon...\n", len(endpoints), timeout)
	results := monitorBeacons(endpoints, timeout)

	fmt.Println("\n--- Temporal Beacon Report ---")
	for _, res := range results {
		statusEmoji := ""
		switch res.Status {
		case "Steady":
			statusEmoji = "🟢"
		case "Lagging":
			statusEmoji = "🟡"
		case "Silent":
			statusEmoji = "🔴"
		}
		latencyStr := "N/A"
		if res.Latency > 0 {
			latencyStr = res.Latency.Round(time.Millisecond).String()
		}
		errorStr := ""
		if res.Error != nil {
			errorStr = fmt.Sprintf(" (Error: %v)", res.Error)
		}
		fmt.Printf("%s %-10s %-40s Latency: %-10s%s\n", statusEmoji, res.Status, res.URL, latencyStr, errorStr)
	}
	fmt.Println("------------------------------")
}
