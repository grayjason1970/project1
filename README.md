# Project1 Terraform Configuration
This repository contains a Terraform configuration for setting up an AWS Virtual Private Cloud (VPC) named Project1. The configuration includes creating subnets, an internet gateway, route tables, security groups and a simple mysql server.  You can use this to setup an inital VPC which can then be used in conjunction with my deployment project https://github.com/grayjason1970/deployment_project

## Prerequisites
* Terraform installed on your local machine
* AWS CLI configured with appropriate access
* An S3 bucket for storing Terraform state files

## Terraform Resources
### Provider Configuration

The AWS provider is configured to use the region specified in the Terraform variables.
```bash
provider "aws" {
  region = var.region
}
```

## Backend Configuration

Terraform state is stored in an S3 bucket to enable remote state management.

```bash
terraform {
  backend "s3" {
    bucket = "your-s3-bucket"
    key    = "terraform/state"
    region = "us-west-2"
  }
}
```

## VPC

Creates a VPC with DNS support and DNS hostnames enabled.

```bash
resource "aws_vpc" "your-vpc-name" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "Project1-VPC"
  }
}
```

## Subnets

Creates three subnets: servers, workstations, and public.

```bash
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
```

## Internet Gateway and Route Tables

Creates an internet gateway and a public route table with an association to the public subnet.

```bash
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.your-vpc-name.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.your-vpc-name.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }
}

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
```

## Security Group

Creates a security group with specific ingress and egress rules.

```bash
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
```

## Outputs

Outputs the IDs of the created VPC and subnets.

```bash
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
```

## Variables

Ensure you have the following variables defined in your Terraform variables file (variables.tf or .tfvars):

```bash
variable "region" {
  description = "AWS region"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "servers_cidr" {
  description = "CIDR block for the servers subnet"
  type        = string
}

variable "servers_az" {
  description = "Availability zone for the servers subnet"
  type        = string
}

variable "workstations_cidr" {
  description = "CIDR block for the workstations subnet"
  type        = string
}

variable "workstations_az" {
  description = "Availability zone for the workstations subnet"
  type        = string
}

variable "public_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
}

variable "public_az" {
  description = "Availability zone for the public subnet"
  type        = string
}
```

## Usage

Initialize Terraform:

```bash
terraform init
```

Apply the configuration:

```bash
terraform apply
```
Confirm the apply with yes.

This will create the VPC, subnets, internet gateway, route table, and security group as defined in the configuration.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
* Terraform documentation and community resources
* AWS documentation and best practices

Feel free to modify and extend this configuration as needed for your specific requirements.
