output "region" {
  description = "AWS region used by Terraform"
  value       = var.region
}

output "aws_vpc_id" {
  value = data.aws_vpc.main.id
}


output "subnet_ids" {
  value = data.aws_subnets.private.ids
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ecs_cluster_arn" {
  value = aws_ecs_cluster.main.arn
}
