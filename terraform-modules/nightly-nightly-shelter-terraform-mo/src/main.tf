resource "random_pet" "shelter_name" {
  length = 2
}

resource "aws_s3_bucket" "shelter_bucket" {
  bucket = "${var.bucket_name_prefix}${random_pet.shelter_name.id}"
  acl    = "private"
}
