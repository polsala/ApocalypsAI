package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker/internal/config"
	"github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker/internal/server"
	"github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker/internal/quantum"
)

func main() {
	// Parse command line flags
	mode := flag.String("mode", "server", "Operation mode: server|generate|verify|monitor")
	configFile := flag.String("config", "config.yaml", "Path to config file")
	port := flag.Int("port", 8080, "Server port (for server mode)")
	pairs := flag.Int("pairs", 5, "Number of pairs to generate/verify")
	fidelity := flag.Float64("fidelity", 0.95, "Quantum fidelity level")
	nodeA := flag.String("node-a", "node1", "First node for verification")
	nodeB := flag.String("node-b", "node2", "Second node for verification")
	duration := flag.Duration("duration", 30*time.Second, "Monitoring duration")
	threshold := flag.Float64("threshold", 0.8, "Coherence threshold")

	flag.Parse()

	// Load configuration
	cfg, err := config.Load(*configFile)
	if err != nil {
		log.Printf("Warning: Could not load config file: %v", err)
		log.Println("Using default configuration")
		cfg = config.Default()
	}

	// Override config with flags if provided
	if *port != 8080 {
		cfg.Server.Port = *port
	}

	switch *mode {
	case "server":
		startServer(cfg)
	case "generate":
		generatePairs(*pairs, *fidelity)
	case "verify":
		verifyEntanglement(*nodeA, *nodeB, *pairs)
	case "monitor":
		monitorCoherence(*duration, *threshold)
	default:
		fmt.Println("Unknown mode. Available modes: server, generate, verify, monitor")
		os.Exit(1)
	}
}

func startServer(cfg *config.Config) {
	srv := server.New(cfg)

	// Start server in a goroutine
	go func() {
		log.Printf("Starting quantum entanglement server on port %d...", cfg.Server.Port)
		if err := srv.Start(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server failed to start: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down server...")
	if err := srv.Shutdown(); err != nil {
		log.Printf("Server shutdown error: %v", err)
	}
	log.Println("Server exited gracefully")
}

func generatePairs(count int, fidelity float64) {
	log.Printf("Generating %d entangled pairs with fidelity %.2f...", count, fidelity)

	generator := quantum.NewPairGenerator(quantum.GeneratorConfig{
		DefaultFidelity: fidelity,
	})

	pairs, err := generator.GeneratePairs(count)
	if err != nil {
		log.Fatalf("Failed to generate pairs: %v", err)
	}

	log.Printf("Successfully generated %d entangled pairs:", len(pairs))
	for i, pair := range pairs {
		log.Printf("  Pair %d: ID=%s, Fidelity=%.3f, Created=%v",
			i+1, pair.ID, pair.Fidelity, pair.CreatedAt)
	}
}

func verifyEntanglement(nodeA, nodeB string, pairs int) {
	log.Printf("Verifying entanglement between %s and %s for %d pairs...", nodeA, nodeB, pairs)

	verifier := quantum.NewEntanglementVerifier()

	// Simulate verification for multiple pairs
	results := make([]quantum.VerificationResult, pairs)
	for i := 0; i < pairs; i++ {
		results[i] = verifier.VerifyEntanglement(nodeA, nodeB)
	}

	// Calculate statistics
	entangled := 0
	totalFidelity := 0.0
	for _, result := range results {
		if result.Entangled {
			entangled++
		}
		totalFidelity += result.MeasuredFidelity
	}

	avgFidelity := totalFidelity / float64(len(results))

	log.Printf("Verification complete:")
	log.Printf("  Entangled pairs: %d/%d (%.1f%%)", entangled, pairs, float64(entangled)/float64(pairs)*100)
	log.Printf("  Average fidelity: %.3f", avgFidelity)
}

func monitorCoherence(duration time.Duration, threshold float64) {
	log.Printf("Monitoring quantum coherence for %v with threshold %.2f...", duration, threshold)

	monitor := quantum.NewCoherenceMonitor(threshold)
	start := time.Now()

	for time.Since(start) < duration {
		status := monitor.GetStatus()
		log.Printf("  Coherence: %.3f, Stable: %v, Measurements: %d",
			status.Coherence, status.Stable, status.Measurements)

		time.Sleep(1 * time.Second)
	}

	finalStatus := monitor.GetStatus()
	log.Printf("Monitoring complete:")
	log.Printf("  Final coherence: %.3f", finalStatus.Coherence)
	log.Printf("  System remained stable: %v", finalStatus.Stable)
	log.Printf("  Total measurements: %d", finalStatus.Measurements)
}
