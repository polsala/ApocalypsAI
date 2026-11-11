package main

import (
	"fmt"
	"net/http"
	"os"
	"sync"
)

func fetchURL(url string, wg *sync.WaitGroup, results chan<- string) {
	defer wg.Done()

	resp, err := http.Get(url)
	if err != nil {
		results <- fmt.Sprintf("URL: %s, Error: %v", url, err)
		return
	}
	defer resp.Body.Close()

	results <- fmt.Sprintf("URL: %s, Status: %d %s", url, resp.StatusCode, resp.Status)
}

func main() {
	urls := os.Args[1:]

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher <url1> <url2> ...")
		return
	}

	var wg sync.WaitGroup
	results := make(chan string, len(urls))

	for _, url := range urls {
		wg.Add(1)
		go fetchURL(url, &wg, results)
	}

	wg.Wait()
	close(results)

	for res := range results {
		fmt.Println(res)
	}
}
