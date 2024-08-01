provider "aws" {
  region = var.region
}

terraform {
  backend "s3" {
    bucket = "your-s3-bucket"
    key    = "terraform/state"
    region = "us-west-2"
  }
}

resource "aws_vpc" "your-vpc-name" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true
    tags = {
    Name = "Project1-VPC"
  }
}

resource "aws_subnet" "servers" {
  vpc_id            = aws_vpc.your-vpc-name.id
  cidr_block        = var.servers_cidr
  availability_zone = var.servers_az
  map_public_ip_on_launch = true
    tags = {
    Name = "servers"
  }
}

resource "aws_subnet" "workstations" {
  vpc_id            = aws_vpc.your-vpc-name.id
  cidr_block        = var.workstations_cidr
  availability_zone = var.workstations_az
    tags = {
    Name = "workstations"
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.your-vpc-name.id
  cidr_block        = var.public_cidr
  availability_zone = var.public_az
    tags = {
    Name = "public"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.project1.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.project1.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

data "aws_caller_identity" "current" {}

output "vpc_id" {
  value = aws_vpc.your-vpc-name.id
}

output "servers_subnet_id" {
  value = aws_subnet.servers.id
}

output "workstations_subnet_id" {
  value = aws_subnet.workstations.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

resource "aws_security_group" "your-vpc-name_sg" {
  vpc_id = aws_vpc.your-vpc-name.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.10.0.0/16"]
  }

  tags = {
    Name = "your-vpc-name"
  }
}
provider "aws" {
  region = "us-west-2"
}