output "full_path" {
  description = "Full path of the created file"
  value       = local_file.output.filename
}

output "random_suffix" {
  description = "Random suffix added to the file name"
  value       = random_id.suffix.hex
}
