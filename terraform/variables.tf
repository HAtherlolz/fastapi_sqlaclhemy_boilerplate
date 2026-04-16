variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.small"
}

variable "ami_id" {
  description = "AMI ID (Ubuntu 24.04 LTS). Leave empty to use latest Ubuntu AMI."
  type        = string
  default     = ""
}

variable "key_name" {
  description = "Name of existing AWS SSH key pair"
  type        = string
}

variable "project_name" {
  description = "Project name for resource tagging"
  type        = string
  default     = "fastapi-boilerplate"
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed for SSH access (e.g. your IP: 1.2.3.4/32)"
  type        = string
  default     = "0.0.0.0/0"
}

variable "root_volume_size" {
  description = "Root EBS volume size in GB"
  type        = number
  default     = 20
}

