package main

import (
	"fmt"
	"net/http"
	"runtime"
	"time"

	"github.com/gorilla/mux"
)

// GoroutineCountHandler returns the current number of goroutines.
func GoroutineCountHandler(w http.ResponseWriter, r *http.Request) {
	count := runtime.NumGoroutine()
	w.Header().Set("Content-Type", "application/json")
	jsonResponse := fmt.Sprintf(`{\"goroutines\": %d}`, count)
	w.Write([]byte(jsonResponse))
}

func main() {
	r := mux.NewRouter()

	// Expose metrics endpoint
	r.HandleFunc("/metrics", GoroutineCountHandler).Methods("GET")

	// Start a dummy goroutine to ensure the server itself has at least one goroutine
	go func() {
		select {}
	}()

	port := "8080"
	fmt.Printf("Starting ApocalypsAI Nightly Go Concurrency Monitor on :%s\n", port)

	// Start the HTTP server
	srv := &http.Server{
		Addr:         ":" + port,
		WriteTimeout: time.Second * 15,
		ReadTimeout:  time.Second * 15,
		IdleTimeout:  time.Second * 60,
		Handler:      r,
	}

	// Run the server and log any errors
	err := srv.ListenAndServe()
	if err != nil {
		fmt.Printf("Error starting server: %v\n", err)
	}
}
