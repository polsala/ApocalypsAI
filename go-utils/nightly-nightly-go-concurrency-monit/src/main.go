package concurrencymonitor

import (
	"net/http"
	"runtime"
	"log"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var ( 
	goroutineCount = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "go_goroutines_total",
		Help: "Number of goroutines currently running.",
	})
)

// Start initializes and starts the HTTP server for the concurrency monitor.
// It exposes goroutine metrics on the specified address.
func Start(addr string) {
	prometheus.MustRegister(goroutineCount)

	http.Handle("/metrics", promhttp.Handler())

	go func() {
		log.Printf("Concurrency monitor starting on %s\n", addr)
		if err := http.ListenAndServe(addr, nil); err != nil {
			log.Fatalf("Concurrency monitor failed to start: %v\n", err)
		}
	}()

	// Update the goroutine count periodically in a separate goroutine
	go func() {
		for {
			count := float64(runtime.NumGoroutine())
			goroutineCount.Set(count)
			time.Sleep(5 * time.Second) // Update every 5 seconds
		}
	}()
}
