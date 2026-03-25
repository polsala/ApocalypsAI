output "manifest_path" {
  description = "Path to the generated manifest file."
  value       = local_file.manifest.filename
}
