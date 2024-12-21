locals {
  prefix = "tfdocs-${var.env}"
}

provider "aws" {
  region = "eu-west-1"
}
