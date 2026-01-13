package main

import (
    "bytes"
    "io"
    "io/ioutil"
    "os"
    "testing"
)

func TestEmojiLoggerWithFile(t *testing.T) {
    content := "first
second
third
"
    tmpfile, err := ioutil.TempFile("", "log")
    if err != nil {
        t.Fatal(err)
    }
    defer os.Remove(tmpfile.Name())
    if _, err := tmpfile.WriteString(content); err != nil {
        t.Fatal(err)
    }
    tmpfile.Close()

    // Capture stdout
    oldStdout := os.Stdout
    r, w, _ := os.Pipe()
    os.Stdout = w

    os.Args = []string{"emoji-logger", tmpfile.Name()}
    main()

    w.Close()
    var buf bytes.Buffer
    io.Copy(&buf, r)
    os.Stdout = oldStdout

    expected := "ð first
ð± second
ð third
"
    if buf.String() != expected {
        t.Fatalf("expected %q, got %q", expected, buf.String())
    }
}

func TestEmojiLoggerWithStdin(t *testing.T) {
    input := "alpha
beta
"
    r := bytes.NewBufferString(input)
    oldStdin := os.Stdin
    os.Stdin = r
    defer func() { os.Stdin = oldStdin }()

    // Capture stdout
    oldStdout := os.Stdout
    outR, outW, _ := os.Pipe()
    os.Stdout = outW

    os.Args = []string{"emoji-logger"}
    main()

    outW.Close()
    var buf bytes.Buffer
    io.Copy(&buf, outR)
    os.Stdout = oldStdout

    expected := "ð alpha
ð± beta
"
    if buf.String() != expected {
        t.Fatalf("expected %q, got %q", expected, buf.String())
    }
}

