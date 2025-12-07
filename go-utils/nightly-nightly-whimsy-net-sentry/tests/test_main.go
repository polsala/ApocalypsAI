package main

import (
	"bytes"
	"fmt"
	"net/http"
	"os"
	"testing"
)

func TestUpEndpoint(t *testing.T) {
	// Mock HTTP Head response
	http.DefaultTransport = &http.Transport{} // Reset transport
	mockServer := &http.Server{Addr: ":8080"}
	go func() {
		http.ListenAndServe(":8080", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.WriteHeader(200)
		}))
	}()
	time.Sleep(100 * time.Millisecond)

	oldArgs := os.Args
	os.Args = []string{"whimsy-net-sentry", "http://localhost:8080/"}
	defer func() { os.Args = oldArgs }()

	buf := &bytes.Buffer{}
	origOut := os.Stdout
	os.Stdout = buf
	defer func() { os.Stdout = origOut }()

	main()

	got := buf.String()
	if !bytes.Contains(got, []byte("✅ 200")) {
		t.Errorf("Expected success status, got %q", got)
	}
}

func TestDownEndpoint(t *testing.T) {
	oldArgs := os.Args
	os.Args = []string{"whimsy-net-sentry", "http://localhost:1234/"}
	defer func() { os.Args = oldArgs }()

	buf := &bytes.Buffer{}
	origOut := os.Stdout
	os.Stdout = buf
	defer func() { os.Stdout = origOut }()

	main()

	got := buf.String()
	if !bytes.Contains(got, []byte("❌ DOWN")) {
		t.Errorf("Expected failure status, got %q", got)
	}
}
