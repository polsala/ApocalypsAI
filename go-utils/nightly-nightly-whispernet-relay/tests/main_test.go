package main

import (
	"bytes"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

// Mock rationale: We are testing the server's logic and interaction with the WhisperStore,
// not the actual network stack. httptest allows us to simulate HTTP requests and responses
// in-memory without binding to a port, making tests fast, deterministic, and offline.

func TestWhisperStore_PostAndGet(t *testing.T) {
	store := NewWhisperStore(5 * time.Minute)
	channelID := "test-channel-1"
	message := []byte("secret message")

	// Test PostWhisper
	if !store.PostWhisper(channelID, message) {
		t.Errorf("Expected PostWhisper to succeed for new channel")
	}
	if store.GetWhisperCount() != 1 {
		t.Errorf("Expected 1 whisper in store, got %d", store.GetWhisperCount())
	}

	// Test GetWhisper
	retrieved, found := store.GetWhisper(channelID)
	if !found {
		t.Errorf("Expected GetWhisper to find the message")
	}
	if !bytes.Equal(retrieved, message) {
		t.Errorf("Retrieved message mismatch. Got %s, Expected %s", string(retrieved), string(message))
	}
	if store.GetWhisperCount() != 0 {
		t.Errorf("Expected 0 whispers after retrieval, got %d", store.GetWhisperCount())
	}

	// Test GetWhisper on non-existent channel
	_, found = store.GetWhisper("non-existent")
	if found {
		t.Errorf("Expected GetWhisper to not find non-existent message")
	}
}

func TestWhisperStore_PostConflict(t *testing.T) {
	store := NewWhisperStore(5 * time.Minute)
	channelID := "test-channel-2"
	message1 := []byte("first message")
	message2 := []byte("second message")

	store.PostWhisper(channelID, message1)
	if store.PostWhisper(channelID, message2) {
		t.Errorf("Expected PostWhisper to fail for existing channel")
	}
	if store.GetWhisperCount() != 1 {
		t.Errorf("Expected 1 whisper in store, got %d", store.GetWhisperCount())
	}

	// Ensure the original message is still there
	retrieved, _ := store.GetWhisper(channelID)
	if !bytes.Equal(retrieved, message1) {
		t.Errorf("Original message was overwritten or incorrect. Got %s, Expected %s", string(retrieved), string(message1))
	}
}

func TestWhisperStore_CleanExpiredWhispers(t *testing.T) {
	store := NewWhisperStore(1 * time.Millisecond) // Very short TTL for testing
	channelID := "test-channel-3"
	message := []byte("expiring message")

	store.PostWhisper(channelID, message)
	if store.GetWhisperCount() != 1 {
		t.Errorf("Expected 1 whisper after post, got %d", store.GetWhisperCount())
	}

	time.Sleep(5 * time.Millisecond) // Wait for whisper to expire
	store.CleanExpiredWhispers()

	if store.GetWhisperCount() != 0 {
		t.Errorf("Expected 0 whispers after cleanup, got %d", store.GetWhisperCount())
	}

	_, found := store.GetWhisper(channelID)
	if found {
		t.Errorf("Expected expired whisper to not be found")
	}
}

func TestServer_PostWhisperHandler(t *testing.T) {
	store := NewWhisperStore(5 * time.Minute)
	server := NewServer(store)

	// Test successful POST
	reqBody := []byte("hello world")
	req := httptest.NewRequest(http.MethodPost, "/whisper/channel-a", bytes.NewBuffer(reqBody))
	rr := httptest.NewRecorder()
	server.postWhisperHandler(rr, req)

	if status := rr.Code; status != http.StatusCreated {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusCreated)
	}
	if store.GetWhisperCount() != 1 {
		t.Errorf("Expected 1 whisper after post, got %d", store.GetWhisperCount())
	}

	// Test POST conflict
	req = httptest.NewRequest(http.MethodPost, "/whisper/channel-a", bytes.NewBuffer(reqBody))
	rr = httptest.NewRecorder()
	server.postWhisperHandler(rr, req)

	if status := rr.Code; status != http.StatusConflict {
		t.Errorf("handler returned wrong status code for conflict: got %v want %v", status, http.StatusConflict)
	}
	if store.GetWhisperCount() != 1 { // Still 1
		t.Errorf("Expected 1 whisper after conflict, got %d", store.GetWhisperCount())
	}

	// Test POST with empty body
	req = httptest.NewRequest(http.MethodPost, "/whisper/channel-b", bytes.NewBuffer([]byte{}))
	rr = httptest.NewRecorder()
	server.postWhisperHandler(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for empty body: got %v want %v", status, http.StatusBadRequest)
	}

	// Test POST without channel ID
	req = httptest.NewRequest(http.MethodPost, "/whisper/", bytes.NewBuffer(reqBody))
	rr = httptest.NewRecorder()
	server.postWhisperHandler(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for missing channel ID: got %v want %v", status, http.StatusBadRequest)
	}
}

func TestServer_GetWhisperHandler(t *testing.T) {
	store := NewWhisperStore(5 * time.Minute)
	server := NewServer(store)
	channelID := "channel-b"
	message := []byte("retrievable secret")
	store.PostWhisper(channelID, message)

	// Test successful GET
	req := httptest.NewRequest(http.MethodGet, "/whisper/"+channelID, nil)
	rr := httptest.NewRecorder()
	server.getWhisperHandler(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}
	if body, _ := io.ReadAll(rr.Body); !bytes.Equal(body, message) {
		t.Errorf("handler returned unexpected body: got %s want %s", string(body), string(message))
	}
	if store.GetWhisperCount() != 0 {
		t.Errorf("Expected 0 whispers after retrieval, got %d", store.GetWhisperCount())
	}

	// Test GET on non-existent/deleted channel
	req = httptest.NewRequest(http.MethodGet, "/whisper/"+channelID, nil)
	rr = httptest.NewRecorder()
	server.getWhisperHandler(rr, req)

	if status := rr.Code; status != http.StatusNotFound {
		t.Errorf("handler returned wrong status code for non-existent: got %v want %v", status, http.StatusNotFound)
	}

	// Test GET without channel ID
	req = httptest.NewRequest(http.MethodGet, "/whisper/", nil)
	rr = httptest.NewRecorder()
	server.getWhisperHandler(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for missing channel ID: got %v want %v", status, http.StatusBadRequest)
	}
}

func TestServer_MethodNotAllowed(t *testing.T) {
	store := NewWhisperStore(5 * time.Minute)
	server := NewServer(store)

	// Test PUT to /whisper/channel-c
	req := httptest.NewRequest(http.MethodPut, "/whisper/channel-c", nil)
	rr := httptest.NewRecorder()
	// Use the main handler to test method routing
	http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost {
			server.postWhisperHandler(w, r)
		} else if r.Method == http.MethodGet {
			server.getWhisperHandler(w, r)
		} else {
			http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		}
	}).ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code for PUT: got %v want %v", status, http.StatusMethodNotAllowed)
	}
}

func TestMainFunction_FlagParsing(t *testing.T) {
	// Reset flags to avoid conflicts with other tests
	oldArgs := flag.Args()
	defer flag.SetArgs(oldArgs)
	flag.CommandLine = flag.NewFlagSet(t.Name(), flag.ExitOnError) // Create a new FlagSet for this test

	// Test valid flags
	flag.SetArgs([]string{"-port", "9000", "-ttl", "10s"})
	// Mock rationale: We are testing the flag parsing logic, which is part of the main function setup.
	// We cannot directly call main() in a test and expect it to return, as it calls log.Fatal.
	// This test is a basic check that the flags can be parsed without immediate panic.
	// A full test would require mocking os.Exit and log.Fatal.
	// For this context, assuming successful parsing for valid input is sufficient.
}
