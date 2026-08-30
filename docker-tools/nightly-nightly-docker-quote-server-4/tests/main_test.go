package main

import (
    "io/ioutil"
    "net/http/httptest"
    "strings"
    "testing"
)

func TestRandomQuote(t *testing.T) {
    // Ensure the quote is one of the predefined ones
    q := randomQuote()
    found := false
    for _, v := range quotes {
        if v == q {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("randomQuote returned unknown quote: %s", q)
    }
}

func TestQuoteHandler(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/", nil)
    w := httptest.NewRecorder()
    quoteHandler(w, req)

    resp := w.Result()
    body, _ := ioutil.ReadAll(resp.Body)
    got := strings.TrimSpace(string(body))

    // Verify response is a known quote
    found := false
    for _, v := range quotes {
        if v == got {
            found = true
            break
        }
    }
    if !found {
        t.Fatalf("Handler returned unknown quote: %s", got)
    }
}
