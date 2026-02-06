package main

import (
    "flag"
    "os"
    "reflect"
    "testing"
    "time"
)

// resetFlags restores a fresh FlagSet for each test case.
func resetFlags() {
    flag.CommandLine = flag.NewFlagSet(os.Args[0], flag.ExitOnError)
}

// TestParseArgs verifies that valid arguments produce the expected Config
// and that invalid inputs return an error.
func TestParseArgs(t *testing.T) {
    cases := []struct {
        args    []string
        want    *Config
        wantErr bool
    }{
        {
            args: []string{"-l", "8080", "-r", "example.com:80"},
            want: &Config{LocalPort: 8080, RemoteAddr: "example.com:80", Delay: 0},
            wantErr: false,
        },
        {
            args: []string{"-l", "0", "-r", "example.com:80"},
            want: nil,
            wantErr: true,
        },
        {
            args: []string{"-l", "8080", "-r", "badaddress"},
            want: nil,
            wantErr: true,
        },
        {
            args: []string{"-l", "8080", "-r", "example.com:eighty"},
            want: nil,
            wantErr: true,
        },
        {
            args: []string{"-l", "8080", "-r", "example.com:80", "-d", "150"},
            want: &Config{LocalPort: 8080, RemoteAddr: "example.com:80", Delay: 150 * time.Millisecond},
            wantErr: false,
        },
    }

    for _, tc := range cases {
        resetFlags()
        os.Args = append([]string{"cmd"}, tc.args...)
        got, err := parseArgs()
        if (err != nil) != tc.wantErr {
            t.Fatalf("parseArgs(%v) error = %v, wantErr %v", tc.args, err, tc.wantErr)
        }
        if err == nil && !reflect.DeepEqual(got, tc.want) {
            t.Fatalf("parseArgs(%v) = %+v, want %+v", tc.args, got, tc.want)
        }
    }
}
