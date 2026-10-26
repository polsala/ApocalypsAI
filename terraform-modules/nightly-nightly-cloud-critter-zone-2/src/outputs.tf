output "food_bowl_name" {
  description = "The name of the S3 bucket (Critter Food Bowl)."
  value       = aws_s3_bucket.critter_food_bowl.id
}

output "water_dish_arn" {
  description = "The ARN of the SNS topic (Critter Water Dish)."
  value       = aws_sns_topic.critter_water_dish.arn
}

output "lullaby_lambda_name" {
  description = "The name of the Lambda function (Critter Lullaby)."
  value       = aws_lambda_function.critter_lullaby_lambda.function_name
}
