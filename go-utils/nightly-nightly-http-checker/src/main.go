package main

import (
	"bufio"
	"flag"
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)

type Result struct {
	URL    string
	Status string
}

func CheckURLs(urls []string, concurrency int) ([]Result, error) {
	results := make([]Result, len(urls))
	var wg sync.WaitGroup
	sem := make(chan struct{}, concurrency)
	client := &http.Client{
		Timeout: 5 * time.Second,
	}

	for i, url := range urls {
		wg.Add(1)
		go func(idx int, u string) {
			defer wg.Done()
			sem <- struct{}{}
			defer func() { <-sem }()
			resp, err := client.Get(u)
			if err != nil {
				results[idx] = Result{URL: u, Status: fmt.Sprintf("error: %v", err)}
				return
			}
			defer resp.Body.Close()
			results[idx] = Result{URL: u, Status: fmt.Sprintf("%d %s", resp.StatusCode, http.StatusText(resp.StatusCode))}
		}(i, url)
	}
	wg.Wait()
	return results, nil
}

func readURLsFromFile(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	var urls []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if line != "" {
			urls = append(urls, line)
		}
	}
	return urls, scanner.Err()
}

func readURLsFromStdin() ([]string, error) {
	var urls []string
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		if line != "" {
			urls = append(urls, line)
		}
	}
	return urls, scanner.Err()
}

func main() {
	var filePath string
	var concurrency int
	flag.StringVar(&filePath, "f", "", "Path to file containing URLs (one per line). If omitted, reads from stdin.")
	flag.IntVar(&concurrency, "c", 10, "Number of concurrent workers.")
	flag.Parse()

	var urls []string
	var err error
	if filePath != "" {
		urls, err = readURLsFromFile(filePath)
	} else {
		urls, err = readURLsFromStdin()
	}
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error reading URLs: %v\n", err)
		os.Exit(1)
	}
	if len(urls) == 0 {
		fmt.Fprintln(os.Stderr, "No URLs provided.")
		os.Exit(1)
	}

	results, _ := CheckURLs(urls, concurrency)
	for _, r := range results {
		fmt.Printf("%s -> %s\n", r.URL, r.Status)
	}
}
