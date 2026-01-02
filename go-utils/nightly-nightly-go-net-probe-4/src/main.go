package main

import (
	"flag"
	"fmt"
	"net"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"
)

type ProbeResult struct {
	Target      string
	IsUp        bool
	ResponseTime time.Duration
	Error       error
}

func probeEndpoint(target string, timeout time.Duration, wg *sync.WaitGroup, results chan<- ProbeResult) {
	defer wg.Done()

	startTime := time.Now()
	var result ProbeResult
	result.Target = target

	var err error

	// Try to parse as URL first
	u, urlErr := url.ParseRequestURI(target)
	if urlErr == nil && (u.Scheme == "http" || u.Scheme == "https") {
		client := http.Client{
			Timeout: timeout,
		}
		resp, httpErr := client.Get(target)
		if httpErr != nil {
			err = httpErr
		} else {
			defer resp.Body.Close()
			if resp.StatusCode >= 200 && resp.StatusCode < 300 {
				result.IsUp = true
			} else {
				err = fmt.Errorf("received status code %d", resp.StatusCode)
			}
		result.ResponseTime = time.Since(startTime)
		}
	} else {
		// Assume it's an IP:Port or hostname:Port
		conn, dialErr := net.DialTimeout("tcp", target, timeout)
		if dialErr != nil {
			err = dialErr
		} else {
			defer conn.Close()
			result.IsUp = true
			result.ResponseTime = time.Since(startTime)
		}
	}

	if err != nil {
		result.IsUp = false
		result.Error = err
	}

	results <- result
}

func main() {
	targetsStr := flag.String("targets", "", "Comma-separated list of network endpoints to probe (e.g., http://google.com,1.1.1.1:53)")
	timeout := flag.Duration("timeout", 5*time.Second, "Timeout for each probe")
	concurrency := flag.Int("concurrency", 10, "Maximum number of concurrent probes")

	flag.Parse()

	if *targetsStr == "" {
		fmt.Println("Error: --targets flag is required.")
		return
	}

	targets := strings.Split(*targetsStr, ",")

	var wg sync.WaitGroup
	results := make(chan ProbeResult, len(targets))

	// Use a semaphore to limit concurrency
	semaphore := make(chan struct{}, *concurrency)

	for _, target := range targets {
		if strings.TrimSpace(target) == "" {
			continue
		}
		wg.Add(1)
		semaphore <- struct{}{}
		go func(t string) {
			probeEndpoint(t, *timeout, &wg, results)
			<-semaphore // Release the semaphore slot
		}(strings.TrimSpace(target))
	}

	wg.Wait()
	close(results)

	// Process results
	for result := range results {
		if result.IsUp {
			fmt.Printf("[INFO] %s is UP (%.0fms)\n", result.Target, float64(result.ResponseTime.Microseconds())/1000.0)
		} else {
			fmt.Printf("[ERROR] %s is DOWN (%v)\n", result.Target, result.Error)
		}
	}
}
