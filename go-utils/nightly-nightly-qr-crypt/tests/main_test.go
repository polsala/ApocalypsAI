package main

import "testing"

func TestGenerateQR(t *testing.T) {
    input := "test"
    // Expected pattern derived from SHA‑256("test")
    expected := "#  #####\n#    ## \n## #    \n#      #\n#   #   \n #  ##  \n ##### #\n ##  # #"
    got := generateQR(input)
    if got != expected {
        t.Fatalf("generateQR(%q) = \n%q\nexpected:\n%q", input, got, expected)
    }
}
