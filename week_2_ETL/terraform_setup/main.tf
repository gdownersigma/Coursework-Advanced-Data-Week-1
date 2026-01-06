provider "aws" {
  region     = var.AWS_REGION
  access_key = var.AWS_ID
  secret_key = var.AWS_SECRET
}

data "aws_vpc" "c21-vpc" {
  id = var.VPC_ID
}

# Find a public subnet in the VPC (we need this for the EC2 instance)
data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [var.VPC_ID]
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# SECTION 4: Security Group
# This controls what network traffic can reach your server
resource "aws_security_group" "pipeline_sg" {
  name   = "c21-george-pipeline-sg"
  vpc_id = data.aws_vpc.c21-vpc.id

  # Allow SSH access (port 22) so you can connect to the server
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # From anywhere
  }

  # Allow all outbound traffic (so the server can reach Kafka and your database)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # All protocols
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# SECTION 5: The EC2 Instance
# This is the actual server that will run your pipeline
resource "aws_instance" "pipeline" {
  ami                    = data.aws_ami.amazon_linux.id  # Operating system
  instance_type          = "t2.micro"                     # Size 
  key_name               = var.key_name                   # SSH key to access it
  subnet_id              = data.aws_subnets.public.ids[0] # Put it in a public subnet
  vpc_security_group_ids = [aws_security_group.pipeline_sg.id]
  associate_public_ip_address = true                           # Give it a public IP

  tags = {
    Name = "c21-george-pipeline"
  }
}