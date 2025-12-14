package main

func rot13(s string) string {
    r := []rune(s)
    for i, c := range r {
        switch {
        case 'a' <= c && c <= 'z':
            r[i] = 'a' + (c-'a'+13)%26
        case 'A' <= c && c <= 'Z':
            r[i] = 'A' + (c-'A'+13)%26
        default:
            // leave unchanged
        }
    }
    return string(r)
}
