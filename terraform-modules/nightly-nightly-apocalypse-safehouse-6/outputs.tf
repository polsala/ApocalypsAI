output "config_path" {
  description = "Absolute path to the generated bucket configuration JSON file"
  value       = local_file.bucket_config.filename
}
