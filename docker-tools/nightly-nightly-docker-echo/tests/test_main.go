package main

import (
    \"net/http\"
    \"net/http/httptest\"
    \"testing\"
)

func TestEchoHandler(t *testing.T) {
    req := httptest.NewRequest(\"GET\", \"/echo?msg=Test\", nil)
    w := httptest.NewRecorder()
    echoHandler(w, req)
    resp := w.Result()
    body := w.Body.String()
    if body != \"Test\" {
        t.Fatalf(\"expected 'Test', got %q\", body)
    }
}

func TestEchoHandlerDefault(t *testing.T) {
    req := httptest.NewRequest(\"GET\", \"/echo\", nil)
    w := httptest.NewRecorder()
    echoHandler(w, req)
    body := w.Body.String()
    if body != \"Hello, world!\" {
        t.Fatalf(\"expected default greeting, got %q\", body)
    }
}

