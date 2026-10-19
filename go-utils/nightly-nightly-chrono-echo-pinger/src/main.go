package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

const ( 
	bufferSize = 1024
)

// getMillis returns the current Unix timestamp in milliseconds.
func getMillis() int64 {
	return time.Now().UnixNano() / int64(time.Millisecond)
}

// pingSender sends periodic UDP pings with the current timestamp.
func pingSender(conn *net.UDPConn, interval time.Duration, wg *sync.WaitGroup) {
	defer wg.Done()
	log.Printf("[INFO] Starting ping sender, interval: %s", interval)
	for {
		select {
		case <-time.After(interval):
			msg := fmt.Sprintf("%d", getMillis())
			_, err := conn.Write([]byte(msg))
			if err != nil {
				log.Printf("[ERROR] Failed to send ping: %v", err)
				continue
			}
			log.Printf("[INFO] Sending temporal ping...")
		}
	}
}

// echoReceiver listens for UDP pings, calculates RTT, and sends echoes.
func echoReceiver(conn *net.UDPConn, anomalyThreshold time.Duration, wg *sync.WaitGroup) {
	defer wg.Done()
	log.Printf("[INFO] Starting echo receiver, anomaly threshold: %s", anomalyThreshold)
	buffer := make([]byte, bufferSize)

	for {
		n, remoteAddr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			log.Printf("[ERROR] Failed to read from UDP: %v", err)
			continue
		}

		if remoteAddr.String() == conn.LocalAddr().String() {
			// Ignore pings from self
			continue
		}

		receivedMillis, err := strconv.ParseInt(strings.TrimSpace(string(buffer[:n])), 10, 64)
		if err != nil {
			log.Printf("[WARN] Could not parse received message from %s: %v", remoteAddr, err)
			continue
		}

		currentMillis := getMillis()
		rtt := time.Duration(currentMillis - receivedMillis) * time.Millisecond

		if rtt > anomalyThreshold {
			log.Printf("[WARN] Chronal Anomaly Detected! Echo from %s, RTT: %s (Threshold: %s)", remoteAddr, rtt, anomalyThreshold)
		} else {
			log.Printf("[INFO] Received echo from %s, RTT: %s", remoteAddr, rtt)
		}

		// Send echo back to the sender
		echoMsg := fmt.Sprintf("%d", currentMillis)
		_, err = conn.WriteToUDP([]byte(echoMsg), remoteAddr)
		if err != nil {
			log.Printf("[ERROR] Failed to send echo to %s: %v", remoteAddr, err)
		}
	}
}

func main() {
	addressPtr := flag.String("address", "255.255.255.255:8080", "UDP broadcast/multicast address and port (e.g., 255.255.255.255:8080)")
	intervalPtr := flag.Duration("interval", 1*time.Second, "Interval to send pings (e.g., 1s, 500ms)")
	thresholdPtr := flag.Duration("threshold", 200*time.Millisecond, "RTT threshold for anomaly detection (e.g., 200ms, 1s)")
	flag.Parse()

	addr, err := net.ResolveUDPAddr("udp", *addressPtr)
	if err != nil {
		log.Fatalf("[FATAL] Failed to resolve UDP address %s: %v", *addressPtr, err)
	}

	// Listen on all available interfaces for the specified port
	listenAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf(":%d", addr.Port))
	if err != nil {
		log.Fatalf("[FATAL] Failed to resolve listen address: %v", err)
	}

	conn, err := net.ListenUDP("udp", listenAddr)
	if err != nil {
		log.Fatalf("[FATAL] Failed to listen on UDP: %v", err)
	}
	defer conn.Close()

	// If it's a broadcast address, enable broadcast option
	// Note: This might require specific OS permissions or network configuration
	// For multicast, use JoinGroup if needed, but for simple broadcast, WriteToUDP is often enough
	if addr.IP.IsBroadcast() {
		log.Printf("[INFO] Detected broadcast address. Attempting to enable broadcast.")
		// This is a best-effort attempt. Actual broadcast might depend on OS/network config.
		// Go's net package doesn't expose a direct SetBroadcast option for UDPConn.
		// For true broadcast, the underlying socket needs to be configured. 
		// For simplicity, we rely on the OS to handle broadcast if the address is 255.255.255.255.
	}

	log.Printf("[INFO] Chrono-Echo Pinger started on %s", conn.LocalAddr())

	var wg sync.WaitGroup
	wg.Add(2)

	go pingSender(conn, *intervalPtr, &wg)
	go echoReceiver(conn, *thresholdPtr, &wg)

	wg.Wait() // Keep main goroutine alive indefinitely
}
