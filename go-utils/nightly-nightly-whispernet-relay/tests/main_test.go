package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// MockRoundTripper allows us to mock HTTP responses for httpClient.Do
type MockRoundTripper struct {
	mu      sync.Mutex
	calls   map[string]int
	Handler func(*http.Request) (*http.Response, error)
}

func (m *MockRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	m.mu.Lock()
	m.calls[req.URL.String()]++
	m.mu.Unlock()
	return m.Handler(req)
}

func newMockRoundTripper(handler func(*http.Request) (*http.Response, error)) *MockRoundTripper {
	return &MockRoundTripper{
		calls:   make(map[string]int),
		Handler: handler,
	}
}

func TestLoadConfig(t *testing.T) {
	// # Mock rationale: Environment variables are external state, mocked for deterministic testing.
	os.Clearenv()
	os.Setenv("TARGET_URLS", "http://target1.com, http://target2.com")
	os.Setenv("PORT", "9000")
	os.Setenv("RETRY_ATTEMPTS", "5")
	os.Setenv("RETRY_DELAY_SECONDS", "2")

	config := loadConfig()

	if config.Port != "9000" {
		t.Errorf("Expected port 9000, got %s", config.Port)
	}
	if len(config.TargetURLs) != 2 || config.TargetURLs[0] != "http://target1.com" || config.TargetURLs[1] != "http://target2.com" {
		t.Errorf("Expected two target URLs, got %v", config.TargetURLs)
	}
	if config.RetryAttempts != 5 {
		t.Errorf("Expected retry attempts 5, got %d", config.RetryAttempts)
	}
	if config.RetryDelaySecs != 2 {
		t.Errorf("Expected retry delay 2, got %d", config.RetryDelaySecs)
	}

	// Test defaults
	os.Clearenv()
	os.Setenv("TARGET_URLS", "http://target.com")
	config = loadConfig()
	if config.Port != defaultPort {
		t.Errorf("Expected default port %s, got %s", defaultPort, config.Port)
	}
	if config.RetryAttempts != defaultRetryAttempts {
		t.Errorf("Expected default retry attempts %d, got %d", defaultRetryAttempts, config.RetryAttempts)
	}
	if config.RetryDelaySecs != defaultRetryDelaySecs {
		t.Errorf("Expected default retry delay %d, got %d", defaultRetryDelaySecs, config.RetryDelaySecs)
	}

	// Test required TARGET_URLS
	os.Clearenv()
	// Temporarily redirect log.Fatal to capture it
	oldLogFatal := log.Fatalf
	defer func() { log.Fatalf = oldLogFatal }()
	var fatalCalled bool
	log.Fatalf = func(format string, v ...interface{}) {
		fatalCalled = true
		panic("log.Fatal called") // Panic to stop execution and be caught by recover
	}

	defer func() {
		if r := recover(); r == nil {
			t.Errorf("loadConfig did not call log.Fatal when TARGET_URLS was missing")
		}
		if !fatalCalled {
			t.Errorf("log.Fatal was not called")
		}
	}()
	loadConfig() // This should trigger log.Fatal
}

func TestHandleStatus(t *testing.T) {
	req, err := http.NewRequest("GET", "/status", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(handleStatus)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	expected := "WhisperNet Relay is operational."
	if rr.Body.String() != expected {
		t.Errorf("handler returned unexpected body: got %v want %v",
			rr.Body.String(), expected)
	}
}

func TestHandleRelay_Success(t *testing.T) {
	// # Mock rationale: http.Client is an external dependency, mocked to control network behavior.
	// We replace the global httpClient with a mock for testing.
	originalHTTPClient := httpClient
	defer func() { httpClient = originalHTTPClient }() // Restore original after test

	mockTarget1Calls := 0
	mockTarget2Calls := 0

	mockRT := newMockRoundTripper(func(req *http.Request) (*http.Response, error) {
		if strings.Contains(req.URL.String(), "target1") {
			mockTarget1Calls++
		} else if strings.Contains(req.URL.String(), "target2") {
			mockTarget2Calls++
		}
		return &http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewBufferString("OK")),
			Request:    req,
		}, nil
	})
	httpClient = &http.Client{Transport: mockRT}

	// # Mock rationale: Environment variables are external state, mocked for deterministic testing.
	os.Clearenv()
	os.Setenv("TARGET_URLS", "http://mock-target1.com,http://mock-target2.com")
	config := loadConfig()

	req, err := http.NewRequest("POST", "/relay", bytes.NewBufferString("test message"))
	if err != nil {
		t.Fatal(err)
	}
	req.Header.Set("Content-Type", "text/plain")

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		handleRelay(w, r, config)
	})

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	// Give goroutines time to execute
	time.Sleep(100 * time.Millisecond)

	if mockRT.calls["http://mock-target1.com"] != 1 {
		t.Errorf("Expected target1 to be called once, got %d", mockRT.calls["http://mock-target1.com"])
	}
	if mockRT.calls["http://mock-target2.com"] != 1 {
		t.Errorf("Expected target2 to be called once, got %d", mockRT.calls["http://mock-target2.com"])
	}
}

func TestHandleRelay_RetryLogic(t *testing.T) {
	// # Mock rationale: http.Client is an external dependency, mocked to control network behavior.
	originalHTTPClient := httpClient
	defer func() { httpClient = originalHTTPClient }()

	mockTarget1Calls := 0
	mockTarget2Calls := 0

	mockRT := newMockRoundTripper(func(req *http.Request) (*http.Response, error) {
		if strings.Contains(req.URL.String(), "target1") {
			mockTarget1Calls++
			if mockTarget1Calls < 2 { // Fail first attempt, succeed second
				return &http.Response{
					StatusCode: http.StatusInternalServerError,
					Body:       io.NopCloser(bytes.NewBufferString("Error")),
					Request:    req,
				}, nil
			}
			return &http.Response{
				StatusCode: http.StatusOK,
				Body:       io.NopCloser(bytes.NewBufferString("OK")),
				Request:    req,
			}, nil
		} else if strings.Contains(req.URL.String(), "target2") {
			mockTarget2Calls++
			// Always fail for target2 to test max retries
			return &http.Response{
				StatusCode: http.StatusBadGateway,
				Body:       io.NopCloser(bytes.NewBufferString("Gateway Error")),
				Request:    req,
			}, nil
		}
		return nil, fmt.Errorf("unknown target")
	})
	httpClient = &http.Client{Transport: mockRT}

	// # Mock rationale: Environment variables are external state, mocked for deterministic testing.
	os.Clearenv()
	os.Setenv("TARGET_URLS", "http://mock-target1.com,http://mock-target2.com")
	os.Setenv("RETRY_ATTEMPTS", "3")
	os.Setenv("RETRY_DELAY_SECONDS", "1") // Short delay for faster test
	config := loadConfig()

	req, err := http.NewRequest("POST", "/relay", bytes.NewBufferString("retry test message"))
	if err != nil {
		t.Fatal(err)
	}
	req.Header.Set("Content-Type", "text/plain")

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		handleRelay(w, r, config)
	})

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	// Give goroutines enough time to execute all retries (1s + 2s for target1, 1s + 2s + 4s for target2)
	// Max delay for target2 is 1+2+4 = 7 seconds. Let's wait a bit more.
	time.Sleep(8 * time.Second)

	// Target 1 should have been called twice (1 fail, 1 success)
	if mockRT.calls["http://mock-target1.com"] != 2 {
		t.Errorf("Expected target1 to be called twice, got %d", mockRT.calls["http://mock-target1.com"])
	}
	// Target 2 should have been called 3 times (all fails, hit max retries)
	if mockRT.calls["http://mock-target2.com"] != 3 {
		t.Errorf("Expected target2 to be called 3 times, got %d", mockRT.calls["http://mock-target2.com"])
	}
}

func TestHandleRelay_InvalidMethod(t *testing.T) {
	// # Mock rationale: Environment variables are external state, mocked for deterministic testing.
	os.Clearenv()
	os.Setenv("TARGET_URLS", "http://mock-target.com")
	config := loadConfig()

	req, err := http.NewRequest("GET", "/relay", nil) // Use GET instead of POST
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		handleRelay(w, r, config)
	})

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusMethodNotAllowed)
	}
}

func TestHandleRelay_EmptyBody(t *testing.T) {
	// # Mock rationale: Environment variables are external state, mocked for deterministic testing.
	os.Clearenv()
	os.Setenv("TARGET_URLS", "http://mock-target.com")
	config := loadConfig()

	req, err := http.NewRequest("POST", "/relay", bytes.NewBufferString("")) // Empty body
	if err != nil {
		t.Fatal(err)
	}
	req.Header.Set("Content-Type", "text/plain")

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		handleRelay(w, r, config)
	})

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusBadRequest)
	}
}
