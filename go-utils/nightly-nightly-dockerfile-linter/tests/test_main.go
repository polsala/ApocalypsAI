package main

import (
    "strings"
    "testing"
)

func TestLintDockerfile_OK(t *testing.T) {
    dockerfile := `
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y curl
CMD ["bash"]
`
    issues := lintDockerfile(strings.NewReader(dockerfile))
    if len(issues) != 0 {
        t.Fatalf("Expected no issues, got %v", issues)
    }
}

func TestLintDockerfile_MissingFrom(t *testing.T) {
    dockerfile := `
RUN apt-get update && apt-get install -y curl
CMD ["bash"]
`
    issues := lintDockerfile(strings.NewReader(dockerfile))
    if !contains(issues, "Missing FROM instruction") {
        t.Fatalf("Expected missing FROM issue, got %v", issues)
    }
}

func TestLintDockerfile_MissingCmd(t *testing.T) {
    dockerfile := `
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y curl
`
    issues := lintDockerfile(strings.NewReader(dockerfile))
    if !contains(issues, "Missing CMD or ENTRYPOINT instruction") {
        t.Fatalf("Expected missing CMD/ENTRYPOINT issue, got %v", issues)
    }
}

func TestLintDockerfile_AddInstruction(t *testing.T) {
    dockerfile := `
FROM ubuntu:20.04
ADD . /app
CMD ["bash"]
`
    issues := lintDockerfile(strings.NewReader(dockerfile))
    if !contains(issues, "ADD instruction found; use COPY instead") {
        t.Fatalf("Expected ADD issue, got %v", issues)
    }
}

func TestLintDockerfile_AptGetUpdateWithoutInstall(t *testing.T) {
    dockerfile := `
FROM ubuntu:20.04
RUN apt-get update
CMD ["bash"]
`
    issues := lintDockerfile(strings.NewReader(dockerfile))
    if !contains(issues, "RUN apt-get update without apt-get install -y") {
        t.Fatalf("Expected apt-get update without install issue, got %v", issues)
    }
}

func contains(slice []string, item string) bool {
    for _, v := range slice {
        if v == item {
            return true
        }
    }
    return false
}
