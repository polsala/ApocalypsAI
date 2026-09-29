package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"os"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"time"
)

type PingResult struct {
	Target    string
	Latency   time.Duration
	Reachable bool
	Error     error
}

// pingExecutor is a function type that can be swapped for testing.
// # Mock rationale: Allows mocking os/exec.Command for deterministic, offline tests.
var pingExecutor = defaultPingExecutor

func defaultPingExecutor(target string, count int) (string, error) {
	cmd := exec.Command("ping", "-c", strconv.Itoa(count), target)
	out, err := cmd.CombinedOutput()
	return string(out), err
}

func parsePingOutput(output string) (time.Duration, error) {
	// Regex to find latency, e.g., "time=25.34 ms"
	// This regex is specific to Linux/macOS ping output. Windows ping output differs.
	// For cross-platform, a more robust solution or a pure Go ICMP library would be needed.
	// For this utility, we assume a Unix-like ping output.
	re := regexp.MustCompile(`time=(\d+\.?\d*)\s*ms`)
	matches := re.FindStringSubmatch(output)

	if len(matches) > 1 {
		latencyMs, err := strconv.ParseFloat(matches[1], 64)
		if err != nil {
			return 0, fmt.Errorf("failed to parse latency: %w", err)
		}
		return time.Duration(latencyMs * float64(time.Millisecond)), nil
	}

	// Check for common 'unreachable' or 'timeout' indicators
	if strings.Contains(output, "Destination Host Unreachable") ||
		strings.Contains(output, "Request timeout for icmp_seq") ||
		strings.Contains(output, "100% packet loss") {
		return 0, fmt.Errorf("target unreachable or timed out")
	}

	return 0, fmt.Errorf("could not parse ping output or target unreachable")
}

func pingTarget(target string, wg *sync.WaitGroup, results chan<- PingResult) {
	defer wg.Done()

	output, err := pingExecutor(target, 1)

	if err != nil {
		results <- PingResult{Target: target, Reachable: false, Error: err}
		return
	}

	latency, parseErr := parsePingOutput(output)
	if parseErr != nil {
		results <- PingResult{Target: target, Reachable: false, Error: parseErr}
		return
	}

	results <- PingResult{Target: target, Latency: latency, Reachable: true}
}

func readTargetsFromFile(filePath string) ([]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open target file: %w", err)
	}
	defer file.Close()

	var targets []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" && !strings.HasPrefix(line, "#") {
			targets = append(targets, line)
		}
	}

	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("error reading target file: %w", err)
	}

	return targets, nil
}

func main() {
	filePath := flag.String("f", "", "Path to a file containing targets (one per line)")
	flag.Parse()

	var targets []string
	if *filePath != "" {
		var err error
		targets, err = readTargetsFromFile(*filePath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}
	} else {
		targets = flag.Args()
	}

	if len(targets) == 0 {
		fmt.Println("Usage: nightly-echo-pinger [-f <file>] <target1> <target2> ...")
		flag.PrintDefaults()
		os.Exit(1)
	}

	fmt.Println("📡 Initiating Echo-Location Scan...\n")

	var wg sync.WaitGroup
	results := make(chan PingResult, len(targets))

	for _, target := range targets {
		wg.Add(1)
		go pingTarget(target, &wg, results)
	}

	wg.Wait()
	close(results)

	for result := range results {
		if result.Reachable {
			fmt.Printf("[%s] Echo Received! Latency: %.2f ms\n", result.Target, float64(result.Latency)/float64(time.Millisecond))
		} else {
			fmt.Printf("[%s] Silence Detected. Target unreachable. (%v)\n", result.Target, result.Error)
		}
	}

	fmt.Println("\nScan Complete. May your signals always find their way.")
}
