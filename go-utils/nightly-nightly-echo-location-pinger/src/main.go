package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"sync"
	"time"
)

type PingResult struct {
	URL     string
	Latency time.Duration
	Err     error
}

// pingURL performs an HTTP GET request to the given URL and measures the latency.
func pingURL(url string) PingResult {
	start := time.Now()
	resp, err := http.Get(url)
	latency := time.Since(start)

	if err != nil {
		return PingResult{URL: url, Latency: latency, Err: fmt.Errorf("failed to ping %s: %w", url, err)}
	}
	defer resp.Body.Close()

	// Read body to ensure full response is received and accounted for in latency
	_, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		return PingResult{URL: url, Latency: latency, Err: fmt.Errorf("failed to read response body from %s: %w", url, err)}
	}

	if resp.StatusCode != http.StatusOK {
		return PingResult{URL: url, Latency: latency, Err: fmt.Errorf("non-OK status code %d from %s", resp.StatusCode, url)}
	}

	return PingResult{URL: url, Latency: latency, Err: nil}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run src/main.go <url1> [url2]...")
		osExit(1)
	}

	urls := os.Args[1:]
	results := make(chan PingResult, len(urls))
	var wg sync.WaitGroup

	fmt.Println("--- Initiating Echo-Location Pings ---")

	for _, url := range urls {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()
			fmt.Printf("Pinging %s...\n", u)
			results <- pingURL(u)
		}(url)
	}

	wg.Wait()
	close(results)

	fmt.Println("\n--- Echo-Location Report ---")
	for res := range results {
		if res.Err != nil {
			fmt.Printf("%s: Error - %v\n", res.URL, res.Err)
		} else {
			fmt.Printf("%s: %s\n", res.URL, res.Latency.Round(time.Millisecond).String())
		}
	}
	fmt.Println("----------------------------")
}

// osExit is a variable that can be overridden for testing os.Exit
var osExit = os.Exit
