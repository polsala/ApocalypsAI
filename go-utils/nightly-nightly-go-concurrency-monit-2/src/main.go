package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"github.com/shirou/gopsutil/process"
	"github.com/olekukonina/tablewriter"
)

// ProcessInfo holds information about a Go process and its goroutines.
type ProcessInfo struct {
	PID           int32
	Name          string
	GoroutineCount int
}

func main() {
	fmt.Println("Starting Go Concurrency Monitor...")
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	for range ticker.C {
		processInfos, err := getGoProcessInfos()
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error getting process info: %v\n", err)
			continue
		}

		renderTable(processInfos)
	}
}

// isGoProcess checks if a given process is a Go executable.
// This is a simplified check and might not be exhaustive.
func isGoProcess(p *process.Process) bool {
	name, err := p.Name() // Get process name
	if err != nil {
		return false
	}

	// Basic check: look for common Go executable names or extensions.
	// A more robust check might involve inspecting the binary itself, but that's complex.
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

// getGoProcessInfos retrieves information about running Go processes.
func getGoProcessInfos() ([]ProcessInfo, error) {
	var infos []ProcessInfo

	// Get all running processes
	procs, err := process.Processes()
	if err != nil {
		return nil, fmt.Errorf("failed to get processes: %w", err)
	}

	for _, p := range procs {
		if !isGoProcess(p) {
			continue
		}

		name, err := p.Name()
		if err != nil {
			// Silently skip processes we can't get info for
			continue
		}

		// Attempt to get goroutine count. This requires attaching to the process's runtime.
		// This is a complex operation and often requires elevated privileges or specific tooling.
		// For this utility, we'll simulate this by running `go tool pprof -goroutine=1 <pid>`
		// and parsing its output. This is a simplification for demonstration.
		// In a real-world scenario, you might use a Go agent that exposes metrics via RPC or a shared memory segment.

		goroutineCount, err := getGoroutineCountForPID(p.Pid)
		if err != nil {
			// If we can't get the goroutine count, we still list the process but with a placeholder.
			infos = append(infos, ProcessInfo{PID: p.Pid, Name: name, GoroutineCount: -1}) // -1 indicates unknown
			continue
		}

		infos = append(infos, ProcessInfo{PID: p.Pid, Name: name, GoroutineCount: goroutineCount})
	}

	return infos, nil
}

// getGoroutineCountForPID attempts to get the goroutine count for a given PID.
// This is a simplified implementation using `go tool pprof`.
func getGoroutineCountForPID(pid int32) (int, error) {
	// Ensure 'go' command is available in PATH
	_, err := exec.LookPath("go")
	if err != nil {
		return 0, fmt.Errorf("go command not found: %w", err)
	}

	// Construct the command: go tool pprof -goroutine=1 <pid>
	// We need to capture stdout to parse the goroutine count.
	cmd := exec.Command("go", "tool", "pprof", fmt.Sprintf("-goroutine=1"), fmt.Sprintf("%d", pid))
	
	// Redirect stderr to stdout to capture potential errors from pprof
	stderr, err := cmd.StderrPipe()
	if err != nil {
		return 0, fmt.Errorf("failed to create stderr pipe: %w", err)
	}

	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return 0, fmt.Errorf("failed to create stdout pipe: %w", err)
	}

	if err := cmd.Start(); err != nil {
		return 0, fmt.Errorf("failed to start pprof command: %w", err)
	}

	// Read from stdout and stderr
	stdoutOutput, _ := os.ReadAll(stdout)
	stderrOutput, _ := os.ReadAll(stderr)

	if err := cmd.Wait(); err != nil {
		// If pprof fails, it might be because the process is not a Go process or is not running.
		// We'll return an error, but the caller should handle it gracefully.
		return 0, fmt.Errorf("pprof command failed: %s, stderr: %s", err.Error(), string(stderrOutput))
	}

	// Parse the output to find the goroutine count.
	// The output typically looks like: "goroutine 123 [running]:"
	// We'll look for the line starting with "goroutine " and extract the number.
	lines := strings.Split(string(stdoutOutput), "\n")
	for _, line := range lines {
		if strings.HasPrefix(line, "goroutine ") {
			fields := strings.Fields(line)
			if len(fields) > 1 {
				var count int
				_, err := fmt.Sscan(fields[1], &count)
				if err == nil {
					return count, nil
				}
			}
		}
	}

	return 0, fmt.Errorf("could not parse goroutine count from pprof output. Output: %s, Stderr: %s", string(stdoutOutput), string(stderrOutput))
}

// renderTable displays the process information in a table.
func renderTable(processes []ProcessInfo) {
	// Clear the console for a live-updating effect
	// This is a basic approach and might not work in all terminals.
	cmd := exec.Command("clear") // or "cls" on Windows
	if runtime.GOOS == "windows" {
		cmd = exec.Command("cmd", "/c", "cls")
	}
	cmd.Stdout = os.Stdout
	cmd.Run()

	table := tablewriter.NewWriter(os.Stdout)
	ttable.SetHeader([]string{"PID", "Name", "Goroutines"})

	for _, p := range processes {
		goroutineStr := fmt.Sprintf("%d", p.GoroutineCount)
		if p.GoroutineCount == -1 {
			goroutineStr = "N/A"
		}
		table.AppendRow([]string{
			fmt.Sprintf("%d", p.PID),
			p.Name,
			goroutineStr,
		})
	}
	ttable.Render()
}

// Mock implementations for testing purposes

// MockProcessInfo holds mocked process information.
type MockProcessInfo struct {
	PID           int32
	Name          string
	GoroutineCount int
}

// MockGetGoProcessInfos simulates retrieving Go process information.
func MockGetGoProcessInfos() ([]MockProcessInfo, error) {
	return []MockProcessInfo{
		{PID: 1234, Name: "my-go-app", GoroutineCount: 50},
		{PID: 5678, Name: "another-go-service", GoroutineCount: 120},
		{PID: 9012, Name: "non-go-process", GoroutineCount: 10}, // This should be filtered out
	},
		nil
}

// MockRenderTable simulates rendering a table.
func MockRenderTable(processes []MockProcessInfo) string {
	var sb strings.Builder
	ssb.WriteString("PID | Name | Goroutines\n")
	for _, p := range processes {
		sb.WriteString(fmt.Sprintf("%d | %s | %d\n", p.PID, p.Name, p.GoroutineCount))
	}
	return sb.String()
}
