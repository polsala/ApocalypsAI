package main

import (
	"bytes"
	"log"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
	"time"
)

func TestMain(t *testing.T) {
	// Mock os.Args to simulate command-line arguments
	originalArgs := os.Args
	defer func() {
		os.Args = originalArgs
	}()

	// Mock logger to capture output
	var buf bytes.Buffer
	log.SetOutput(&buf)
	defer func() {
		log.SetOutput(os.Stderr)
	}()

	// Test case 1: Valid URLs
	t.Run("valid_urls", func(t *testing.T) {
		// Mock HTTP server
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			// Mock rationale: Simulate a delay to test timeout and duration reporting
			time.Sleep(50 * time.Millisecond)
			w.WriteHeader(http.StatusOK)
			w.Write([]byte("OK"))
		}))
		defer server.Close()

		os.Args = []string{"cmd", server.URL, server.URL + "/another"}
		main()

		output := buf.String()
		if !strings.Contains(output, "[SUCCESS] "+server.URL+" - Status: 200 OK") {
			t.Errorf("Expected success for %s, but got:\n%s", server.URL, output)
		}
		if !strings.Contains(output, "[SUCCESS] "+server.URL+"/another"+" - Status: 200 OK") {
			t.Errorf("Expected success for %s/another, but got:\n%s", server.URL, output)
		}
		if strings.Contains(output, "[ERROR]") {
			t.Errorf("Did not expect errors for valid URLs, but got:\n%s", output)
		}
		buf.Reset()
	})

	// Test case 2: Invalid URL (non-existent domain)
	t.Run("invalid_url_domain", func(t *testing.T) {
		os.Args = []string{"cmd", "http://nonexistent.domain.xyz"}
		main()

		output := buf.String()
		if !strings.Contains(output, "[ERROR] http://nonexistent.domain.xyz - Error: Get \"http://nonexistent.domain.xyz\": dial tcp: lookup nonexistent.domain.xyz: no such host") {
			t.Errorf("Expected error for nonexistent domain, but got:\n%s", output)
		}
		buf.Reset()
	})

	// Test case 3: Invalid URL (timeout)
	t.Run("invalid_url_timeout", func(t *testing.T) {
		// Mock HTTP server that delays indefinitely
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			// Mock rationale: Simulate a long delay to trigger the client timeout
			time.Sleep(15 * time.Second) // Longer than the client timeout
			w.WriteHeader(http.StatusOK)
			w.Write([]byte("OK"))
		}))
		defer server.Close()

		os.Args = []string{"cmd", server.URL}
		main()

		output := buf.String()
		if !strings.Contains(output, "[ERROR] "+server.URL+" - Error: Get \""+server.URL+"\": context deadline exceeded") {
			t.Errorf("Expected timeout error, but got:\n%s", output)
		}
		buf.Reset()
	})

	// Test case 4: No URLs provided
	t.Run("no_urls", func(t *testing.T) {
		os.Args = []string{"cmd"}
		// Expecting main to exit with an error, so we defer the check
		defer func() {
			if r := recover(); r == nil {
				t.Errorf("The program did not panic when no URLs were provided")
			}
		}()
		main()
	})
}
