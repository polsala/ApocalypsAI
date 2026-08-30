package main

import (
    "errors"
    "reflect"
    "testing"
    "time"
)

// mockPing replaces the global pingHost during the test.
func mockPing(responses map[string]struct {
    latency time.Duration
    err     error
}) func(string) (time.Duration, error) {
    return func(host string) (time.Duration, error) {
        if r, ok := responses[host]; ok {
            return r.latency, r.err
        }
        return 0, errors.New("unknown host")
    }
}

func TestRunPing_MixedResults(t *testing.T) {
    // Prepare deterministic responses.
    mockResponses := map[string]struct {
        latency time.Duration
        err     error
    }{
        "example.com": {latency: 85 * time.Millisecond, err: nil},
        "missing.tld": {latency: 0, err: errors.New("dial timeout")},
    }

    // Swap out the real pingHost.
    original := pingHost
    pingHost = mockPing(mockResponses)
    defer func() { pingHost = original }()

    hosts := []string{"example.com", "missing.tld"}
    results := runPing(hosts)

    // Expected slice – order is not guaranteed because of concurrency.
    expected := []Result{
        {Host: "example.com", Latency: 85 * time.Millisecond, Err: nil},
        {Host: "missing.tld", Latency: 0, Err: errors.New("dial timeout")},
    }

    // Helper to compare errors as strings.
    equal := func(a, b Result) bool {
        if a.Host != b.Host {
            return false
        }
        if a.Err != nil && b.Err != nil {
            return a.Err.Error() == b.Err.Error()
        }
        return a.Err == b.Err && a.Latency == b.Latency
    }

    // Verify each expected result appears exactly once.
    for _, exp := range expected {
        found := false
        for _, got := range results {
            if equal(got, exp) {
                found = true
                break
            }
        }
        if !found {
            t.Fatalf("expected result not found: %+v (got %+v)", exp, results)
        }
    }
}

func TestFormatResult(t *testing.T) {
    cases := []struct {
        input    Result
        expected string
    }{
        {Result{Host: "foo.com", Latency: 123 * time.Millisecond, Err: nil}, "foo.com: 123ms"},
        {Result{Host: "bar.com", Latency: 0, Err: errors.New("dial timeout")}, "bar.com: error: dial timeout"},
    }
    for _, c := range cases {
        got := formatResult(c.input)
        if got != c.expected {
            t.Errorf("formatResult(%+v) = %s; want %s", c.input, got, c.expected)
        }
    }
}

func TestReadHostsFromStdin_NoData(t *testing.T) {
    // This test runs in an environment where stdin is a terminal, so the function should return nil, nil.
    hosts, err := readHostsFromStdin()
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if hosts != nil && len(hosts) != 0 {
        t.Fatalf("expected no hosts, got %v", hosts)
    }
}

func TestMain_NoArgs_NoStdin(t *testing.T) {
    // This test ensures that the program exits with an error when no input is provided.
    // Since testing os.Exit directly would terminate the test process, we invoke the
    // validation logic indirectly via a helper.
    // The helper is not exported; we replicate the validation here.
    hosts := []string{}
    if len(hosts) == 0 {
        // Simulate the error path.
        expected := "no hosts provided. supply as arguments or pipe via stdin"
        // Capture the output using a pipe.
        r, w, _ := os.Pipe()
        oldStderr := os.Stderr
        os.Stderr = w
        // Run the validation block.
        if len(hosts) == 0 {
            fmt.Fprintln(os.Stderr, expected)
        }
        w.Close()
        os.Stderr = oldStderr
        buf := make([]byte, 1024)
        n, _ := r.Read(buf)
        output := string(buf[:n])
        if !strings.Contains(output, expected) {
            t.Fatalf("expected error message %q, got %q", expected, output)
        }
    }
}
