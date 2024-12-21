locals {
  vpc_cidr = "10.100.0.0/24"
  // make a 2 x 2 network (2 private, 2 public)
  address_space        = [for block in cidrsubnets(local.vpc_cidr, 1, 1) : cidrsubnets(block, 1, 1)]
  public_subnet_cidrs  = local.address_space[0]
  private_subnet_cidrs = local.address_space[1]
}

module "network" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.17.0"

  cidr            = local.vpc_cidr
  azs             = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  public_subnets  = local.public_subnet_cidrs
  private_subnets = local.private_subnet_cidrs

  enable_nat_gateway = true
  single_nat_gateway = true
}
