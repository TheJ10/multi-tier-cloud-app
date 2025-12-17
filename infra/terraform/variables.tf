variable "project" {
  description = "Project name prefix"
  type        = string
  default     = "mta"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "my_ip" {
  description = "My public IP for SSH/API access"
  type        = string
}
