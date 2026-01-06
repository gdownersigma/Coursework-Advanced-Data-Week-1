# AWS credentials
variable "AWS_REGION" {
  description = "Which AWS region to create resources in"
  type        = string
}

variable "AWS_ID" {
  description = "Your AWS access key ID"
  type        = string
  sensitive   = true
}

variable "AWS_SECRET" {
  description = "Your AWS secret access key"
  type        = string
  sensitive   = true
}

# Network
variable "VPC_ID" {
  description = "The ID of your organisation's VPC"
  type        = string
}

# SSH access
variable "key_name" {
  description = "Name of the SSH key pair to access the server"
  type        = string
}