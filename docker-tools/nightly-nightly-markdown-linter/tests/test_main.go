package main

import (
    "io"
    "net/http"
    "strings"
    "testing"
)

// mockTransport is an http.RoundTripper that returns predefined status codes.
// # Mock rationale: ensures link checks are deterministic and offline.
type mockTransport struct {
    responses map[string]int
}

func (m *mockTransport) RoundTrip(req *http.Request) (*http.Response, error) {
    status, ok := m.responses[req.URL.String()]
    if !ok {
        status = 404
    }
    return &http.Response{
        StatusCode: status,
        Body:       io.NopCloser(strings.NewReader("")),
        Header:     make(http.Header),
    }, nil
}

func TestHeadingHierarchy(t *testing.T) {
    md := "# Title\n## Sub\n### Subsub\n## Another\n#### Too deep"
    result := lintMarkdown(md)
    if len(result.Errors) != 1 {
        t.Fatalf("expected 1 error, got %d", len(result.Errors))
    }
    if !strings.Contains(result.Errors[0].Message, "Heading level jumps") {
        t.Errorf("unexpected error message: %s", result.Errors[0].Message)
    }
}

func TestImageAlt(t *testing.T) {
    md := "![\n](image.png)"
    result := lintMarkdown(md)
    if len(result.Errors) != 1 {
        t.Fatalf("expected 1 error, got %d", len(result.Errors))
    }
    if result.Errors[0].Message != "Image missing alt text" {
        t.Errorf("unexpected error message: %s", result.Errors[0].Message)
    }
}

func TestLinkLint(t *testing.T) {
    // Replace the global checkLink function with a mock that uses mockTransport.
    originalCheckLink := checkLink
    defer func() { checkLink = originalCheckLink }()
    checkLink = func(url string) error {
        client := &http.Client{Transport: &mockTransport{responses: map[string]int{"http://good.com": 200, "http://bad.com": 404}}}
        req, _ := http.NewRequest("HEAD", url, nil)
        resp, err := client.Do(req)
        if err != nil {
            return err
        }
        defer resp.Body.Close()
        if resp.StatusCode < 200 || resp.StatusCode >= 400 {
            return errors.New("status " + resp.Status)
        }
        return nil
    }

    md := "[good](http://good.com)\n[bad](http://bad.com)"
    result := lintMarkdown(md)
    if len(result.Errors) != 1 {
        t.Fatalf("expected 1 error, got %d", len(result.Errors))
    }
    if !strings.Contains(result.Errors[0].Message, "Broken link") {
        t.Errorf("unexpected error message: %s", result.Errors[0].Message)
    }
}
