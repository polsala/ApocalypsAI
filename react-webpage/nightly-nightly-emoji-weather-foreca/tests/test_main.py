import pathlib


def test_main_contains_component():
    main_path = pathlib.Path('src/main.jsx')
    assert main_path.exists(), "src/main.jsx should exist"
    content = main_path.read_text()
    assert 'function EmojiWeatherForecast' in content, "Component should be defined"
    assert 'const forecastData' in content, "Forecast data should be defined"


def test_index_includes_script():
    index_path = pathlib.Path('src/index.html')
    assert index_path.exists(), "src/index.html should exist"
    content = index_path.read_text()
    assert '<script type="module" src="main.jsx"></script>' in content, "index.html should load main.jsx"
    assert 'react.development.js' in content, "React CDN should be loaded"
