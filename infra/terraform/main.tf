terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
  profile = "infra"
}

data "aws_vpc" "main" {
  id = "vpc-0e9d8bfc817560e14"
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
}

resource "aws_ecs_cluster" "main"{ 
 name = "${var.project}-cluster"
}

resource "aws_security_group" "backend_sg" {
  name        = "${var.project}-backend-sg"
  description = "Security group for ECS backend"
  vpc_id      = data.aws_vpc.main.id

  ingress {
    description = "Allow backend access"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project}-backend-sg"
  }
}
