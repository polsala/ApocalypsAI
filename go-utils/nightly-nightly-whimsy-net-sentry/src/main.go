package main

import (
	"fmt"
	"net/http"
	"os"
	"time"
)

func checkEndpoint(url string, ch chan<- string) {
	resp, err := http.Head(url)
	status := "⚠️ UNKNOWN"
	if err == nil {
		status = fmt.Sprintf("✅ %d", resp.StatusCode)
		resp.Body.Close()
	} else {
		status = "❌ DOWN"
	}
	ch <- fmt.Sprintf("[%s] %s", status, url)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "Usage: whimsy-net-sentry URL...")
		os.Exit(1)
	}

	ch := make(chan string)
	for _, url := range os.Args[1:] {
		go checkEndpoint(url, ch)
	}

	results := make([]string, 0, len(os.Args)-1)
	for i := 0; i < len(os.Args)-1; i++ {
		results = append(results, <-ch)
	}

	fmt.Println("\n--- NETWORK SURVIVAL REPORT ---")
	for _, r := range results {
		fmt.Println(r)
	}
	fmt.Println("--- END OF TRANSMISSION ---\n")
}
