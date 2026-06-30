module "test_beacon" {
  source = "../src"

  bucket_name_prefix    = "test-apocalypsai-whisper"
  region                = "us-east-1"
  initial_whisper_message = "Test whisper: The code compiles, for now."
}
