package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// MockResponse creates a test HTTP server that responds with the given status code.
func MockResponse(statusCode int, body string) *httptest.Server {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(statusCode)
		w.Write([]byte(body))
	}))
	return server
}

// MockNetworkErrorServer creates a test HTTP server that always returns a network error.
func MockNetworkErrorServer() *httptest.Server {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// This handler will never be reached if the client itself errors out before sending.
		// For testing client-side errors like connection refused, we rely on the http.Client's behavior.
		// A simple way to simulate a server that causes issues is to make it slow or unresponsive.
		// However, for deterministic tests, we'll mock the client's Get method in a more robust way if needed.
		// For this simple case, we'll rely on the fact that a non-existent domain will cause a DNS error.
		// Or, we can make the server itself return an error if the client tries to connect.
		// For now, we'll simulate a server that just doesn't respond in time for a timeout test.
		// For actual network errors like connection refused, the http.Client will handle it.
		// We'll use a non-existent domain in tests to trigger DNS errors.
		panic("This should not be reached in a network error test scenario")
	}))
	return server
}

func TestConcurrentFetcher(t *testing.T) {
	// Mock servers
	server200 := MockResponse(http.StatusOK, "OK")
	defer server200.Close()

	server404 := MockResponse(http.StatusNotFound, "Not Found")
	defer server404.Close()

	// Mock a server that will cause a timeout
	serverTimeout := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(5 * time.Second) // Sleep longer than the test timeout
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Too slow!"))
	}))
	defer serverTimeout.Close()

	// A non-existent domain to simulate DNS errors
	nonExistentDomain := "http://localhost.nonexistentdomain.invalid"

	tests := []struct {
		name         string
		urls         []string
		timeout      time.Duration
		expectedLen  int
		checkResults func([]FetchResult) bool
	}{
		{
			name:        "Basic fetch with 200 and 404",
			urls:        []string{server200.URL, server404.URL},
			timeout:     5 * time.Second,
			expectedLen: 2,
			checkResults: func(results []FetchResult) bool {
				found200 := false
				found404 := false
				for _, res := range results {
					if res.URL == server200.URL {
						if res.StatusCode != http.StatusOK || res.Error != "" {
							treturn false
						}
						found200 = true
					}
					if res.URL == server404.URL {
						if res.StatusCode != http.StatusNotFound || res.Error != "" {
							treturn false
						}
						found404 = true
					}
				}
				return found200 && found404
			},
		},
		{
			name:        "Timeout test",
			urls:        []string{serverTimeout.URL},
			timeout:     2 * time.Second, // Shorter than server sleep
			expectedLen: 1,
			checkResults: func(results []FetchResult) bool {
				if len(results) != 1 {
					return false
				}
				res := results[0]
				// Expecting a timeout error, status code might be 0 or the last one before timeout
				// The exact error message can vary, so we check for the presence of an error string.
				return res.Error != "" && strings.Contains(res.Error, "Client.Timeout")
			},
		},
		{
			name:        "Non-existent domain test",
			urls:        []string{nonExistentDomain},
			timeout:     5 * time.Second,
			expectedLen: 1,
			checkResults: func(results []FetchResult) bool {
				if len(results) != 1 {
					return false
				}
				res := results[0]
				// Expecting a DNS lookup error
				return res.Error != "" && strings.Contains(res.Error, "lookup")
			},
		},
		{
			name:        "Empty URL list",
			urls:        []string{}, // Should be handled by main function's arg check, but good to test channel behavior
			timeout:     5 * time.Second,
			expectedLen: 0,
			checkResults: func(results []FetchResult) bool {
				return len(results) == 0
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Mock the main function's behavior for testing
			// We need to capture the output and the results channel
			// This requires a bit of refactoring or using a test harness.
			// For simplicity, we'll simulate the core logic directly.

			resultsChan := make(chan FetchResult, len(tt.urls))
			var wg sync.WaitGroup

			client := &http.Client{
				Timeout: tt.timeout,
			}

			for _, url := range tt.urls {
				wg.Add(1)
				go fetchURL(url, client, resultsChan, &wg)
			}

			go func() {
				wg.Wait()
				close(resultsChan)
			}()

			var actualResults []FetchResult
			for res := range resultsChan {
				actualResults = append(actualResults, res)
			}

			if len(actualResults) != tt.expectedLen {
				t.Errorf("Expected %d results, got %d", tt.expectedLen, len(actualResults))
				return
			}

			if !tt.checkResults(actualResults) {
				// Print detailed results for debugging
				var sb strings.Builder
				sb.WriteString("Result check failed. Actual results:\n")
				for _, res := range actualResults {
					statusCodeStr := "N/A"
					if res.StatusCode != 0 {
						statusCodeStr = fmt.Sprintf("%d", res.StatusCode)
					}
					sb.WriteString(fmt.Sprintf("  URL: %s, Status: %s, ResponseTime: %s, Error: %s\n", res.URL, statusCodeStr, res.ResponseTime.Round(time.Millisecond), res.Error))
				}
				t.Error(sb.String())
			}
		})
	}
}

// Mock rationale: The httptest package is used to create mock HTTP servers. 
// This allows us to simulate different server responses (e.g., 200 OK, 404 Not Found, slow responses, or servers that cause network errors) 
// without making actual network calls. This ensures tests are deterministic, fast, and can run offline.
// The nonExistentDomain simulates DNS lookup failures, which are common network errors.
