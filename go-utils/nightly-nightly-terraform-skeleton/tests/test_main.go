package main

import (
	"os"
	"path/filepath"
	"testing"
)

func TestCreateSkeleton(t *testing.T) {
	tmpDir := t.TempDir()
	err := createSkeleton(tmpDir)
	if err != nil {
		t.Fatalf("createSkeleton returned error: %v", err)
	}
	expectedFiles := []string{
		"main.tf",
		"variables.tf",
		"outputs.tf",
		"README.md",
		".gitignore",
	}
	for _, f := range expectedFiles {
		path := filepath.Join(tmpDir, f)
		info, err := os.Stat(path)
		if err != nil {
			t.Fatalf("expected file %s to exist, but got error: %v", f, err)
		}
		if info.IsDir() {
			t.Fatalf("expected %s to be a file, but it's a directory", f)
		}
		content, err := os.ReadFile(path)
		if err != nil {
			t.Fatalf("failed to read file %s: %v", f, err)
		}
		if len(content) == 0 {
			t.Fatalf("file %s is empty", f)
		}
	}
}

