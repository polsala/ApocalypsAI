package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock implementations for testing network operations.
// Mock rationale: These functions replace actual network calls with predefined, deterministic results,
// allowing tests to run offline and consistently without external dependencies or network flakiness.

func mockPing(host string, timeout time.Duration) (time.Duration, error) {
	switch host {
	case "good.example.com":
		return 50 * time.Millisecond, nil
	case "slow.example.com":
		return 150 * time.Millisecond, nil // Above 100ms threshold
	case "fail.example.com":
		return 0, fmt.Errorf("mock ping failed for %s", host)
	case "8.8.8.8":
		return 50 * time.Millisecond, nil
	case "1.1.1.1":
		return 120 * time.Millisecond, nil // Will trigger warning in main test
	default:
		return 0, fmt.Errorf("unknown mock host: %s", host)
	}
}

func mockLookupHost(host string) ([]string, error) {
	switch host {
	case "google.com":
		return []string{"142.250.190.142"}, nil
	case "cloudflare.com":
		return []string{"104.16.132.229"}, nil
	case "unknown.domain":
		return nil, fmt.Errorf("mock DNS lookup failed for %s", host)
	case "mismatched.domain":
		return []string{"1.2.3.4"}, nil // For expected IP mismatch test
	default:
		return nil, fmt.Errorf("unknown mock domain: %s", host)
	}
}

func mockHTTPGet(url string, timeout time.Duration) (*http.Response, error) {
	switch url {
	case "https://good.example.com":
		return &http.Response{StatusCode: 200, Body: ioutil.NopCloser(bytes.NewBufferString("OK"))}, nil
	case "https://badstatus.example.com":
		return &http.Response{StatusCode: 500, Body: ioutil.NopCloser(bytes.NewBufferString("Internal Server Error"))}, nil
	case "https://timeout.example.com":
		return nil, fmt.Errorf("mock http timeout for %s", url)
	case "https://www.google.com":
		return &http.Response{StatusCode: 200, Body: ioutil.NopCloser(bytes.NewBufferString("OK"))}, nil
	case "https://www.github.com":
		return &http.Response{StatusCode: 500, Body: ioutil.NopCloser(bytes.NewBufferString("Error"))}, nil // Will trigger warning in main test
	default:
		return nil, fmt.Errorf("unknown mock URL: %s", url)
	}
}

func TestPerformHostCheck(t *testing.T) {
	// Temporarily replace real functions with mocks for this test suite.
	originalPingFunc := pingFunc
	pingFunc = mockPing
	defer func() { pingFunc = originalPingFunc }() // Restore after test completes.

	tests := []struct {
		name     string
		check    HostCheck
		expected string
	}{
		{"Good Host", HostCheck{Address: "good.example.com", ThresholdMs: 100}, "OK"},
		{"Slow Host", HostCheck{Address: "slow.example.com", ThresholdMs: 100}, "WARNING"},
		{"Failed Host", HostCheck{Address: "fail.example.com", ThresholdMs: 100}, "ERROR"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var wg sync.WaitGroup
			results := make(chan CheckResult, 1)
			wg.Add(1)
			go performHostCheck(tt.check, results, &wg)
			wg.Wait()
			close(results)
			res := <-results
			if res.Status != tt.expected {
				t.Errorf("Expected status %s, got %s for %s. Message: %s", tt.expected, res.Status, tt.check.Address, res.Message)
			}
		})
	}
}

func TestPerformDNSCheck(t *testing.T) {
	originalLookupHostFunc := lookupHostFunc
	lookupHostFunc = mockLookupHost
	defer func() { lookupHostFunc = originalLookupHostFunc }()

	tests := []struct {
		name     string
		check    DNSCheck
		expected string
	}{
		{"Good DNS with Expected IPs", DNSCheck{Domain: "google.com", ExpectedIPs: []string{"142.250.190.142"}}, "OK"},
		{"Good DNS without Expected IPs", DNSCheck{Domain: "cloudflare.com"}, "OK"},
		{"Failed DNS Lookup", DNSCheck{Domain: "unknown.domain"}, "ERROR"},
		{"Mismatched Expected IPs", DNSCheck{Domain: "mismatched.domain", ExpectedIPs: []string{"9.9.9.9"}}, "WARNING"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var wg sync.WaitGroup
			results := make(chan CheckResult, 1)
			wg.Add(1)
			go performDNSCheck(tt.check, results, &wg)
			wg.Wait()
			close(results)
			res := <-results
			if res.Status != tt.expected {
				t.Errorf("Expected status %s, got %s for %s. Message: %s", tt.expected, res.Status, tt.check.Domain, res.Message)
			}
		})
	}
}

func TestPerformHTTPCheck(t *testing.T) {
	originalHTTPGetFunc := httpGetFunc
	httpGetFunc = mockHTTPGet
	defer func() { httpGetFunc = originalHTTPGetFunc }()

	tests := []struct {
		name     string
		check    HTTPCheck
		expected string
	}{
		{"Good HTTP Status", HTTPCheck{URL: "https://good.example.com", ExpectedStatus: 200, TimeoutMs: 5000}, "OK"},
		{"Bad HTTP Status", HTTPCheck{URL: "https://badstatus.example.com", ExpectedStatus: 200, TimeoutMs: 5000}, "WARNING"},
		{"Failed HTTP Request", HTTPCheck{URL: "https://timeout.example.com", ExpectedStatus: 200, TimeoutMs: 5000}, "ERROR"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var wg sync.WaitGroup
			results := make(chan CheckResult, 1)
			wg.Add(1)
			go performHTTPCheck(tt.check, results, &wg)
			wg.Wait()
			close(results)
			res := <-results
			if res.Status != tt.expected {
				t.Errorf("Expected status %s, got %s for %s. Message: %s", tt.expected, res.Status, tt.check.URL, res.Message)
			}
		})
	}
}

// Test the main function's output for overall summary and specific messages.
// This test captures stdout to verify the end-to-end output of the main program
// when run with mocked network dependencies.
func TestMainFunctionOutput(t *testing.T) {
	// Mock all network functions to ensure deterministic output for the main function.
	originalPingFunc := pingFunc
	originalLookupHostFunc := lookupHostFunc
	originalHTTPGetFunc := httpGetFunc
	defer func() {
		pingFunc = originalPingFunc
		lookupHostFunc = originalLookupHostFunc
		httpGetFunc = originalHTTPGetFunc
	}()

	// Apply specific mocks for the main function's hardcoded checks.
	pingFunc = mockPing
	lookupHostFunc = func(host string) ([]string, error) {
		if host == "google.com" { return []string{"142.250.190.142"}, nil }
		if host == "cloudflare.com" { return nil, fmt.Errorf("mock dns error for cloudflare.com") } // Will trigger error
		return nil, fmt.Errorf("mock dns error for %s", host)
	}
	httpGetFunc = mockHTTPGet

	// Capture stdout to inspect the main function's printed output.
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	main() // Run the main function with mocked dependencies.

	w.Close()
	out, _ := ioutil.ReadAll(r)
	os.Stdout = oldStdout // Restore stdout.

	output := string(out)

	// Verify expected messages and overall status in the captured output.
	// Check for OK messages.
	if !strings.Contains(output, "[OK] 8.8.8.8: Host 8.8.8.8 responds with a harmonious 50ms. All is stable.") {
		t.Errorf("Expected OK message for 8.8.8.8 not found in output:\n%s", output)
	}
	if !strings.Contains(output, "[OK] google.com: The ancient scrolls for google.com confirm the IPs: [142.250.190.142]. All is stable.") {
		t.Errorf("Expected OK message for google.com not found in output:\n%s", output)
	}
	if !strings.Contains(output, "[OK] https://www.google.com: The digital gates of https://www.google.com respond with a harmonious 200 OK.") {
		t.Errorf("Expected OK message for https://www.google.com not found in output:\n%s", output)
	}

	// Check for WARNING messages.
	if !strings.Contains(output, "[WARNING] 1.1.1.1: A temporal distortion of 120ms detected on 1.1.1.1! The network fabric shimmers.") {
		t.Errorf("Expected WARNING message for 1.1.1.1 not found in output:\n%s", output)
	}
	if !strings.Contains(output, "[WARNING] https://www.github.com: The digital gates of https://www.github.com respond with an unsettling 500. Expected 200.") {
		t.Errorf("Expected WARNING message for https://www.github.com not found in output:\n%s", output)
	}

	// Check for ERROR messages.
	if !strings.Contains(output, "[ERROR] cloudflare.com: The ancient scrolls for cloudflare.com are unreadable: mock dns error for cloudflare.com") {
		t.Errorf("Expected ERROR message for cloudflare.com not found in output:\n%s", output)
	}

	// Check for the overall summary message indicating warnings/errors.
	if !strings.Contains(output, "Beware! The network fabric shows signs of instability. Further investigation advised.") {
		t.Errorf("Expected overall warning message not found in output:\n%s", output)
	}

	// Ensure the 'calm' message is NOT present when there are warnings/errors.
	if strings.Contains(output, "The network fabric is calm. No significant echoes or distortions detected.") {
		t.Errorf("Unexpected 'calm' message found in output when warnings/errors were present:\n%s", output)
	}
}
