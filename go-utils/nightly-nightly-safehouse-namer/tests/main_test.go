package main

import (
    "regexp"
    "strings"
    "testing"
)

func contains(slice []string, item string) bool {
    for _, v := range slice {
        if v == item {
            return true
        }
    }
    return false
}

func TestGenerateNamePattern(t *testing.T) {
    name := generateName()
    pattern := `^[A-Za-z]+ [A-Za-z]+$`
    matched, err := regexp.MatchString(pattern, name)
    if err != nil {
        t.Fatalf("regex error: %v", err)
    }
    if !matched {
        t.Fatalf("generated name %q does not match pattern", name)
    }
}

func TestGenerateNameComponents(t *testing.T) {
    name := generateName()
    parts := strings.Split(name, " ")
    if len(parts) != 2 {
        t.Fatalf("expected two parts, got %d", len(parts))
    }
    adj, noun := parts[0], parts[1]
    if !contains(adjectives, adj) {
        t.Fatalf("adjective %q not in list", adj)
    }
    if !contains(nouns, noun) {
        t.Fatalf("noun %q not in list", noun)
    }
}
