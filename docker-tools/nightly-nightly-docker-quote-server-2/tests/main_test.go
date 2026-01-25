package main

import (
    "io/ioutil"
    "net/http/httptest"
    "strings"
    "testing"
)

func TestQuoteHandlerReturnsValidQuote(t *testing.T) {
    req := httptest.NewRequest("GET", "/", nil)
    w := httptest.NewRecorder()
    quoteHandler(w, req)
    resp := w.Result()
    body, _ := ioutil.ReadAll(resp.Body)
    got := strings.TrimSpace(string(body))
    valid := false
    for _, q := range quotes {
        if got == q {
            valid = true
            break
        }
    }
    if !valid {
        t.Fatalf("unexpected quote: %q", got)
    }
}
