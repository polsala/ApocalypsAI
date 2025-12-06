# Nightly Wasteland Weather Station

## Overview

The "Wasteland Weather Station" is a rugged, containerized utility designed to provide essential atmospheric data for survivors navigating the post-apocalyptic landscape. It fetches current weather conditions for a specified location and presents them in a stylized, terminal-friendly format, helping you plan your scavenging runs or shelter from the next dust storm.

## Features

*   **Location-Specific Forecasts**: Get real-time weather for any city or coordinate.
*   **Wasteland Styling**: Output is formatted with a gritty, terminal-friendly aesthetic.
*   **Containerized**: Easy to deploy and run anywhere Docker is available, ensuring minimal dependencies.
*   **Essential Data**: Displays temperature, "feels like" temperature (for radiation exposure, of course), weather description, wind speed/direction, and humidity.

## Usage

### Prerequisites

*   Docker installed on your system.
*   An API key from OpenWeatherMap (or a similar weather API). You can get one for free at [OpenWeatherMap](https://openweathermap.org/api).

### Running the Weather Station

1.  **Build the Docker Image**:
    ```bash
    docker build -t wasteland-weather-station .
    ```

2.  **Run the Container**:
    You need to provide your OpenWeatherMap API key and the desired location.

    *   **By City Name**:
        ```bash
        docker run --rm -e API_KEY="YOUR_OPENWEATHERMAP_API_KEY" -e LOCATION="London" wasteland-weather-station
        ```
        (Replace "London" with your desired city, e.g., "New York", "Tokyo", "Mos Eisley")

    *   **By Latitude and Longitude**:
        ```bash
        docker run --rm -e API_KEY="YOUR_OPENWEATHERMAP_API_KEY" -e LAT="34.0522" -e LON="-118.2437" wasteland-weather-station
        ```
        (Replace with your desired coordinates)

    *   **Example Output**:
        ```
        +-------------------------------------+
        |  Wasteland Weather Report           |
        +-------------------------------------+
        | Location: New York                  |
        | Conditions: Scattered Clouds ☁️      |
        | Temperature: 25°C (Feels like: 27°C)|
        | Wind: 10 km/h NE                    |
        | Humidity: 60%                       |
        +-------------------------------------+
        ```

### Configuration

The utility uses the following environment variables:

*   `API_KEY` (Required): Your OpenWeatherMap API key.
*   `LOCATION` (Optional): The city name (e.g., "Tokyo"). If `LAT` and `LON` are provided, this is ignored.
*   `LAT` (Optional): Latitude for coordinates-based lookup. Must be used with `LON`.
*   `LON` (Optional): Longitude for coordinates-based lookup. Must be used with `LAT`.

    **Note**: You must provide either `LOCATION` or both `LAT` and `LON`. If neither is provided, it will default to a pre-defined wasteland location (e.g., "Chernobyl").

## Development

### Project Structure

```
.
├── Dockerfile
├── README.md
├── requirements.txt
├── src/
│   └── app.py
└── tests/
    ├── test_app.py
    └── run_tests.sh
```

### Running Tests

To run the unit tests for the Python script within the container:

```bash
./tests/run_tests.sh
```

This script will build the Docker image and then execute the Python unit tests inside a temporary container.
