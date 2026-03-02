nightly-wasteland-weather-sim

Dockerized CLI that generates whimsical post-apocalyptic weather forecasts for any location and day offset.

Build:
	docker build -t wasteland-weather .

Usage:
	docker run --rm wasteland-weather "New York" 2

The forecast is deterministic: based on the sum of ASCII codes of the location and offset, so the same inputs always produce the same weather.

Testing:
	cd tests
	bash test_weather.sh
