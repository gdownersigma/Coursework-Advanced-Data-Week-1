variable "DB_USERNAME" {
    type        = string
}
variable "DB_PASSWORD" {
    type        = string
}

variable "AWS_REGION" {
    type        = string
    default     = "eu-west-2"
}

variable "AWS_ID" {
    type        = string

}

variable "AWS_SECRET" {
    type        = string
}
variable "VPC_ID" {
  type        = string
}