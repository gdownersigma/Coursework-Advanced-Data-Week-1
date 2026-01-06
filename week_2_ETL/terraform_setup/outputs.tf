output "instance_public_ip" {
  description = "Public IP address of your EC2 server"
  value       = aws_instance.pipeline.public_ip
}

output "ssh_command" {
  description = "Command to connect to your server"
  value       = "ssh -i ${var.key_name}.pem ec2-user@${aws_instance.pipeline.public_ip}"
}