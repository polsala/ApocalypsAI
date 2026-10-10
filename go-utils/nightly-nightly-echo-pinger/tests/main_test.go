package main

import (
	"bytes"
	"errors"
	"io/ioutil"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Helper to capture stdout
func captureOutput(f func()) string {
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	f()

	w.Close()
	out, _ := ioutil.ReadAll(r)
	os.Stdout = oldStdout
	return string(out)
}

// Helper to capture stderr
func captureErrorOutput(f func()) string {
	oldStderr := os.Stderr
	r, w, _ := os.Pipe()
	os.Stderr = w

	f()

	w.Close()
	out, _ := ioutil.ReadAll(r)
	os.Stderr = oldStderr
	return string(out)
}

func TestParsePingOutput(t *testing.T) {
	// Test successful parse
	outputSuccess := "PING google.com (142.250.186.142): 56 data bytes\n64 bytes from 142.250.186.142: icmp_seq=0 ttl=117 time=25.340 ms\n\n--- google.com ping statistics ---\n1 packets transmitted, 1 packets received, 0.0% packet loss\nround-trip min/avg/max/stddev = 25.340/25.340/25.340/0.000 ms\n"
	latency, err := parsePingOutput(outputSuccess)
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if latency != 25*time.Millisecond+340*time.Microsecond {
		t.Errorf("Expected latency of 25.34ms, got %v", latency)
	}

	// Test unreachable output
	outputUnreachable := "PING 192.168.1.254 (192.168.1.254): 56 data bytes\nRequest timeout for icmp_seq 0\n\n--- 192.168.1.254 ping statistics ---\n1 packets transmitted, 0 packets received, 100.0% packet loss\n"
	_, err = parsePingOutput(outputUnreachable)
	if err == nil || !strings.Contains(err.Error(), "unreachable") {
		t.Errorf("Expected 'unreachable' error, got %v", err)
	}

	// Test malformed output
	outputMalformed := "This is not a ping output\n"
	_, err = parsePingOutput(outputMalformed)
	if err == nil || !strings.Contains(err.Error(), "could not parse") {
		t.Errorf("Expected 'could not parse' error, got %v", err)
	}
}

func TestPingTarget(t *testing.T) {
	// # Mock rationale: Replace the actual ping command execution with a mock for deterministic testing.
	originalPingExecutor := pingExecutor
	defer func() { pingExecutor = originalPingExecutor }()

	// Test case 1: Successful ping
	pingExecutor = func(target string, count int) (string, error) {
		if target == "example.com" {
			return "time=10.50 ms", nil
		}
		return "", errors.New("unexpected target")
	}

	var wg sync.WaitGroup
	results := make(chan PingResult, 1)
	wg.Add(1)
	go pingTarget("example.com", &wg, results)
	wg.Wait()
	close(results)

	result := <-results
	if !result.Reachable {
		t.Errorf("Expected example.com to be reachable")
	}
	if result.Latency != 10*time.Millisecond+500*time.Microsecond {
		t.Errorf("Expected latency of 10.50ms, got %v", result.Latency)
	}
	if result.Target != "example.com" {
		t.Errorf("Expected target example.com, got %s", result.Target)
	}

	// Test case 2: Unreachable target
	pingExecutor = func(target string, count int) (string, error) {
		if target == "unreachable.host" {
			return "Request timeout for icmp_seq 0", errors.New("exit status 1") // Simulate ping failure
		}
		return "", errors.New("unexpected target")
	}

	wg = sync.WaitGroup{}
	results = make(chan PingResult, 1)
	wg.Add(1)
	go pingTarget("unreachable.host", &wg, results)
	wg.Wait()
	close(results)

	result = <-results
	if result.Reachable {
		t.Errorf("Expected unreachable.host to be unreachable")
	}
	if result.Error == nil || !strings.Contains(result.Error.Error(), "exit status 1") {
		t.Errorf("Expected an error for unreachable host, got %v", result.Error)
	}

	// Test case 3: Ping command error (e.g., host not found by system)
	pingExecutor = func(target string, count int) (string, error) {
		if target == "nonexistent.domain" {
			return "ping: cannot resolve nonexistent.domain: Unknown host", errors.New("exit status 2")
		}
		return "", errors.New("unexpected target")
	}

	wg = sync.WaitGroup{}
	results = make(chan PingResult, 1)
	wg.Add(1)
	go pingTarget("nonexistent.domain", &wg, results)
	wg.Wait()
	close(results)

	result = <-results
	if result.Reachable {
		t.Errorf("Expected nonexistent.domain to be unreachable")
	}
	if result.Error == nil || !strings.Contains(result.Error.Error(), "exit status 2") {
		t.Errorf("Expected an error for nonexistent domain, got %v", result.Error)
	}
}

func TestReadTargetsFromFile(t *testing.T) {
	// Create a temporary file for testing
	content := "google.com\n# This is a comment\n  example.org  \n\n192.168.1.1\n"
	tmpfile, err := ioutil.TempFile(".", "targets-*.txt")
	if err != nil {
		t.Fatalf("Failed to create temp file: %v", err)
	}
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	if _, err := tmpfile.WriteString(content); err != nil {
		t.Fatalf("Failed to write to temp file: %v", err)
	}

	targets, err := readTargetsFromFile(tmpfile.Name())
	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}

	expected := []string{"google.com", "example.org", "192.168.1.1"}
	if len(targets) != len(expected) {
		t.Fatalf("Expected %d targets, got %d: %v", len(expected), len(targets), targets)
	}

	for i, target := range targets {
		if target != expected[i] {
			t.Errorf("Expected target %s at index %d, got %s", expected[i], i, target)
		}
	}

	// Test non-existent file
	_, err = readTargetsFromFile("nonexistent-file.txt")
	if err == nil || !strings.Contains(err.Error(), "failed to open target file") {
		t.Errorf("Expected error for non-existent file, got %v", err)
	}
}

func TestMainFunction(t *testing.T) {
	// # Mock rationale: Replace the actual ping command execution with a mock for deterministic testing.
	originalPingExecutor := pingExecutor
	defer func() { pingExecutor = originalPingExecutor }()

	// Mock pingExecutor for main function tests
	pingExecutor = func(target string, count int) (string, error) {
		switch target {
		case "host1.com":
			return "time=10.00 ms", nil
		case "host2.com":
			return "Request timeout", errors.New("exit status 1")
		case "host3.com":
			return "time=50.00 ms", nil
		default:
			return "", errors.New("unknown host for mock")
		}
	}

	// Test with command-line arguments
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()

	os.Args = []string{"nightly-echo-pinger", "host1.com", "host2.com"}

	output := captureOutput(func() {
		main()
	})

	if !strings.Contains(output, "[host1.com] Echo Received! Latency: 10.00 ms") {
		t.Errorf("Expected host1.com success, got: %s", output)
	}
	if !strings.Contains(output, "[host2.com] Silence Detected. Target unreachable.") {
		t.Errorf("Expected host2.com failure, got: %s", output)
	}

	// Test with file input
	fileContent := "host1.com\nhost3.com\n"
	tmpfile, err := ioutil.TempFile(".", "main-targets-*.txt")
	if err != nil {
		t.Fatalf("Failed to create temp file: %v", err)
	}
	defer os.Remove(tmpfile.Name())
	defer tmpfile.Close()

	if _, err := tmpfile.WriteString(fileContent); err != nil {
		t.Fatalf("Failed to write to temp file: %v", err)
	}

	os.Args = []string{"nightly-echo-pinger", "-f", tmpfile.Name()}
	output = captureOutput(func() {
		main()
	})

	if !strings.Contains(output, "[host1.com] Echo Received! Latency: 10.00 ms") {
		t.Errorf("Expected host1.com success from file, got: %s", output)
	}
	if !strings.Contains(output, "[host3.com] Echo Received! Latency: 50.00 ms") {
		t.Errorf("Expected host3.com success from file, got: %s", output)
	}

	// Test no arguments
	os.Args = []string{"nightly-echo-pinger"}
	exitCode := 0
	oldExit := os.Exit
	defer func() { os.Exit = oldExit }()
	os.Exit = func(code int) { exitCode = code; panic("os.Exit was called") } // Use panic to stop execution

	errOutput := captureErrorOutput(func() {
		defer func() { recover() }() // Recover from panic
		main()
	})

	if exitCode != 1 {
		t.Errorf("Expected exit code 1 for no arguments, got %d", exitCode)
	}
	if !strings.Contains(errOutput, "Usage: nightly-echo-pinger") {
		t.Errorf("Expected usage message for no arguments, got: %s", errOutput)
	}
}
