package main

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
		Name: "app_goroutines_total",
		Help: "Total number of Goroutines currently running.",
	})
	goroutinesRunning = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "app_goroutines_running",
		Help: "Number of Goroutines in the _running state.",
	})
	goroutinesSyscall = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "app_goroutines_syscall",
		Help: "Number of Goroutines in the _syscall state.",
	})
	goroutinesWaiting = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "app_goroutines_waiting",
		Help: "Number of Goroutines in the _waiting state.",
	})
	channelsCreatedTotal = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "app_channels_created_total",
		Help: "Total number of channels created.",
	})
	channelsInUseTotal = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "app_channels_in_use_total",
		Help: "Total number of channels currently in use.",
	})
)

var ( 
	once sync.Once
	stopChan chan struct{}
)

// Start begins the concurrency monitoring. It registers the metrics and starts an HTTP server.
// If config is nil, default values are used.
func Start(config *MonitorConfig) {
	once.Do(func() {
		stopChan = make(chan struct{})
		var cfg MonitorConfig
		if config == nil {
			cfg = defaultMonitorConfig
		} else {
			cfg = *config
		}

		prometheus.MustRegister(goroutinesTotal)
		prometheus.MustRegister(goroutinesRunning)
		prometheus.MustRegister(goroutinesSyscall)
		prometheus.MustRegister(goroutinesWaiting)
		prometheus.MustRegister(channelsCreatedTotal)
		prometheus.MustRegister(channelsInUseTotal)

		go startMetricsServer(cfg.Port)
		go collectMetricsPeriodically(cfg.Interval)
	})
}

// Stop signals the monitoring to shut down.
func Stop() {
	close(stopChan)
}

func startMetricsServer(port int) {
	http.Handle("/metrics", promhttp.Handler())
	addr := fmt.Sprintf(":%d", port)
	fmt.Printf("Starting metrics server on %s\n", addr)
	if err := http.ListenAndServe(addr, nil); err != nil && err != http.ErrServerClosed {
		fmt.Printf("Metrics server error: %v\n", err)
	}
}

func collectMetricsPeriodically(interval time.Duration) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			collectMetrics()
		case <-stopChan:
			return
		}
	}
}

func collectMetrics() {
	// Goroutine metrics
	stats := runtime.ReadMemStats()
	goroutinesTotal.Set(float64(runtime.NumGoroutine()))
	goroutinesRunning.Set(float64(stats.GocRunning))
	goroutinesSyscall.Set(float64(stats.GocSyscall))
	goroutinesWaiting.Set(float64(stats.GocWaiting))

	// Channel metrics (approximate, as Go's runtime doesn't directly expose channel counts easily)
	// This is a placeholder and would require more advanced instrumentation if precise counts are needed.
	// For now, we'll just track created channels and assume a rough correlation with 'in use'.
	// A more robust solution might involve wrapping channel creation/usage.

	// Placeholder for channel creation tracking. This would ideally be called when a channel is created.
	// For demonstration, we'll assume some channels are created implicitly.
	// channelsCreatedTotal.Add(1) // Example of incrementing

	// Estimating channels in use is complex without explicit instrumentation.
	// This metric is a placeholder and might not be accurate without custom channel wrappers.
	// For now, we'll set it to a dummy value or a very rough estimate if possible.
	// A real-world scenario might involve a custom channel type that tracks its own lifecycle.
	// For this example, we'll leave it as a gauge that could be manually set or updated by other parts of the app.
}

// MonitorConfig holds configuration for the monitor.
type MonitorConfig struct {
	Port     int
	Interval time.Duration
}

var defaultMonitorConfig = MonitorConfig{
	Port:     8080,
	Interval: 5 * time.Second,
}

// MockChannel is a dummy type to simulate channel creation for testing.
type MockChannel chan int

// CreateMockChannel simulates the creation of a channel and increments the counter.
func CreateMockChannel() MockChannel {
	channelsCreatedTotal.Inc()
	return make(MockChannel)
}

// GetChannelsInUse is a placeholder to demonstrate how channel usage might be reported.
// In a real application, this would be more sophisticated.
func GetChannelsInUse() float64 {
	// This is a very rough estimate. A proper implementation would track active channels.
	// For testing purposes, we can simulate a value.
	return 5.0 // Dummy value for demonstration
}

func init() {
	// This init function is just for demonstration purposes and to ensure
	// the metrics are registered when the package is imported.
	// In a real application, Start() would be called explicitly.
}
