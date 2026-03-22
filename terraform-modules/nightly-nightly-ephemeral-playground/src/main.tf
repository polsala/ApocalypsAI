resource "random_pet" "name" {
  length    = 2
  separator = "-"
}

resource "aws_vpc" "playground_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name              = "ephemeral-playground-vpc-${random_pet.name.id}"
    ManagedBy         = "ApocalypsAI-NightlyIntegrator"
    EphemeralPlayground = "true"
  }
}

resource "aws_subnet" "playground_subnet" {
  vpc_id                  = aws_vpc.playground_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.region}a" # Assuming 'a' zone exists
  map_public_ip_on_launch = true
  tags = {
    Name              = "ephemeral-playground-subnet-${random_pet.name.id}"
    ManagedBy         = "ApocalypsAI-NightlyIntegrator"
    EphemeralPlayground = "true"
  }
}

resource "aws_internet_gateway" "playground_igw" {
  vpc_id = aws_vpc.playground_vpc.id
  tags = {
    Name              = "ephemeral-playground-igw-${random_pet.name.id}"
    ManagedBy         = "ApocalypsAI-NightlyIntegrator"
    EphemeralPlayground = "true"
  }
}

resource "aws_route_table" "playground_rt" {
  vpc_id = aws_vpc.playground_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.playground_igw.id
  }
  tags = {
    Name              = "ephemeral-playground-rt-${random_pet.name.id}"
    ManagedBy         = "ApocalypsAI-NightlyIntegrator"
    EphemeralPlayground = "true"
  }
}

resource "aws_route_table_association" "playground_rta" {
  subnet_id      = aws_subnet.playground_subnet.id
  route_table_id = aws_route_table.playground_rt.id
}

resource "aws_security_group" "playground_sg" {
  vpc_id      = aws_vpc.playground_vpc.id
  name        = "ephemeral-playground-sg-${random_pet.name.id}"
  description = "Allow SSH access to ephemeral playground"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: For demo, restrict in production
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name              = "ephemeral-playground-sg-${random_pet.name.id}"
    ManagedBy         = "ApocalypsAI-NightlyIntegrator"
    EphemeralPlayground = "true"
  }
}

resource "aws_key_pair" "playground_key" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

resource "aws_instance" "playground_instance" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.playground_subnet.id
  vpc_security_group_ids      = [aws_security_group.playground_sg.id]
  key_name                    = aws_key_pair.playground_key.key_name
  associate_public_ip_address = true

  tags = {
    Name              = "Ephemeral-Playground-Instance-${random_pet.name.id}"
    ManagedBy         = "ApocalypsAI-NightlyIntegrator"
    EphemeralPlayground = "true"
    DestroyAfter      = formatdate("YYYY-MM-DD'T'HH:MM:SSZ", timeadd(timestamp(), "${var.destroy_after_hours}h"))
  }
}
