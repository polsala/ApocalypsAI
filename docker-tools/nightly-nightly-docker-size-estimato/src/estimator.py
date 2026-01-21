import sys
import requests


def get_image_size(image: str) -> int:
    """
    Returns the compressed size of a Docker Hub image tag in megabytes.
    """
    if ":" in image:
        name, tag = image.split(":", 1)
    else:
        name, tag = image, "latest"
    if "/" not in name:
        # Official library images are under the "library" namespace
        namespace = "library"
        repo = name
    else:
        namespace, repo = name.split("/", 1)
    url = f"https://hub.docker.com/v2/repositories/{namespace}/{repo}/tags/{tag}/"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    size_bytes = data.get("full_size", 0)
    size_mb = size_bytes / (1024 * 1024)
    return int(size_mb)


def main():
    if len(sys.argv) < 2:
        print("Usage: estimator <image>[:tag]")
        sys.exit(1)
    image = sys.argv[1]
    try:
        size = get_image_size(image)
        print(f"{image} size: {size} MB")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
