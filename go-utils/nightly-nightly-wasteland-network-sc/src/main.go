package main

import (
    "flag"
    "fmt"
    "net"
    "strings"
    "sync"
    "time"
)

var adjectives = []string{
    "Radiated Raider",
    "Wasteland Wanderer",
    "Dusty Drifter",
    "Cursed Crusader",
    "Bleak Brawler",
    "Ghoul Gambler",
    "Ashen Archer",
    "Mire Marauder",
}

// generateName returns a whimsical name based on the IP address.
func generateName(ip string) string {
    // Simple deterministic hash: sum of bytes modulo len(adjectives)
    parts := strings.Split(ip, ".")
    sum := 0
    for _, p := range parts {
        var v int
        fmt.Sscanf(p, "%d", &v)
        sum += v
    }
    return adjectives[sum%len(adjectives)]
}

// scanHost probes the given ports on host using the supplied dial function.
// It returns a slice of open ports.
func scanHost(host string, ports []int, dial func(network, address string) (net.Conn, error)) []int {
    var open []int
    for _, p := range ports {
        address := fmt.Sprintf("%s:%d", host, p)
        conn, err := dial("tcp", address)
        if err == nil {
            open = append(open, p)
            conn.Close()
        }
    }
    return open
}

// defaultDial is the production dialer with a short timeout.
func defaultDial(network, address string) (net.Conn, error) {
    return net.DialTimeout(network, address, 500*time.Millisecond)
}

// ipRange returns all IP addresses in the CIDR block.
func ipRange(cidr string) ([]string, error) {
    ip, ipnet, err := net.ParseCIDR(cidr)
    if err != nil {
        return nil, err
    }
    var ips []string
    for ip := ip.Mask(ipnet.Mask); ipnet.Contains(ip); incIP(ip) {
        ips = append(ips, ip.String())
    }
    // remove network and broadcast addresses
    if len(ips) > 2 {
        return ips[1 : len(ips)-1], nil
    }
    return ips, nil
}

// incIP increments an IP address.
func incIP(ip net.IP) {
    for j := len(ip) - 1; j >= 0; j-- {
        ip[j]++
        if ip[j] > 0 {
            break
        }
    }
}

func main() {
    cidr := flag.String("cidr", "", "CIDR block to scan (e.g., 192.168.1.0/24)")
    portsStr := flag.String("ports", "22,80,443", "Comma-separated list of TCP ports")
    flag.Parse()

    if *cidr == "" {
        fmt.Println("Error: -cidr flag is required")
        return
    }

    portParts := strings.Split(*portsStr, ",")
    var ports []int
    for _, p := range portParts {
        var v int
        fmt.Sscanf(strings.TrimSpace(p), "%d", &v)
        if v > 0 {
            ports = append(ports, v)
        }
    }

    hosts, err := ipRange(*cidr)
    if err != nil {
        fmt.Printf("Invalid CIDR: %v\n", err)
        return
    }

    var wg sync.WaitGroup
    sem := make(chan struct{}, 100) // limit concurrency

    for _, host := range hosts {
        wg.Add(1)
        go func(h string) {
            defer wg.Done()
            sem <- struct{}{}
            open := scanHost(h, ports, defaultDial)
            <-sem
            if len(open) > 0 {
                name := generateName(h)
                fmt.Printf("Host %s (%s) open ports: %s\n", h, name, intsToString(open))
            }
        }(host)
    }
    wg.Wait()
}

// intsToString joins ints with commas.
func intsToString(ints []int) string {
    var parts []string
    for _, v := range ints {
        parts = append(parts, fmt.Sprintf("%d", v))
    }
    return strings.Join(parts, ", ")
}
