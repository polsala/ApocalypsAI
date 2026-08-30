package concurrencymonitor

import (
	"fmt"
	"net/http"
	"runtime"
	"sync"
	"time"
)

var ( 
	monitorPort string
	mu sync.Mutex
)

// StartMonitor starts the HTTP server for the concurrency monitor.
// It listens on the specified port (e.g., ":8080").
func StartMonitor(port string) {
	mu.Lock()
	monitorPort = port
	mu.Unlock()

	http.HandleFunc("/monitor", handleMonitorRequest)
	fmt.Printf("Concurrency monitor started on port %s\n", port)

	// Use a goroutine to start the server so it doesn't block the main application.
	go func() {
		if err := http.ListenAndServe(port, nil); err != nil {
			fmt.Printf("Error starting concurrency monitor: %v\n", err)
		}
	}()
}

func handleMonitorRequest(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	port := monitorPort
	mu.Unlock()

	goroutineCount := runtime.NumGoroutine()

	// For a more detailed breakdown, we'd typically need to inspect stack traces,
	// which is more complex. For this utility, we'll focus on the total count
	// and a simple 'running' vs 'other' approximation based on common states.
	// A more robust solution might involve custom metrics or profiling.

	// This is a simplified approximation. A true breakdown requires deeper introspection.
	// For now, we'll just show the total count.

	fmt.Fprintf(w, "<html><head><title>Goroutine Monitor</title></head><body>")
	fmt.Fprintf(w, "<h1>Goroutine Monitor</h1>")
	fmt.Fprintf(w, "<p>Timestamp: %s</p>", time.Now().Format(time.RFC3339))
	fmt.Fprintf(w, "<p>Total Goroutines: <strong>%d</strong></p>", goroutineCount)
	fmt.Fprintf(w, "<p>Monitor accessible at: <a href=\"http://localhost%s/monitor\">http://localhost%s/monitor</a></p>", port, port)
	fmt.Fprintf(w, "</body></html>")
}
