output "random_string" {
  description = "The generated random string (hex encoded)"
  value       = random_id.rand.hex
}

output "file_path" {
  description = "Absolute path to the created file"
  value       = local_file.output.filename
}
