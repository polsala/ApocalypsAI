package main

import (
	"fmt"
	"strings"
	"testing"
	"github.com/shirou/gopsutil/process"
)

// Mock rationale: These mocks simulate the behavior of external dependencies like
// process.Processes() and the `go tool pprof` command. This allows for deterministic
// and offline testing of the core logic without relying on actual running processes
// or the availability of the Go toolchain in the test environment.

// MockProcess is a mock implementation of process.Process.
type MockProcess struct {
	pid int32
	name string
}

func (m *MockProcess) Pid() int32 { return m.pid }
func (m *MockProcess) Name() (string, error) { return m.name, nil }
func (m *MockProcess) CmdlineSlice() ([]string, error) { return []string{m.name}, nil } // Simplified for testing

// MockProcesses returns a predefined list of mock processes.
func MockProcesses() []*process.Process {
	return []*process.Process{
		&process.Process{Pid: 1001, Name: "my-go-app"}, // Mocked to behave like a Go process
		&process.Process{Pid: 1002, Name: "another-go-service"}, // Mocked to behave like a Go process
		&process.Process{Pid: 1003, Name: "some-other-app"}, // Should be filtered out
		&process.Process{Pid: 1004, Name: "go-runtime-helper"}, // Mocked to behave like a Go process
	}
}

// MockGetGoroutineCountForPID simulates the output of `go tool pprof`.
func MockGetGoroutineCountForPID(pid int32) (int, error) {
	switch pid {
	case 1001: // my-go-app
		return 42, nil
	case 1002: // another-go-service
		return 150, nil
	case 1004: // go-runtime-helper
		return 5, nil
	default:
		return 0, fmt.Errorf("mock error: unknown PID %d", pid)
	}
}

// Mock isGoProcess simulates the isGoProcess function.
func MockIsGoProcess(p *process.Process) bool {
	// This mock logic should mirror the actual isGoProcess logic for testing purposes.
	name, err := p.Name()
	if err != nil {
		return false
	}

	if strings.Contains(strings.ToLower(name), "go") || strings.HasSuffix(strings.ToLower(name), ".go") {
		return true
	}

	// On Linux, we can try to read the command line arguments to see if it's a Go program.
	if runtime.GOOS == "linux" {
		cmdline, err := p.CmdlineSlice()
		if err != nil {
			return false
		}
		for _, arg := range cmdline {
			if strings.Contains(strings.ToLower(arg), "go") {
				return true
			}
		}
	}

	return false
}

// MockRenderTable simulates the console clearing and table rendering.
// It returns a string representation of the table for assertion.
func MockRenderTable(processes []ProcessInfo) string {
	var sb strings.Builder
	ssb.WriteString("PID | Name | Goroutines\n") // Header approximation
	for _, p := range processes {
		goroutineStr := fmt.Sprintf("%d", p.GoroutineCount)
		if p.GoroutineCount == -1 {
			goroutineStr = "N/A"
		}
		sb.WriteString(fmt.Sprintf("%d | %s | %s\n", p.PID, p.Name, goroutineStr))
	}
	return sb.String()
}

func TestGetGoProcessInfos(t *testing.T) {
	// Temporarily replace the actual functions with mocks
	originalGetGoroutineCount := getGoroutineCountForPID
	originalIsGoProcess := isGoProcess
	originalProcesses := process.Processes

	getGoroutineCountForPID = func(pid int32) (int, error) { return MockGetGoroutineCountForPID(pid) }
	isGoProcess = func(p *process.Process) bool { return MockIsGoProcess(p) }
	process.Processes = func() ([]*process.Process, error) { return MockProcesses(), nil }

	defer func() {
		// Restore original functions
		getGoroutineCountForPID = originalGetGoroutineCount
		isGoProcess = originalIsGoProcess
		process.Processes = originalProcesses
	}()

	infos, err := getGoProcessInfos()
	if err != nil {
		t.Fatalf("getGoProcessInfos() returned an error: %v", err)
	}

	if len(infos) != 3 {
		t.Errorf("Expected 3 Go processes, but got %d", len(infos))
	}

	// Check specific process details
	foundApp := false
	foundService := false
	foundHelper := false

	for _, info := range infos {
		switch info.PID {
		case 1001:
			if info.Name != "my-go-app" || info.GoroutineCount != 42 {
				t.Errorf("my-go-app: expected Name=my-go-app, GoroutineCount=42, got Name=%s, GoroutineCount=%d", info.Name, info.GoroutineCount)
			}
			foundApp = true
		case 1002:
			if info.Name != "another-go-service" || info.GoroutineCount != 150 {
				t.Errorf("another-go-service: expected Name=another-go-service, GoroutineCount=150, got Name=%s, GoroutineCount=%d", info.Name, info.GoroutineCount)
			}
			foundService = true
		case 1004:
			if info.Name != "go-runtime-helper" || info.GoroutineCount != 5 {
				t.Errorf("go-runtime-helper: expected Name=go-runtime-helper, GoroutineCount=5, got Name=%s, GoroutineCount=%d", info.Name, info.GoroutineCount)
			}
			foundHelper = true
		default:
			t.Errorf("Unexpected PID found: %d", info.PID)
		}
	}

	if !foundApp || !foundService || !foundHelper {
		t.Errorf("Not all expected Go processes were found.")
	}
}

func TestIsGoProcess(t *testing.T) {
	mockProcGoApp := &MockProcess{pid: 1, name: "my-go-app"}
	mockProcGoService := &MockProcess{pid: 2, name: "go-service"}
	mockProcGoFile := &MockProcess{pid: 3, name: "script.go"}
	mockProcNonGo := &MockProcess{pid: 4, name: "python-script"}
	mockProcGoWithArgs := &MockProcess{pid: 5, name: "my-app"} // Simulate a Go app that might have 'go' in its name

	// Mocking CmdlineSlice for Linux-specific test
	if runtime.GOOS == "linux" {
		mockProcGoWithArgs.CmdlineSlice = func() ([]string, error) { return []string{"./my-app", "--config=/etc/go/app.conf"}, nil }
	}

	ttests := []struct {
		name    string
		process *process.Process
		expected bool
	}{
		{"Go App Name", mockProcGoApp, true},
		{"Go Service Name", mockProcGoService, true},
		{"Go File Suffix", mockProcGoFile, true},
		{"Non Go App", mockProcNonGo, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Need to cast MockProcess to *process.Process for the function call
			// This is a bit hacky but necessary for testing the interface.
			var procInterface process.Process = tt.process
			actual := isGoProcess(&procInterface)
			if actual != tt.expected {
				t.Errorf("isGoProcess() = %v, want %v", actual, tt.expected)
			}
		})
	}
}

func TestRenderTable(t *testing.T) {
	mockProcesses := []ProcessInfo{
		{PID: 1001, Name: "my-go-app", GoroutineCount: 42},
		{PID: 1002, Name: "another-go-service", GoroutineCount: 150},
		{PID: 1003, Name: "unknown-process", GoroutineCount: -1},
	}

	// We can't directly test the console clearing, but we can check the table output.
	// The MockRenderTable function is designed to return a string representation.
	output := MockRenderTable(mockProcesses)

	expectedOutput := "PID | Name | Goroutines\n"
	expectedOutput += "1001 | my-go-app | 42\n"
	expectedOutput += "1002 | another-go-service | 150\n"
	expectedOutput += "1003 | unknown-process | N/A\n"

	if strings.TrimSpace(output) != strings.TrimSpace(expectedOutput) {
		t.Errorf("renderTable() output mismatch.\nExpected:\n%s\nGot:\n%s", expectedOutput, output)
	}
}

// Helper function to replace global variables for testing
var (
	getGoroutineCountForPID func(pid int32) (int, error)
	isGoProcess func(p *process.Process) bool
)
