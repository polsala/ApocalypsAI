package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"strconv"
	"strings"
	"testing"
	"time"
)

// Mock rationale:
// We need to mock `io.Reader` and `io.Writer` to simulate network communication
// without actually opening sockets. This makes tests deterministic and offline.
// We also mock `time.Now()` to control the server's perceived time, ensuring
// drift calculations are consistent regardless of when the test runs.

// mockReadWriter implements io.Reader, io.Writer, and io.Closer for testing.
type mockReadWriter struct {
	readBuf  *bytes.Buffer
	writeBuf *bytes.Buffer
	closed   bool
}

func newMockReadWriter(input string) *mockReadWriter {
	return &mockReadWriter{
		readBuf:  bytes.NewBufferString(input),
		writeBuf: new(bytes.Buffer),
	}
}

func (m *mockReadWriter) Read(p []byte) (n int, err error) {
	if m.closed {
		return 0, io.EOF
	}
	return m.readBuf.Read(p)
}

func (m *mockReadWriter) Write(p []byte) (n int, err error) {
	if m.closed {
		return 0, io.ErrClosedPipe
	}
	return m.writeBuf.Write(p)
}

func (m *mockReadWriter) Close() error {
	m.closed = true
	return nil
}

func TestProcessClientRequest(t *testing.T) {
	// Define a fixed server start time for deterministic tests
	serverStartTime := time.Date(2023, time.January, 1, 12, 0, 0, 0, time.UTC)

	tests := []struct {
		name             string
		clientInput      string
		simulatedLatency time.Duration
		// expectedOutputFn now takes the actual clientTime, and the two server times from the mock
		expectedOutputFn func(clientTime, serverTimeBeforeLatency, serverTimeAfterLatency time.Time, simulatedLatency time.Duration) string
		expectedError    bool
	}{
		{
			name:             "Valid client timestamp, no drift (client time matches server receive time)",
			clientInput:      fmt.Sprintf("%d\n", serverStartTime.UnixNano()), // Client time is exactly serverStartTime
			simulatedLatency: 50 * time.Millisecond,
			expectedOutputFn: func(clientTime, serverTimeBeforeLatency, serverTimeAfterLatency time.Time, simulatedLatency time.Duration) string {
				drift := clientTime.Sub(serverTimeBeforeLatency) // Should be 0
				return fmt.Sprintf("OK: Client Time: %s, Server Time (pre-latency): %s, Server Time (post-latency): %s, Clock Drift: %s, Simulated Latency: %s\n",
					clientTime.Format(time.RFC3339Nano),
					serverTimeBeforeLatency.Format(time.RFC3339Nano),
					serverTimeAfterLatency.Format(time.RFC3339Nano),
					drift,
					simulatedLatency,
				)
			},
			expectedError: false,
		},
		{
			name:             "Valid client timestamp, client clock ahead",
			clientInput:      fmt.Sprintf("%d\n", serverStartTime.Add(5*time.Second).UnixNano()),
			simulatedLatency: 100 * time.Millisecond,
			expectedOutputFn: func(clientTime, serverTimeBeforeLatency, serverTimeAfterLatency time.Time, simulatedLatency time.Duration) string {
				drift := clientTime.Sub(serverTimeBeforeLatency)
				return fmt.Sprintf("OK: Client Time: %s, Server Time (pre-latency): %s, Server Time (post-latency): %s, Clock Drift: %s, Simulated Latency: %s\n",
					clientTime.Format(time.RFC3339Nano),
					serverTimeBeforeLatency.Format(time.RFC3339Nano),
					serverTimeAfterLatency.Format(time.RFC3339Nano),
					drift,
					simulatedLatency,
				)
			},
			expectedError: false,
		},
		{
			name:             "Valid client timestamp, client clock behind",
			clientInput:      fmt.Sprintf("%d\n", serverStartTime.Add(-5*time.Second).UnixNano()),
			simulatedLatency: 200 * time.Millisecond,
			expectedOutputFn: func(clientTime, serverTimeBeforeLatency, serverTimeAfterLatency time.Time, simulatedLatency time.Duration) string {
				drift := clientTime.Sub(serverTimeBeforeLatency)
				return fmt.Sprintf("OK: Client Time: %s, Server Time (pre-latency): %s, Server Time (post-latency): %s, Clock Drift: %s, Simulated Latency: %s\n",
					clientTime.Format(time.RFC3339Nano),
					serverTimeBeforeLatency.Format(time.RFC3339Nano),
					serverTimeAfterLatency.Format(time.RFC3339Nano),
					drift,
					simulatedLatency,
				)
			},
			expectedError: false,
		},
		{
			name:             "Invalid client timestamp format",
			clientInput:      "not-a-timestamp\n",
			simulatedLatency: 0,
			expectedOutputFn: func(_, _, _, _ time.Time, _ time.Duration) string {
				return "ERROR: Invalid timestamp format. Send Unix nanoseconds."
			},
			expectedError: true,
		},
		{
			name:             "Empty client timestamp",
			clientInput:      "\n",
			simulatedLatency: 0,
			expectedOutputFn: func(_, _, _, _ time.Time, _ time.Duration) string {
				return "ERROR: Invalid timestamp format. Send Unix nanoseconds."
			},
			expectedError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockRW := newMockReadWriter(tt.clientInput)

			mockNowCallCount := 0
			mockNow := func() time.Time {
				mockNowCallCount++
				if mockNowCallCount == 1 {
					// First call to NowFunc is for serverTimeBeforeLatency
					return serverStartTime
				}
				// Second call to NowFunc is for serverTimeAfterLatency, which occurs after simulatedLatency
				return serverStartTime.Add(tt.simulatedLatency)
			}

			config := Config{
				SimulatedLatency: tt.simulatedLatency,
				NowFunc:          mockNow,
			}

			// Capture log output to ensure no unexpected errors are logged by processClientRequest
			var logBuf bytes.Buffer
			log.SetOutput(&logBuf)
			defer log.SetOutput(io.Discard) // Reset log output after test

			processClientRequest(mockRW, mockRW, config)

			output := mockRW.writeBuf.String()

			if tt.expectedError {
				if !strings.Contains(output, "ERROR:") {
					t.Errorf("Expected an error message, but got: %s", output)
				}
				// For error cases, the expectedOutputFn provides a substring to check
				if !strings.Contains(output, tt.expectedOutputFn(time.Time{}, time.Time{}, time.Time{}, 0)) {
					t.Errorf("Expected error message to contain '%s', but got '%s'", tt.expectedOutputFn(time.Time{}, time.Time{}, time.Time{}, 0), output)
				}
			} else {
				// For non-error cases, parse client time from input
				clientUnixNano, _ := strconv.ParseInt(strings.TrimSpace(tt.clientInput), 10, 64)
				clientTime := time.Unix(0, clientUnixNano)
				
				// Generate expected output using the exact times from the mock
				expectedOutput := tt.expectedOutputFn(clientTime, serverStartTime, serverStartTime.Add(tt.simulatedLatency), tt.simulatedLatency)

				if output != expectedOutput {
					t.Errorf("Expected output:\n'%s'\nGot:\n'%s'", expectedOutput, output)
				}
			}

			// Check if any unexpected errors were logged by writeResponse (e.g., if mockRW failed to write/flush)
			// For these tests, mockRW is robust, so this should ideally be empty.
			if logBuf.Len() > 0 && !tt.expectedError {
				t.Logf("Unexpected log output: %s", logBuf.String())
			}
		})
	}
}
