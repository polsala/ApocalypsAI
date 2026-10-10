package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"golang.org/x/net/websocket"
)

const (
	defaultPort       = "8080"
	pulseInterval     = 1 * time.Second // Interval for WebSocket broadcasts
	shutdownTimeout   = 5 * time.Second
)

// pulseHandler serves the current UTC timestamp via HTTP.
func pulseHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	fmt.Fprintf(w, "Temporal Pulse: %s\n", time.Now().UTC().Format(time.RFC3339Nano))
}

// streamHandler upgrades the connection to a WebSocket and continuously broadcasts timestamps.
func streamHandler(ws *websocket.Conn) {
	defer ws.Close()
	log.Printf("New Chronosync Beacon stream connection from %s", ws.RemoteAddr())

	ticker := time.NewTicker(pulseInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			timestamp := time.Now().UTC().Format(time.RFC3339Nano)
			if err := websocket.Message.Send(ws, timestamp); err != nil {
				log.Printf("Failed to send pulse to %s: %v", ws.RemoteAddr(), err)
				return // Client disconnected or error
			}
		case <-ws.Request().Context().Done(): // Check if client disconnected
			log.Printf("Client %s disconnected from stream.", ws.RemoteAddr())
			return
		}
	}
}

// startServer initializes and starts the HTTP server.
func startServer(port string) *http.Server {
	mux := http.NewServeMux()
	mux.HandleFunc("/pulse", pulseHandler)
	mux.Handle("/stream", websocket.Handler(streamHandler))

	server := &http.Server{
		Addr:    ":" + port,
		Handler: mux,
		// Add timeouts for production robustness
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  120 * time.Second,
	}

	go func() {
		log.Printf("Chronosync Beacon online at http://localhost%s", server.Addr)
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Chronosync Beacon failed to start: %v", err)
		}
	}()
	return server
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	server := startServer(port)

	// Set up graceful shutdown
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)

	<-stop // Wait for interrupt signal

	log.Println("Shutting down Chronosync Beacon...")
	ctx, cancel := context.WithTimeout(context.Background(), shutdownTimeout)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Fatalf("Chronosync Beacon shutdown failed: %v", err)
	}
	log.Println("Chronosync Beacon gracefully stopped.")
}
