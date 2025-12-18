module "chaos_monkey" {
  source = "../../"
  
  enabled = true
  intensity = 0.2
  safe_mode = false
  cloud_provider = "aws"
  region = "us-west-2"
  resources = [
    "aws_instance.web-1",
    "aws_instance.web-2",
    "aws_db_instance.main",
    "aws_elasticache_cluster.cache"
  ]
}

resource "aws_instance" "web-1" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  
  lifecycle {
    ignore_changes = [ami] # Ignore changes to test chaos
  }
}

resource "aws_instance" "web-2" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  
  lifecycle {
    ignore_changes = [ami]
  }
}

resource "aws_db_instance" "main" {
  identifier = "chaos-db"
  engine     = "postgres"
  
  lifecycle {
    ignore_changes = [engine]
  }
}

resource "aws_elasticache_cluster" "cache" {
  cluster_id = "chaos-cache"
  engine     = "redis"
  
  lifecycle {
    ignore_changes = [engine]
  }
}
