provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ID
    secret_key = var.AWS_SECRET
}

#refer to existing resources
data "aws_vpc" "c21-vpc"{
    id = var.VPC_ID
}

#Security Group
resource "aws_security_group" "db-sg" {
  name        = "c21-george-museum-sg"
  vpc_id      = data.aws_vpc.c21-vpc.id
}

resource "aws_vpc_security_group_ingress_rule" "db-sg-inbound-postgres" {
  security_group_id = aws_security_group.db-sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 5432
  ip_protocol       = "tcp"
  to_port           = 5432
}

# Database 
resource "aws_db_instance" "museum-db" {
    allocated_storage            = 10
    db_name                      = "museum"
    identifier                   = "c21-george-museum"
    engine                       = "postgres"
    engine_version               = "17.6"
    instance_class               = "db.t3.micro"
    publicly_accessible          = true
    performance_insights_enabled = false
    skip_final_snapshot          = true
    db_subnet_group_name         = "c21-public-subnet-group"
    vpc_security_group_ids       = [aws_security_group.db-sg.id]
    username                     = var.DB_USERNAME
    password                     = var.DB_PASSWORD
}