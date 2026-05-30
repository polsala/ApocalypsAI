package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We use bytes.Buffer to capture logs in memory instead of writing to a file,
// ensuring tests are deterministic and don't rely on file system state.
// We use httptest.NewServer to create a local, in-memory HTTP server for testing the EchoHandler
// and for mocking the forward target, ensuring network calls are contained within the test environment.

func TestEchoLogger_Log(t *testing.T) {
	var buf bytes.Buffer
	logger := NewEchoLogger(&buf)

	testEcho := Echo{
		Timestamp:   time.Date(2023, 1, 1, 12, 0, 0, 0, time.UTC),
		RemoteAddr:  "127.0.0.1:12345",
		Method:      "GET",
		Path:        "/test",
		Headers:     map[string]string{"User-Agent": "test-client"},
		BodySnippet: "hello",
	}

	logger.Log(testEcho)

	loggedOutput := buf.String()
	if !strings.Contains(loggedOutput, `"method":"GET"`) {
		t.Errorf("Logged output missing method: %s", loggedOutput)
	}
	if !strings.Contains(loggedOutput, `"path":"/test"`) {
		t.Errorf("Logged output missing path: %s", loggedOutput)
	}
	if !strings.Contains(loggedOutput, `"body_snippet":"hello"`) {
		t.Errorf("Logged output missing body snippet: %s", loggedOutput)
	}

	// Verify it's valid JSON
	var receivedEcho Echo
	err := json.Unmarshal([]byte(loggedOutput), &receivedEcho)
	if err != nil {
		t.Fatalf("Logged output is not valid JSON: %v\n%s", err, loggedOutput)
	}
	if receivedEcho.Method != testEcho.Method {
		t.Errorf("Expected method %s, got %s", testEcho.Method, receivedEcho.Method)
	}
}

func TestEchoHandler_NoForward(t *testing.T) {
	var logBuf bytes.Buffer
	logger := NewEchoLogger(&logBuf)

	handler := EchoHandler(logger, "") // No forwarding

	req := httptest.NewRequest("POST", "/api/data", strings.NewReader("test body"))
	req.Header.Set("Content-Type", "text/plain")
	req.RemoteAddr = "192.168.1.100:54321"

	rr := httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	expectedBodyPrefix := "Temporal echo received and processed at"
	if !strings.HasPrefix(rr.Body.String(), expectedBodyPrefix) {
		t.Errorf("handler returned unexpected body: got %v want prefix %v",
			rr.Body.String(), expectedBodyPrefix)
	}

	// Give goroutine a moment to log
	time.Sleep(10 * time.Millisecond)

	loggedOutput := logBuf.String()
	if !strings.Contains(loggedOutput, `"method":"POST"`) {
		t.Errorf("Logged output missing method: %s", loggedOutput)
	}
	if !strings.Contains(loggedOutput, `"path":"/api/data"`) {
		t.Errorf("Logged output missing path: %s", loggedOutput)
	}
	if !strings.Contains(loggedOutput, `"body_snippet":"test body"`) {
		t.Errorf("Logged output missing body snippet: %s", loggedOutput)
	}
	if !strings.Contains(loggedOutput, `"remote_addr":"192.168.1.100:54321"`) {
		t.Errorf("Logged output missing remote address: %s", loggedOutput)
	}
	if !strings.Contains(loggedOutput, `"Content-Type":"text/plain"`) {
		t.Errorf("Logged output missing header: %s", loggedOutput)
	}
}

func TestEchoHandler_WithForward(t *testing.T) {
	var logBuf bytes.Buffer
	logger := NewEchoLogger(&logBuf)

	// Mock rationale: Use httptest.NewServer to create a local mock HTTP server
	// that acts as the forward target. This allows us to verify that the EchoHandler
	// correctly forwards requests without making actual external network calls.
	var forwardedRequests []httptest.Request
	var forwardMu sync.Mutex
	forwardTarget := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		forwardMu.Lock()
		defer forwardMu.Unlock()
		bodyBytes, _ := io.ReadAll(r.Body)
		r.Body = io.NopCloser(bytes.NewReader(bodyBytes)) // Restore body for inspection
		forwardedRequests = append(forwardedRequests, *r)
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "Forwarded OK")
	}))
	defer forwardTarget.Close()

	handler := EchoHandler(logger, forwardTarget.URL)

	req := httptest.NewRequest("PUT", "/items/123", strings.NewReader(`{"id":123,"name":"item"}`)))
	req.Header.Set("Authorization", "Bearer token")
	req.Header.Set("Content-Type", "application/json")
	req.RemoteAddr = "10.0.0.5:8080"

	rr := httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	// Give goroutines time to log and forward
	time.Sleep(50 * time.Millisecond) // Increased sleep for forwarding

	// Verify log
	loggedOutput := logBuf.String()
	if !strings.Contains(loggedOutput, `"method":"PUT"`) {
		t.Errorf("Logged output missing method: %s", loggedOutput)
	}
	if !strings.Contains(loggedOutput, `"path":"/items/123"`) {
		t.Errorf("Logged output missing path: %s", loggedOutput)
	}
	if !strings.Contains(loggedOutput, `"body_snippet":"{\"id\":123,\"name\":\"item\"}"`) {
		t.Errorf("Logged output missing body snippet: %s", loggedOutput)
	}
	if !strings.Contains(loggedOutput, `"Authorization":"Bearer token"`) {
		t.Errorf("Logged output missing header: %s", loggedOutput)
	}

	// Verify forwarded request
	forwardMu.Lock()
	defer forwardMu.Unlock()
	if len(forwardedRequests) != 1 {
		t.Fatalf("Expected 1 forwarded request, got %d", len(forwardedRequests))
	}
	forwardedReq := forwardedRequests[0]
	if forwardedReq.Method != "PUT" {
		t.Errorf("Forwarded request method mismatch: got %s, want PUT", forwardedReq.Method)
	}
	if forwardedReq.URL.Path != "/items/123" {
		t.Errorf("Forwarded request path mismatch: got %s, want /items/123", forwardedReq.URL.Path)
	}
	forwardedBody, _ := io.ReadAll(forwardedReq.Body)
	if string(forwardedBody) != `{"id":123,"name":"item"}` {
		t.Errorf("Forwarded request body mismatch: got %s", string(forwardedBody))
	}
	if forwardedReq.Header.Get("Authorization") != "Bearer token" {
		t.Errorf("Forwarded request header 'Authorization' mismatch: got %s", forwardedReq.Header.Get("Authorization"))
	}
}

func TestEchoHandler_BodySnippetTruncation(t *testing.T) {
	var logBuf bytes.Buffer
	logger := NewEchoLogger(&logBuf)

	handler := EchoHandler(logger, "")

	longBody := strings.Repeat("a", 250)
	req := httptest.NewRequest("POST", "/longbody", strings.NewReader(longBody))
	rr := httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	time.Sleep(10 * time.Millisecond)

	loggedOutput := logBuf.String()
	if !strings.Contains(loggedOutput, `"body_snippet":"`+strings.Repeat("a", 200)+`..."`) {
		t.Errorf("Body snippet was not truncated correctly: %s", loggedOutput)
	}
}
