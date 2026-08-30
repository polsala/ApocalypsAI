package monitor

import (
	"encoding/json"
	"fmt"
	"net/http"
	"runtime"
	"sync"
)

var ( 
	serverMux *http.ServeMux
	once sync.Once
)

// Start initializes and starts the HTTP server for monitoring goroutines.
// It listens on the specified address (e.g., ":8080").
func Start(addr string) {
	once.Do(func() {
		serverMux = http.NewServeMux()
		serverMux.HandleFunc("/goroutines", handleGoroutines)
	
		fmt.Printf("Concurrency monitor started on %s\n", addr)
		if err := http.ListenAndServe(addr, serverMux);
		   err != nil {
			fmt.Printf("Error starting concurrency monitor: %v\n", err)
		}
	})
}

// handleGoroutines is an HTTP handler that returns the current goroutine count.
func handleGoroutines(w http.ResponseWriter, r *http.Request) {
	goroutineCount := runtime.NumGoroutine()

	response := map[string]int{
		"goroutine_count": goroutineCount,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}
