# Nightly Survival Cache Inspector

## Summary

The `nightly-survival-cache-inspector` is a containerized utility designed to provide a safe and isolated way to inspect the contents and calculate the SHA256 sum of compressed archives (like `.tar.gz`, `.zip`) without extracting their contents directly onto your host system. This is particularly useful for examining potentially untrusted archives or simply quickly checking what's inside a 'survival cache' without cluttering your local filesystem.

## How it works

The utility builds a small Docker image containing `tar`, `unzip`, and `sha256sum`. When run, you mount your archive into the container, and the internal script automatically detects the archive type and lists its contents, along with providing the SHA256 hash of the archive file itself.

## Usage

1.  **Build the Docker image (if not already built):**

    ```bash
    docker build -t nightly-survival-cache-inspector .
    ```

2.  **Inspect an archive:**

    Replace `/path/to/your/archive.tar.gz` with the actual path to your archive file.

    ```bash
    docker run --rm -v /path/to/your/archive.tar.gz:/mnt/cache/archive.tar.gz nightly-survival-cache-inspector /mnt/cache/archive.tar.gz
    ```

    **Example for a `.zip` file:**

    ```bash
    docker run --rm -v /path/to/your/my_cache.zip:/mnt/cache/my_cache.zip nightly-survival-cache-inspector /mnt/cache/my_cache.zip
    ```

    The output will include the SHA256 sum of the archive and a listing of its contents.

## Development & Testing

To run the automated tests, ensure you have `docker` and `bash` installed. The tests will build the Docker image, create dummy archive files, run the inspector against them, and verify the output.

```bash
./tests/test_inspector.sh
```
