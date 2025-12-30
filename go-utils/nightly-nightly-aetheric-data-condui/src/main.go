package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net"
	"os"
	"sync"
	"time"
)

// AethericConfig holds the configuration for network anomalies.
type AethericConfig struct {
	DelayMs        int
	LossRate       float64 // 0.0 to 1.0
	CorruptionRate float64 // 0.0 to 1.0
	BufferSize     int
	RandSource     *rand.Rand // For deterministic testing, can be injected
}

// NewAethericConfig creates a new AethericConfig with a default random source.
func NewAethericConfig(delayMs int, lossRate, corruptionRate float64, bufferSize int) AethericConfig {
	return AethericConfig{
		DelayMs:        delayMs,
		LossRate:       lossRate,
		CorruptionRate: corruptionRate,
		BufferSize:     bufferSize,
		RandSource:     rand.New(rand.NewSource(time.Now().UnixNano())), // Default to non-deterministic
	}
}

// applyAethericEffects processes a buffer, applying configured anomalies.
// It returns the modified buffer and an error if any. If loss occurs, it returns nil, nil.
func (c AethericConfig) applyAethericEffects(buf []byte) ([]byte, error) {
	// Apply delay
	if c.DelayMs > 0 {
		time.Sleep(time.Duration(c.DelayMs) * time.Millisecond)
	}

	// Apply loss
	if c.LossRate > 0 && c.RandSource.Float64() < c.LossRate {
		return nil, nil // Simulate packet loss by returning no data
	}

	// Apply corruption
	if c.CorruptionRate > 0 {
		mutatedBuf := make([]byte, len(buf))
		copy(mutatedBuf, buf)
		for i := 0; i < len(mutatedBuf); i++ {
			if c.RandSource.Float64() < c.CorruptionRate {
				mutatedBuf[i] = byte(c.RandSource.Intn(256)) // Corrupt byte
			}
		}
		return mutatedBuf, nil
	}

	return buf, nil // No effects applied or only delay
}

// proxyData copies data from src to dst, applying aetheric effects.
func proxyData(dst io.Writer, src io.Reader, config AethericConfig, wg *sync.WaitGroup) {
	defer wg.Done()
	buf := make([]byte, config.BufferSize)
	for {
		n, err := src.Read(buf)
		if n > 0 {
			processedBuf, effectErr := config.applyAethericEffects(buf[:n])
			if effectErr != nil {
				log.Printf("Error applying aetheric effects: %v", effectErr)
				break
			}
			if processedBuf == nil { // Packet loss
				// log.Println("Simulating packet loss.")
				continue
			}
			
			_, writeErr := dst.Write(processedBuf)
			if writeErr != nil {
				// log.Printf("Error writing to destination: %v", writeErr)
				break
			}
		}
		if err != nil {
			if err != io.EOF {
				// log.Printf("Error reading from source: %v", err)
			}
			break
		}
	}
}

// handleConnection sets up proxying for a single client connection.
func handleConnection(clientConn net.Conn, targetHost, targetPort string, config AethericConfig) {
	defer clientConn.Close()

	targetAddr := fmt.Sprintf("%s:%s", targetHost, targetPort)
	log.Printf("Proxying connection from %s to %s", clientConn.RemoteAddr(), targetAddr)

	targetConn, err := net.Dial("tcp", targetAddr)
	if err != nil {
		log.Printf("Failed to connect to target %s: %v", targetAddr, err)
		return
	}
	defer targetConn.Close()

	var wg sync.WaitGroup
	wg.Add(2)

	// Client to Target
	go proxyData(targetConn, clientConn, config, &wg)
	// Target to Client
	go proxyData(clientConn, targetConn, config, &wg)

	wg.Wait()
	log.Printf("Connection from %s closed.", clientConn.RemoteAddr())
}

func main() {
	listenPort := flag.Int("listen-port", 0, "The local port the conduit will listen on.")
	targetHost := flag.String("target-host", "", "The target hostname or IP address to proxy to.")
	targetPort := flag.String("target-port", "", "The target port to proxy to.")
	delayMs := flag.Int("delay-ms", 0, "Average delay to introduce for each data chunk in milliseconds.")
	lossRate := flag.Float64("loss-rate", 0.0, "Probability of dropping a data chunk (0.0 to 1.0).")
	corruptionRate := flag.Float64("corruption-rate", 0.0, "Probability of corrupting a single byte within a data chunk (0.0 to 1.0).")
	bufferSize := flag.Int("buffer-size", 4096, "Size of the buffer used for copying data.")

	flag.Parse()

	if *listenPort == 0 || *targetHost == "" || *targetPort == "" {
		fmt.Println("Error: --listen-port, --target-host, and --target-port are required.")
		flag.Usage()
		os.Exit(1)
	}

	config := NewAethericConfig(*delayMs, *lossRate, *corruptionRate, *bufferSize)

	listener, err := net.Listen("tcp", fmt.Sprintf(":%d", *listenPort))
	if err != nil {
		log.Fatalf("Failed to listen on port %d: %v", *listenPort, err)
	}
	defer listener.Close()

	log.Printf("Aetheric Data Conduit listening on :%d, proxying to %s:%s with config: Delay=%dms, Loss=%.2f, Corruption=%.2f",
		*listenPort, *targetHost, *targetPort, *delayMs, *lossRate, *corruptionRate)

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Failed to accept connection: %v", err)
			continue
		}
		go handleConnection(conn, *targetHost, *targetPort, config)
	}
}
