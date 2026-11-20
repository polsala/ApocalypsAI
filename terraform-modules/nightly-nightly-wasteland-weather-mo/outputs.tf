output "forecast_path" {\n  description = "Path to the generated JSON file"\n  value       = local_file.weather_json.filename\n}\n
