package main

import (
	"fmt"
	"net/http"
	"runtime"
	"time"

	"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/internal/monitor"
)

func main() {
	port := "8080"
	fmt.Printf("Starting Go Concurrency Monitor on port %s\n", port)

	// Start the monitor in a separate goroutine
	go monitor.StartMonitor(8080)

	// Keep the main goroutine alive to allow the monitor to run
	select {}
}
