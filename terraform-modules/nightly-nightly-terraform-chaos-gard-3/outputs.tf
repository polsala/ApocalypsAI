output "garden_health" {
  value = "${var.garden_name} is ${100 - (var.chaos_factor * 100)}% healthy"
}

output "surviving_resources" {
  value = [
    for bucket in aws_s3_bucket.garden_buckets : bucket.id
    if random_integer.chaos_seed.result > (var.chaos_factor * 100)
  ]
}

output "destroyed_resources" {
  value = [
    for bucket in aws_s3_bucket.garden_buckets : bucket.id
    if random_integer.chaos_seed.result <= (var.chaos_factor * 100)
  ]
}

output "dashboard_url" {
  value = aws_cloudwatch_dashboard.garden_dashboard.dashboard_arn
}
