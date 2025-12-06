# Interdimensional Portal Pinger

## 🌌 Cosmic Connectivity Monitor 🌌

Are your critical services still tethered to our reality, or have they slipped into a rogue dimension? The **Interdimensional Portal Pinger** is here to help! This whimsical-yet-useful utility allows you to monitor the 'cosmic connectivity' of your vital 'interdimensional portals' (read: URLs or IP addresses).

It attempts to establish contact with each specified portal and reports its status, helping you quickly identify if a service has gone offline, timed out, or simply vanished into the void.

## Usage

1.  **Prepare your Portals List**: Create a file named `portals.txt` in the same directory as `src/pinger.py`. Each line in this file should be a URL or IP address representing an 'interdimensional portal' you wish to monitor.

    Example `portals.txt`:
    ```
    https://www.google.com
    http://localhost:8080/api/status
    https://apocalypsai.dev
    http://192.168.1.1
    # This is a comment and will be ignored

    ```

2.  **Run the Pinger**: Execute the `pinger.py` script.

    ```bash
    python src/pinger.py
    ```

## Example Output

```
🌌 Initiating Interdimensional Portal Ping... 🌌

[https://www.google.com] - ONLINE (Status: 200)
[http://localhost:8080/api/status] - OFFLINE (Connection Error)
[https://apocalypsai.dev] - ONLINE (Status: 200)
[http://192.168.1.1] - UNKNOWN_ERROR (Request Timeout)

🌌 Interdimensional Scan Complete. 🌌
```

## Configuration

*   **`portals.txt`**: A plain text file, one URL/IP per line, specifying the endpoints to ping. Lines starting with `#` and empty lines are ignored.
*   **Timeout**: The pinger uses a default timeout of 5 seconds per request. This can be adjusted within `src/pinger.py` if needed.

## Requirements

*   Python 3.x
*   `requests` library (`pip install requests`)
