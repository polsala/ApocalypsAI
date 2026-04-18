import os
import importlib.util
import unittest.mock as mock

def load_forecast_module():
    module_path = os.path.abspath(os.path.join('..', 'src', 'forecast.py'))
    spec = importlib.util.spec_from_file_location('forecast', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_generate_fixed():
    forecast = load_forecast_module()
    with mock.patch('random.choice', return_value=("Snowy", "\u2744\uFE0F")):
        result = forecast.generate()
        assert result == "Snowy today! \u2744\uFE0F"
