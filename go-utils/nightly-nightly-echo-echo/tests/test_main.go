package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestEchoHandler(t *testing.T) {
	handler := NewHandler()
	server := httptest.NewServer(handler)
	defer server.Close()

	tests := []struct {
		method string
		path   string
		body   string
		header map[string]string
	}{
		{
			method: "GET",
			path:   "/test",
			body:   "",
			header: map[string]string{
				"X-Test": "value",
			},
		},
		{
			method: "POST",
			path:   "/submit",
			body:   "hello world",
			header: map[string]string{
				"Content-Type": "text/plain",
			},
		},
	}

	for _, tc := range tests {
		req, err := http.NewRequest(tc.method, server.URL+tc.path, strings.NewReader(tc.body))
		if err != nil {
			t.Fatalf("creating request: %v", err)
		}
		for k, v := range tc.header {
			req.Header.Set(k, v)
		}
		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			t.Fatalf("request failed: %v", err)
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			t.Fatalf("expected status 200, got %d", resp.StatusCode)
		}

		var echo EchoResponse
		if err := json.NewDecoder(resp.Body).Decode(&echo); err != nil {
			t.Fatalf("decoding response: %v", err)
		}

		if echo.Method != tc.method {
			t.Errorf("method mismatch: expected %s, got %s", tc.method, echo.Method)
		}
		if echo.URL != tc.path {
			t.Errorf("url mismatch: expected %s, got %s", tc.path, echo.URL)
		}
		if echo.Body != tc.body {
			t.Errorf("body mismatch: expected %s, got %s", tc.body, echo.Body)
		}
		for k, v := range tc.header {
			if echo.Headers[k] != v {
				t.Errorf("header %s mismatch: expected %s, got %s", k, v, echo.Headers[k])
			}
		}
	}
}
