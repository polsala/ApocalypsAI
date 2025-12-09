resource "aws_vpc" "sandbox" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "${var.owner}-chaos-${random_string.suffix.result}"
  }
}

resource "aws_security_group" "restricted" {
  vpc_id = aws_vpc.sandbox.id
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
}

resource "aws_instance" "chaos_node" {
  count = 3
  ami = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  tags = {
    Name = "ChaosNode-${count.index + 1}"
  }
}

resource "aws_cloudwatch_event_rule" "self_destruct" {
  name = "sandbox-cleanup"
  schedule_expression = "rate(24h)"
}

resource "aws_cloudwatch_event_target" "self_destruct" {
  rule = aws_cloudwatch_event_rule.self_destruct.name
  arn = "arn:aws:lambda:...
