package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"math"
	"math/rand"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

// ChaosConfig holds configuration for chaos testing
type ChaosConfig struct {
	Target     string
	Latency    int
	PacketLoss int
	Jitter     int
	Requests   int
	Timeout    int
}

// ChaosResult holds results of a single request
type ChaosResult struct {
	RequestNum int
	Latency    time.Duration
	Success    bool
	Message    string
}

// Whimsical messages for different scenarios
var whimsicalMessages = map[string][]string{
	"success": {
		"The network gods are smiling today!",
		"Smooth sailing!",
		"Lightning fast!",
		"Like butter!",
		"No gremlins here!",
		"Perfection!",
		"You've got the touch!",
		"Slaying the latency dragon!",
	},
	"failure": {
		"The network gremlins got this one",
		"Houston, we have a problem",
		"Not today, Satan!",
		"RIP connection",
		"Lost in transmission",
		"The internet is down!",
		"Connection went on vacation",
		"This request is a ghost",
	},
}

// parseTarget parses host:port or adds default port if needed
func parseTarget(target string) (string, int, error) {
	if !strings.Contains(target, ":") {
		// Add default HTTP port
		target = target + ":80"
	}

	host, portStr, err := net.SplitHostPort(target)
	if err != nil {
		return "", 0, fmt.Errorf("invalid target format: %v", err)
	}

	port, err := strconv.Atoi(portStr)
	if err != nil {
		return "", 0, fmt.Errorf("invalid port: %v", err)
	}

	return host, port, nil
}

// shouldDropPacket determines if a packet should be dropped based on packet loss percentage
func shouldDropPacket(packetLoss int) bool {
	if packetLoss <= 0 {
		return false
	}
	return rand.Intn(100) < packetLoss
}

// getLatency calculates latency with jitter
func getLatency(baseLatency, jitter int) time.Duration {
	if baseLatency <= 0 {
		return 0
	}

	jitterAmount := 0
	if jitter > 0 {
		jitterAmount = rand.Intn(jitter*2) - jitter
	}

	latency := baseLatency + jitterAmount
	if latency < 0 {
		latency = 0
	}

	return time.Duration(latency) * time.Millisecond
}

// getWhimsicalMessage returns a random whimsical message
func getWhimsicalMessage(success bool) string {
	category := "success"
	if !success {
		category = "failure"
	}

	messages := whimsicalMessages[category]
	return messages[rand.Intn(len(messages))]
}

// makeRequest makes a single connection attempt with chaos parameters
func makeRequest(config *ChaosConfig, requestNum int) ChaosResult {
	result := ChaosResult{
		RequestNum: requestNum,
	}

	// Check if packet should be dropped
	if shouldDropPacket(config.PacketLoss) {
		result.Success = false
		result.Message = getWhimsicalMessage(false)
		return result
	}

	// Calculate latency
	latency := getLatency(config.Latency, config.Jitter)
	result.Latency = latency

	// Parse target
	host, port, err := parseTarget(config.Target)
	if err != nil {
		result.Success = false
		result.Message = fmt.Sprintf("Invalid target: %v", err)
		return result
	}

	// Create context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(config.Timeout)*time.Millisecond)
	defer cancel()

	// Simulate latency before connection
	if latency > 0 {
		time.Sleep(latency)
	}

	// Make connection
	start := time.Now()
	dialer := net.Dialer{}
	conn, err := dialer.DialContext(ctx, "tcp", fmt.Sprintf("%s:%d", host, port))
	elapsed := time.Since(start)

	if err != nil {
		result.Success = false
		result.Latency = elapsed
		result.Message = getWhimsicalMessage(false)
		return result
	}

	conn.Close()
	result.Success = true
	result.Latency = elapsed
	result.Message = getWhimsicalMessage(true)

	return result
}

// printHeader prints the chaos probe header
func printHeader(config *ChaosConfig) {
	fmt.Println("\n🧪 Initiating chaos probe...")
	fmt.Printf("🎯 Target: %s\n", config.Target)
	if config.Latency > 0 {
		if config.Jitter > 0 {
			fmt.Printf("⚡ Latency: %dms ± %dms jitter\n", config.Latency, config.Jitter)
		} else {
			fmt.Printf("⚡ Latency: %dms\n", config.Latency)
		}
	} else {
		fmt.Println("⚡ Latency: Disabled")
	}
	if config.PacketLoss > 0 {
		fmt.Printf("💔 Packet loss: %d%%\n", config.PacketLoss)
	} else {
		fmt.Println("💔 Packet loss: Disabled")
	}
	fmt.Printf("📡 Making %d requests...\n\n", config.Requests)
}

// printResult prints a single request result
func printResult(result ChaosResult) {
	status := "✅"
	if !result.Success {
		status = "❌ DROPPED"
	}
	fmt.Printf("Request %d: %s %s\n", result.RequestNum+1, formatLatency(result.Latency), status)
	if result.Message != "" {
		fmt.Printf("  📝 %s\n", result.Message)
	}
}

// formatLatency formats latency for display
func formatLatency(d time.Duration) string {
	return fmt.Sprintf("%dms", d.Milliseconds())
}

// printStatistics prints summary statistics
func printStatistics(results []ChaosResult) {
	total := len(results)
	successes := 0
	var latencies []time.Duration

	for _, result := range results {
		if result.Success {
			successes++
			latencies = append(latencies, result.Latency)
		}
	}

	successRate := float64(successes) / float64(total) * 100

	fmt.Println("\n📊 Statistics:")
	fmt.Printf("- Success rate: %.1f%%\n", successRate)

	if len(latencies) > 0 {
		avgLatency := calculateAverage(latencies)
		minLatency := calculateMin(latencies)
		maxLatency := calculateMax(latencies)

		fmt.Printf("- Average latency: %s\n", formatLatency(avgLatency))
		fmt.Printf("- Min latency: %s\n", formatLatency(minLatency))
		fmt.Printf("- Max latency: %s\n", formatLatency(maxLatency))
	} else {
		fmt.Println("- Average latency: N/A (no successful requests)")
		fmt.Println("- Min latency: N/A (no successful requests)")
		fmt.Println("- Max latency: N/A (no successful requests)")
	}

	fmt.Printf("- Total requests: %d\n", total)
	fmt.Printf("- Failed requests: %d\n", total-successes)
	fmt.Println("\n🎉 Chaos probe complete! Your service survived... mostly.")
}

// calculateAverage calculates average latency
func calculateAverage(latencies []time.Duration) time.Duration {
	var total time.Duration
	for _, l := range latencies {
		total += l
	}
	return total / time.Duration(len(latencies))
}

// calculateMin finds minimum latency
func calculateMin(latencies []time.Duration) time.Duration {
	min := latencies[0]
	for _, l := range latencies[1:] {
		if l < min {
			min = l
		}
	}
	return min
}

// calculateMax finds maximum latency
func calculateMax(latencies []time.Duration) time.Duration {
	max := latencies[0]
	for _, l := range latencies[1:] {
		if l > max {
			max = l
		}
	}
	return max
}

// validateConfig validates the chaos configuration
func validateConfig(config *ChaosConfig) error {
	if config.Target == "" {
		return fmt.Errorf("target is required")
	}

	if config.Latency < 0 {
		return fmt.Errorf("latency must be non-negative")
	}

	if config.PacketLoss < 0 || config.PacketLoss > 100 {
		return fmt.Errorf("packet loss must be between 0 and 100")
	}

	if config.Jitter < 0 {
		return fmt.Errorf("jitter must be non-negative")
	}

	if config.Requests <= 0 {
		return fmt.Errorf("requests must be positive")
	}

	if config.Timeout <= 0 {
		return fmt.Errorf("timeout must be positive")
	}

	return nil
}

// parseConfig parses command line arguments into ChaosConfig
func parseConfig() (*ChaosConfig, error) {
	var config ChaosConfig

	flag.StringVar(&config.Target, "target", "", "Target host:port or hostname to test (required)")
	flag.IntVar(&config.Latency, "latency", 0, "Fixed latency in milliseconds")
	flag.IntVar(&config.PacketLoss, "packet-loss", 0, "Packet loss percentage (0-100)")
	flag.IntVar(&config.Jitter, "jitter", 0, "Jitter in milliseconds (random variation around latency)")
	flag.IntVar(&config.Requests, "requests", 10, "Number of requests to make")
	flag.IntVar(&config.Timeout, "timeout", 5000, "Request timeout in milliseconds")

	flag.Parse()

	if config.Target == "" {
		return nil, fmt.Errorf("target is required. Use --help for usage information")
	}

	return &config, nil
}

func main() {
	// Seed random number generator
	rand.Seed(time.Now().UnixNano())

	// Parse configuration
	config, err := parseConfig()
	if err != nil {
		log.Fatalf("❌ Configuration error: %v\n", err)
	}

	// Validate configuration
	if err := validateConfig(config); err != nil {
		log.Fatalf("❌ Validation error: %v\n", err)
	}

	// Print header
	printHeader(config)

	// Run chaos probe
	var wg sync.WaitGroup
	results := make([]ChaosResult, config.Requests)
	resultChan := make(chan ChaosResult, config.Requests)\n
	// Launch goroutines for concurrent requests
	for i := 0; i < config.Requests; i++ {
		wg.Add(1)
		go func(requestNum int) {
			defer wg.Done()
			result := makeRequest(config, requestNum)
			resultChan <- result
		}(i)
	}

	// Wait for all requests to complete
	wg.Wait()
	close(resultChan)

	// Collect results
	i := 0
	for result := range resultChan {
		results[i] = result
		printResult(result)
		i++
	}

	// Print statistics
	printStatistics(results)
}
