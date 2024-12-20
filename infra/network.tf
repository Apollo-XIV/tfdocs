locals {
  vpc_cidr             = "10.100.0.0/16"
  address_space        = [for block in cidrsubnets(local.vpc_cidr, 1, 1) : cidrsubnets(block, 2, 2)]
  public_subnet_cidrs  = local.address_space[0]
  private_subnet_cidrs = local.address_space[1]
}

module "network" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.17.0"

  azs             = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  public_subnets  = local.public_subnet_cidrs
  private_subnets = local.private_subnet_cidrs

  enable_nat_gateway = true
  single_nat_gateway = true
}
