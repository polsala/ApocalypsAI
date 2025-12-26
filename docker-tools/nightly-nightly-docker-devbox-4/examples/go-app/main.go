package main

import (
	"encoding/json"
	"fmt"
	"os"
	"runtime"
	"time"
)

type SystemInfo struct {
	GoVersion         string `json:"go_version"`
	CurrentTime       string `json:"current_time"`
	WorkingDirectory  string `json:"working_directory"`
	Platform          string `json:"platform"`
	Architecture      string `json:"architecture"`
}

func main() {
	info := getSystemInfo()
	
	// Check if -json flag is provided
	if len(os.Args) > 1 && os.Args[1] == "-json" {
		jsonOutput, err := json.MarshalIndent(info, "", "  ")
		if err != nil {
			panic(err)
		}
		fmt.Println(string(jsonOutput))
	} else {
		printHumanReadable(info)
	}
}

func getSystemInfo() SystemInfo {
	currentTime := time.Now().Format(time.RFC3339)
	workingDir, _ := os.Getwd()
	platform := fmt.Sprintf("%s %s", runtime.GOOS, runtime.GOARCH)
	
	return SystemInfo{
		GoVersion:        runtime.Version(),
		CurrentTime:      currentTime,
		WorkingDirectory: workingDir,
		Platform:         platform,
		Architecture:     runtime.GOARCH,
	}
}

func printHumanReadable(info SystemInfo) {
	fmt.Println("🐹 Welcome to the Go Development Environment!")
	fmt.Printf("Go version: %s\n", info.GoVersion)
	fmt.Printf("Current time: %s\n", info.CurrentTime)
	fmt.Printf("Working directory: %s\n", info.WorkingDirectory)
	fmt.Printf("Platform: %s\n", info.Platform)
	fmt.Printf("Architecture: %s\n", info.Architecture)
	
	fmt.Println("\n📊 Basic Go functionality:")
	
	// Slice example
	squares := make([]int, 10)
	for i := 0; i < 10; i++ {
		squares[i] = (i + 1) * (i + 1)
	}
	fmt.Printf("Squares 1-10: %v\n", squares)
	
	// Map example
	wordLengths := make(map[string]int)
	for _, word := range []string{"hello", "world", "go", "devbox"} {
		wordLengths[word] = len(word)
	}
	fmt.Printf("Word lengths: %v\n", wordLengths)
	
	fmt.Println("\n🎉 Go environment is ready for development!")
}
