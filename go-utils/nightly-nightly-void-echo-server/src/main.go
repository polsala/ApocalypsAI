package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
)

type Stats struct {
	activeConnections int
	totalMessages     int
	mutex             sync.Mutex
}

var stats Stats

func reverse(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}

func handleConnection(conn net.Conn, wg *sync.WaitGroup) {
	defer conn.Close()
	defer wg.Done()

	stats.mutex.Lock()
	stats.activeConnections++
	stats.mutex.Unlock()

	defer func() {
		stats.mutex.Lock()
		stats.activeConnections--
		stats.mutex.Unlock()
	}()

	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		msg := strings.TrimSpace(scanner.Text())
		if msg == "" {
			continue
		}

		stats.mutex.Lock()
		stats.totalMessages++
		stats.mutex.Unlock()

		reversed := reverse(msg)
		response := fmt.Sprintf("%s\n", reversed)
		conn.Write([]byte(response))
	}
}

func main() {
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
	defer listener.Close()

	log.Println("_void-echo-server started on :8080_")

	var wg sync.WaitGroup

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		log.Println("Shutting down server...")
		listener.Close()
		wg.Wait()
		log.Printf("Stats - Active Connections: %d, Total Messages: %d\n", stats.activeConnections, stats.totalMessages)
		os.Exit(0)
	}()

	for {
		conn, err := listener.Accept()
		if err != nil {
			select {
			case <-c:
				// Server is shutting down
				return
			default:
				log.Printf("Failed to accept connection: %v", err)
			}
			continue
		}
		wg.Add(1)
		go handleConnection(conn, &wg)
	}
}
