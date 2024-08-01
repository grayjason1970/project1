variable "region" {
  default = "us-west-2"
}

variable "servers_az" {
  default = "us-west-2a"
}

variable "workstations_az" {
  default = "us-west-2b"
}

variable "public_az" {
  default = "us-west-2c"
}

variable "vpc_cidr" { default = "10.10.0.0/16" }
variable "servers_cidr" { default = "10.10.8.0/21" }
variable "workstations_cidr" { default = "10.10.24.0/21" }
variable "public_cidr" { default = "10.10.40.0/25" }
