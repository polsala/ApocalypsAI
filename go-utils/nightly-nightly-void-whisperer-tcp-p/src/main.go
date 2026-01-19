package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

var (
	listenAddr = flag.String("listen", ":8080", "Address to listen on")
	targetAddr = flag.String("target", "localhost:9000", "Target address to forward to")
	verbose    = flag.Bool("verbose", false, "Enable verbose logging")
)

func main() {
	flag.Parse()

	listener, err := net.Listen("tcp", *listenAddr)
	if err != nil {
		log.Fatalf("Failed to listen on %s: %v", *listenAddr, err)
	}
	defer listener.Close()

	log.Printf("_void_whisperer_ proxy listening on %s -> forwarding to %s", *listenAddr, *targetAddr)

	var wg sync.WaitGroup

	// Handle graceful shutdown
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		log.Println("Shutting down _void_whisperer_ proxy...")
		listener.Close()
		wg.Wait()
		os.Exit(0)
	}()

	for {
		conn, err := listener.Accept()
		if err != nil {
			select {
			case <-c:
				return
			default:
				log.Printf("Failed to accept connection: %v", err)
			}
			continue
		}

		wg.Add(1)
		go func(c net.Conn) {
			defer wg.Done()
			handleConnection(c)
		}(conn)
	}
}

func handleConnection(clientConn net.Conn) {
	if *verbose {
		log.Printf("[WHISPER] New connection from %s", clientConn.RemoteAddr())
	}

	serverConn, err := net.Dial("tcp", *targetAddr)
	if err != nil {
		log.Printf("Failed to connect to target %s: %v", *targetAddr, err)
		clientConn.Close()
		return
	}

	if *verbose {
		log.Printf("[WHISPER] Forwarding %s -> %s", clientConn.RemoteAddr(), serverConn.RemoteAddr())
	}

	var wg sync.WaitGroup
	wg.Add(2)

	copyConn := func(dst, src net.Conn) {
		defer wg.Done()
		io.Copy(dst, src)
		dst.Close()
		src.Close()
	}

	go copyConn(serverConn, clientConn)
	go copyConn(clientConn, serverConn)

	wg.Wait()

	if *verbose {
		log.Printf("[WHISPER] Connection %s closed", clientConn.RemoteAddr())
	}
}
