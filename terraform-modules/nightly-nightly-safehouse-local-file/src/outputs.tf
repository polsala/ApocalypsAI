output "file_path" {
  description = "Absolute path of the generated safehouse log file."
  value       = local_file.safehouse.filename
}
