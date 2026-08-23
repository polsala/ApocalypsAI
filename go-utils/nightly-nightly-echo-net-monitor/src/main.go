package main

import (
	"fmt"
	"net"
	"net/http"
	"sync"
	"time"
)

// Define types for checks
type HostCheck struct {
	Address     string
	ThresholdMs int // Milliseconds
}

type DNSCheck struct {
	Domain      string
	ExpectedIPs []string // Optional, for specific IP validation
}

type HTTPCheck struct {
	URL           string
	ExpectedStatus int
	TimeoutMs     int // Milliseconds
}

// Result types
type CheckResult struct {
	Type    string
	Target  string
	Status  string
	Message string
}

// Mockable functions for network operations
// These global variables allow tests to replace the real network functions with mock versions.
var (
	pingFunc      func(host string, timeout time.Duration) (time.Duration, error)
	lookupHostFunc func(host string) ([]string, error)
	httpGetFunc    func(url string, timeout time.Duration) (*http.Response, error)
)

func init() {
	// Default to real implementations when the program starts
	pingFunc = realPing
	lookupHostFunc = realLookupHost
	httpGetFunc = realHTTPGet
}

// realPing attempts to establish a TCP connection to the host on port 80
// to simulate basic reachability and latency. This is not an ICMP ping.
func realPing(host string, timeout time.Duration) (time.Duration, error) {
	start := time.Now()
	conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, "80"), timeout)
	if err != nil {
		// Try port 443 if 80 fails, common for many services
		conn, err = net.DialTimeout("tcp", net.JoinHostPort(host, "443"), timeout)
		if err != nil {
			return 0, fmt.Errorf("failed to dial %s (ports 80/443): %w", host, err)
		}
	}
	defer conn.Close()
	return time.Since(start), nil
}

// realLookupHost performs a standard DNS lookup.
func realLookupHost(host string) ([]string, error) {
	return net.LookupHost(host)
}

// realHTTPGet performs an HTTP GET request.
func realHTTPGet(url string, timeout time.Duration) (*http.Response, error) {
	client := http.Client{
		Timeout: timeout,
	}
	return client.Get(url)
}

// performHostCheck executes a host reachability check and reports the result.
func performHostCheck(check HostCheck, results chan<- CheckResult, wg *sync.WaitGroup) {
	defer wg.Done()
	// Give the ping function a bit more time than the threshold to complete
	latency, err := pingFunc(check.Address, time.Duration(check.ThresholdMs)*time.Millisecond*2)
	if err != nil {
		results <- CheckResult{"Host", check.Address, "ERROR", fmt.Sprintf("The host %s is lost in the void: %v", check.Address, err)}
		return
	}

	if latency.Milliseconds() > int64(check.ThresholdMs) {
		results <- CheckResult{"Host", check.Address, "WARNING", fmt.Sprintf("A temporal distortion of %dms detected on %s! The network fabric shimmers.", latency.Milliseconds(), check.Address)}
	} else {
		results <- CheckResult{"Host", check.Address, "OK", fmt.Sprintf("Host %s responds with a harmonious %dms. All is stable.", check.Address, latency.Milliseconds())}
	}
}

// performDNSCheck executes a DNS lookup and validates IPs if expected ones are provided.
func performDNSCheck(check DNSCheck, results chan<- CheckResult, wg *sync.WaitGroup) {
	defer wg.Done()
	ips, err := lookupHostFunc(check.Domain)
	if err != nil {
		results <- CheckResult{"DNS", check.Domain, "ERROR", fmt.Sprintf("The ancient scrolls for %s are unreadable: %v", check.Domain, err)}
		return
	}

	if len(check.ExpectedIPs) > 0 {
		foundExpected := false
		for _, expectedIP := range check.ExpectedIPs {
			for _, actualIP := range ips {
				if expectedIP == actualIP {
					foundExpected = true
					break
				}
			}
			if foundExpected {
				break
			}
		}
		if !foundExpected {
			results <- CheckResult{"DNS", check.Domain, "WARNING", fmt.Sprintf("The ancient scrolls for %s reveal unexpected IPs: %v. Expected one of: %v", check.Domain, ips, check.ExpectedIPs)}
			return
		}
	}
	results <- CheckResult{"DNS", check.Domain, "OK", fmt.Sprintf("The ancient scrolls for %s confirm the IPs: %v. All is stable.", check.Domain, ips)}
}

// performHTTPCheck executes an HTTP GET request and validates the status code.
func performHTTPCheck(check HTTPCheck, results chan<- CheckResult, wg *sync.WaitGroup) {
	defer wg.Done()
	resp, err := httpGetFunc(check.URL, time.Duration(check.TimeoutMs)*time.Millisecond)
	if err != nil {
		results <- CheckResult{"HTTP", check.URL, "ERROR", fmt.Sprintf("The digital gates of %s are unresponsive: %v", check.URL, err)}
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != check.ExpectedStatus {
		results <- CheckResult{"HTTP", check.URL, "WARNING", fmt.Sprintf("The digital gates of %s respond with an unsettling %d. Expected %d.", check.URL, resp.StatusCode, check.ExpectedStatus)}
	} else {
		results <- CheckResult{"HTTP", check.URL, "OK", fmt.Sprintf("The digital gates of %s respond with a harmonious %d OK.", check.URL, resp.StatusCode)}
	}
}

func main() {
	fmt.Println("Initiating Nightly Echo Net Monitor...")

	// Hardcoded checks for simplicity. In a real-world scenario, these would be loaded from a config file.
	hostChecks := []HostCheck{
		{Address: "8.8.8.8", ThresholdMs: 100},
		{Address: "1.1.1.1", ThresholdMs: 100},
	}

	dnsChecks := []DNSCheck{
		{Domain: "google.com", ExpectedIPs: []string{"142.250.190.142"}}, // Example IP, might change over time
		{Domain: "cloudflare.com"}, // No specific IP expected, just resolve
	}

	httpChecks := []HTTPCheck{
		{URL: "https://www.google.com", ExpectedStatus: 200, TimeoutMs: 5000},
		{URL: "https://www.github.com", ExpectedStatus: 200, TimeoutMs: 5000},
	}

	var wg sync.WaitGroup
	results := make(chan CheckResult, len(hostChecks)+len(dnsChecks)+len(httpChecks))

	for _, hc := range hostChecks {
		wg.Add(1)
		go performHostCheck(hc, results, &wg)
	}

	for _, dc := range dnsChecks {
		wg.Add(1)
		go performDNSCheck(dc, results, &wg)
	}

	for _, htc := range httpChecks {
		wg.Add(1)
		go performHTTPCheck(htc, results, &wg)
	}

	wg.Wait()
	close(results)

	fmt.Println("\n--- Echoes from the Network Fabric ---")
	hasWarnings := false
	for res := range results {
		fmt.Printf("[%s] %s: %s\n", res.Status, res.Target, res.Message)
		if res.Status == "WARNING" || res.Status == "ERROR" {
			hasWarnings = true
		}
	}

	if hasWarnings {
		fmt.Println("\nBeware! The network fabric shows signs of instability. Further investigation advised.")
	} else {
		fmt.Println("\nThe network fabric is calm. No significant echoes or distortions detected.")
	}
}
