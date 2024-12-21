locals {
  vpc_cidr             = "10.100.0.0/24"
  address_space        = cidrsubnets(local.vpc_cidr, 2, 2, 2, 2)          # Split into 4 CIDR blocks
  public_subnet_cidrs  = [local.address_space[0], local.address_space[1]] # Use the first two blocks
  private_subnet_cidrs = [local.address_space[2], local.address_space[3]] # Use the next two blocks
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
