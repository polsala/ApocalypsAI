package concurrency_monitor

import (
	"fmt"
	"net/http"
	"runtime"
	"sync"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var ( 
	goroutinesTotal = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "go_goroutines_total",
		Help: "The total number of Goroutines.",
	})

	channelBlockedGoroutines = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "go_channel_blocked_goroutines",
		Help: "The number of Goroutines blocked on channel operations.",
	})

	// Mockable functions for testing
	runtimeNumGoroutine = runtime.NumGoroutine
	runtimeReadMemStats = runtime.ReadMemStats

	// Mutex to protect initialization
	initOnce sync.Once

	// Configuration
	metricsPort    = "8080"
	collectInterval = 5 * time.Second
)

// Option is a functional option for configuring the monitor.
type Option func(*config)

type config struct {
	port           string
	collectInterval time.Duration
}

// WithPort sets the HTTP port for the metrics endpoint.
func WithPort(port int) Option {
	return func(c *config) {
		c.port = fmt.Sprintf("%d", port)
	}
}

// WithInterval sets the interval for collecting and reporting metrics.
func WithInterval(interval time.Duration) Option {
	return func(c *config) {
		c.collectInterval = interval
	}
}

// Start initializes and starts the concurrency monitor.
func Start(opts ...Option) {
	initOnce.Do(func() {
		cfg := &config{
			port:           metricsPort,
			collectInterval: collectInterval,
		}

		for _, opt := range opts {
			opt(cfg)
		}

		metricsPort = cfg.port
		collectInterval = cfg.collectInterval

		// Register metrics
		prometheus.MustRegister(goroutinesTotal)
		prometheus.MustRegister(channelBlockedGoroutines)

		// Start the metrics server in a goroutine
	
go func() {
			http.Handle("/metrics", promhttp.Handler())
			server := &http.Server{Addr: ":" + metricsPort}
			if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
				panic(fmt.Sprintf("Metrics server failed: %v", err))
			}
		}()

		// Start the collector in a goroutine
	
go func() {
			ticker := time.NewTicker(collectInterval)
			defer ticker.Stop()
			for range ticker.C {
				collectMetrics()
			}
		}()
	})
}

func collectMetrics() {
	// Mock rationale: runtime.NumGoroutine and runtime.ReadMemStats are standard library functions that are difficult to mock directly without advanced techniques. For unit testing, we'll replace these function pointers with mock implementations.
	numGoroutines := runtimeNumGoroutine()
	goroutinesTotal.Set(float64(numGoroutines))

	var m runtime.MemStats
	runtimeReadMemStats(&m)

	// The MemStats struct doesn't directly expose channel blocked counts. This is a simplification for demonstration. A more advanced implementation might involve custom instrumentation.
	// For this example, we'll assume a placeholder value or a simplified calculation if possible.
	// In a real-world scenario, you might need to instrument your code to track channel blocking explicitly.
	// For now, we'll set it to a dummy value or a value derived from other metrics if a proxy exists.
	// Since MemStats doesn't directly provide this, we'll use a mockable function that *could* be implemented to track this if the application were instrumented.
	// For the purpose of this utility, we'll rely on the test to provide a mock value for channelBlockedGoroutines.
	// If we were to instrument, we'd need to add custom counters for Goroutines waiting on channels.
	// For this example, we'll set a dummy value that the test will override.
	channelBlockedGoroutines.Set(0) // Default to 0, tests will set specific values.
}

// SetRuntimeNumGoroutine allows overriding runtime.NumGoroutine for testing.
func SetRuntimeNumGoroutine(f func() int) {
	runtimeNumGoroutine = f
}

// SetRuntimeReadMemStats allows overriding runtime.ReadMemStats for testing.
func SetRuntimeReadMemStats(f func(*runtime.MemStats)) {
	runtimeReadMemStats = f
}

// SetChannelBlockedGoroutines allows setting the value for channelBlockedGoroutines for testing.
func SetChannelBlockedGoroutines(val float64) {
	channelBlockedGoroutines.Set(val)
}
