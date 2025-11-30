# Nightly Resource Scavenger Link Checker

## Description

In the desolate landscape of the post-apocalypse, reliable information sources are paramount. The `nightly-resource-scavenger-link-checker` is a Python utility designed to help survivors (and their AI overlords) maintain a pristine list of online resources. It takes a file containing a list of URLs, checks their availability using HTTP HEAD requests, and reports any broken or unreachable links.

Keep your digital survival guide up-to-date, ensuring that when you need that crucial schematic for a makeshift water purifier or the last known location of a pre-collapse data cache, the link still works!

## Usage

1.  **Prepare your link list**: Create a plain text file (e.g., `resources.txt`) with one URL per line.

    ```
    https://example.com/working-resource
    https://broken.link/old-data
    https://another.valid.site/info
    http://nonexistent.domain/page
    ```

2.  **Run the scavenger**: Execute the script with your link list file as an argument.

    ```bash
    python src/scavenger.py resources.txt
    ```

## Example Output

```
Scanning 4 URLs...

[✅ 200] https://example.com/working-resource
[❌ 404] https://broken.link/old-data
[✅ 200] https://another.valid.site/info
[❌ ERR] http://nonexistent.domain/page (ConnectionError: DNS lookup failed)

--- Scan Summary ---
Total URLs: 4
Working URLs: 2
Broken URLs: 2
```

## Dependencies

This utility requires the `requests` library. Install it using pip:

```bash
pip install requests
```
