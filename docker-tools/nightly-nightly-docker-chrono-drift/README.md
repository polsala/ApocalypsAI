# Nightly Docker Chrono-Drift Detector

The ApocalypsAI Nightly Integrator presents the "Nightly Docker Chrono-Drift Detector"! In the ever-shifting sands of the post-apocalyptic digital wasteland, containers can mysteriously acquire new traits, like a lone wanderer picking up strange trinkets. This utility helps you spot those temporal anomalies in your running Docker containers.

It scans a specified running container for:
1.  **Environment Variable Drift:** Detects environment variables present in the running container that were not defined in its original image, or variables whose values have changed.
2.  **Exposed Port Anomalies:** Identifies ports exposed by the running container that were not declared in its original image definition.
3.  **Temporal Marker Files:** Checks for the presence of a specific "chrono-drift marker" file (`/tmp/chrono_drift_marker.txt`) within the container's filesystem, indicating an unexpected alteration.

Keep your containers pristine and predictable, even when the fabric of reality is fraying!

## Usage

### 1. Build the Docker Image

```bash
docker build -t nightly-docker-chrono-drift .
```

### 2. Run the Detector

To run the detector against a live container, you need to provide it with the container's ID or name. The detector will then use `docker inspect` and `docker exec` (for filesystem checks) to gather information.

```bash
# Example: Scan a container named 'my-app-container'
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    nightly-docker-chrono-drift my-app-container
```

**Note:** The utility requires access to the Docker daemon socket (`/var/run/docker.sock`) to inspect containers and execute commands within them.

### Expected Output

The utility will print a report indicating any detected drift:

```
Scanning container: my-app-container (ID: abcdef123456)

--- Chrono-Drift Report ---

[NO DRIFT DETECTED]
Container 'my-app-container' appears stable across monitored parameters.
```

OR

```
Scanning container: my-app-container (ID: abcdef123456)

--- Chrono-Drift Report ---

Environment Variable Drift:
  - Added: MY_NEW_VAR=some_value
  - Changed: PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/new/path (was: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin)

Exposed Port Anomalies:
  - New Port Exposed: 8080/tcp

Temporal Marker File Detected:
  - Found /tmp/chrono_drift_marker.txt. This indicates an unexpected filesystem alteration.

[DRIFT DETECTED]
Container 'my-app-container' shows signs of temporal instability!
```

## Development and Testing

### Automated Tests

The tests simulate Docker daemon interactions using pre-defined JSON and text files, ensuring deterministic and offline execution.

```bash
./tests/test_chrono_drift.sh
```

This script will:
1.  Build the `nightly-docker-chrono-drift` image.
2.  Create mock `docker inspect` outputs for both an image and a container (with and without drift).
3.  Create mock `docker exec ls -R /` outputs (with and without the marker file).
4.  Run the `nightly-docker-chrono-drift` container, mounting these mock files and instructing the script to use them.
5.  Assert that the output correctly identifies drift or its absence.
