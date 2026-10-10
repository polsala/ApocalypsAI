package main

import (
	"bufio"
	"flag"
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

// PingResult holds the outcome of a single chrono-ping.
type PingResult struct {
	URL        string
	StatusCode int
	Latency    time.Duration
	Error      error
}

// PingURL sends an HTTP GET request to the given URL and measures its latency.
// It is exported for testing purposes.
func PingURL(url string, timeout time.Duration) PingResult {
	client := http.Client{
		Timeout: timeout,
	}

	start := time.Now()
	resp, err := client.Get(url)
	latency := time.Since(start)

	if err != nil {
		return PingResult{URL: url, Latency: latency, Error: err}
	}
	defer resp.Body.Close()

	return PingResult{URL: url, StatusCode: resp.StatusCode, Latency: latency, Error: nil}
}

func main() {
	var ( // Declare flags
		filePath string
		timeoutStr string
	)

	flag.StringVar(&filePath, "f", "", "Path to a file containing URLs (one per line)")
	flag.StringVar(&timeoutStr, "t", "5s", "Timeout for each HTTP request (e.g., 1s, 500ms)")
	flag.Parse()

	timeout, err := time.ParseDuration(timeoutStr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error parsing timeout duration: %v\n", err)
		os.Exit(1)
	}

	var urls []string

	if filePath != "" {
		file, err := os.Open(filePath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error opening URL file: %v\n", err)
			os.Exit(1)
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := strings.TrimSpace(scanner.Text())
			if line != "" && !strings.HasPrefix(line, "#") {
				urls = append(urls, line)
			}
		}
		if err := scanner.Err(); err != nil {
			fmt.Fprintf(os.Stderr, "Error reading URL file: %v\n", err)
			os.Exit(1)
		}
	} else {
		urls = flag.Args()
	}

	if len(urls) == 0 {
		fmt.Println("No URLs provided. Use 'chrono-ping-dispatcher <url1> ...' or 'chrono-ping-dispatcher -f urls.txt'")
		flag.Usage()
		os.Exit(1)
	}

	var wg sync.WaitGroup
	results := make(chan PingResult, len(urls))

	fmt.Println("Chrono-Ping Dispatcher initiating temporal probes...")
	for _, url := range urls {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()
			results <- PingURL(u, timeout)
		}(url)
	}

	wg.Wait()
	close(results)

	fmt.Println("\nChrono-Ping Report:\n-------------------")
	for res := range results {
		fmt.Printf("URL: %s\n", res.URL)
		if res.Error != nil {
			fmt.Printf("  Status: %d\n", res.StatusCode) // Status code might be 0 on error
			fmt.Printf("  Latency: %s\n", res.Latency)
			fmt.Printf("  Error: %v\n", res.Error)
		} else {
			fmt.Printf("  Status: %d %s\n", res.StatusCode, http.StatusText(res.StatusCode))
			fmt.Printf("  Latency: %s\n", res.Latency)
			fmt.Printf("  Error: <nil>\n")
		}
		fmt.Println("")
	}
	fmt.Println("-------------------")
	fmt.Println("Report Complete. Temporal stability assessed.")
}
