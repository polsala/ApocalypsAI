package monitor

import (
	"fmt"
	"net/http"
	"runtime"
	"time"
)

// StartMonitor starts an HTTP server to expose goroutine metrics.
// It listens on the specified port.
func StartMonitor(port int) {
	http.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		goroutines := runtime.NumGoroutine()
		fmt.Fprintf(w, "# HELP go_goroutines_total The total number of goroutines.\n")
		fmt.Fprintf(w, "# TYPE go_goroutines_total gauge\n")
		fmt.Fprintf(w, "go_goroutines_total %d\n", goroutines)
	})

	addr := fmt.Sprintf(":%d", port)
	fmt.Printf("Metrics server listening on %s\n", addr)

	// Use a custom server to avoid blocking the main goroutine if this is embedded
	server := &http.Server{
		Addr:              addr,
		ReadTimeout:       5 * time.Second,
		WriteTimeout:      10 * time.Second,
		IdleTimeout:       120 * time.Second,
		Handler:           nil, // Use DefaultServeMux
	}

	if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		fmt.Printf("Metrics server error: %v\n", err)
	}
}
