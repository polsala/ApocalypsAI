package main

import (
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

const (
	userAgent = "ApocalypsAI/ChronalDriftDetector/1.0"
	timeout   = 5 * time.Second
)

// ChronalDrift represents the time difference detected for a given beacon.
type ChronalDrift struct {
	Beacon string
	Drift  time.Duration
	Error  error
}

// fetchBeaconTime fetches the Date header from a given URL.
func fetchBeaconTime(client *http.Client, url string) (time.Time, error) {
	req, err := http.NewRequest("HEAD", url, nil)
	if err != nil {
		return time.Time{}, fmt.Errorf("failed to create request for %s: %w", url, err)
	}
	req.Header.Set("User-Agent", userAgent)

	resp, err := client.Do(req)
	if err != nil {
		return time.Time{}, fmt.Errorf("failed to reach beacon %s: %w", url, err)
	}
	defer resp.Body.Close()

	dateHeader := resp.Header.Get("Date")
	if dateHeader == "" {
		return time.Time{}, fmt.Errorf("no Date header found for beacon %s", url)
	}

	// Standard HTTP Date format: "Mon, 02 Jan 2006 15:04:05 GMT"
	t, err := time.Parse(time.RFC1123, dateHeader)
	if err != nil {
		return time.Time{}, fmt.Errorf("failed to parse Date header '%s' from beacon %s: %w", dateHeader, url, err)
	}
	return t, nil
}

// checkDrift concurrently checks the chronal drift for a single beacon.
func checkDrift(client *http.Client, beaconURL string, results chan<- ChronalDrift) {
	localTime := time.Now().UTC() // Use UTC for consistency

	remoteTime, err := fetchBeaconTime(client, beaconURL)
	if err != nil {
		results <- ChronalDrift{Beacon: beaconURL, Error: err}
		return
	}

	drift := remoteTime.Sub(localTime)
	results <- ChronalDrift{Beacon: beaconURL, Drift: drift}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-chronal-drift-detect <beacon_url_1> [beacon_url_2 ...]")
		os.Exit(1)
	}

	beaconURLs := os.Args[1:]
	results := make(chan ChronalDrift, len(beaconURLs))
	var wg sync.WaitGroup

	httpClient := &http.Client{
		Timeout: timeout,
	}

	fmt.Println("Initiating Chronal Drift Scan...")
	fmt.Printf("Local Chronometer: %s (UTC)\n", time.Now().UTC().Format(time.RFC1123))
	fmt.Println(strings.Repeat("-", 40))

	for _, url := range beaconURLs {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()
			checkDrift(httpClient, u, results)
		}(url)
	}

	wg.Wait()
	close(results)

	fmt.Println(strings.Repeat("-", 40))
	fmt.Println("Chronal Drift Report:")
	hasDrift := false
	for res := range results {
		if res.Error != nil {
			fmt.Printf("  [ERROR] Beacon %s: %v\n", res.Beacon, res.Error)
		} else {
			fmt.Printf("  [OK] Beacon %s: Drift %s\n", res.Beacon, res.Drift)
			if res.Drift.Abs() > 1*time.Second { // Arbitrary threshold for "significant" drift
				hasDrift = true
			}
		}
	}

	if hasDrift {
		fmt.Println("\nWarning: Significant chronal drift detected on one or more beacons. Temporal integrity may be compromised!")
		os.Exit(1) // Indicate an issue
	} else {
		fmt.Println("\nAll time-beacons appear synchronized within acceptable temporal parameters.")
		os.Exit(0)
	}
}
